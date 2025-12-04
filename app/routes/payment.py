from flask import Blueprint, request, jsonify, current_app, url_for, flash, redirect
from flask_login import login_required, current_user
import requests
import json
import hashlib
import hmac
from app import db
from app.models import Transaction, Ticket, Event, User
from app.email_utils import send_ticket_confirmation_email
from datetime import datetime
import qrcode
import base64
from io import BytesIO

payment = Blueprint('payment', __name__)

def calculate_platform_fee(amount, fee_percent=None):
    """Calculate platform fee and organizer amount."""
    if fee_percent is None:
        fee_percent = float(current_app.config.get('PLATFORM_FEE_PERCENT', 2.5))
    platform_fee = (amount * fee_percent) / 100
    organizer_amount = amount - platform_fee
    return platform_fee, organizer_amount

@payment.route('/paystack/webhook', methods=['POST'])
def paystack_webhook():
    """Handle Paystack webhook for payment events."""
    try:
        # Verify webhook signature
        signature = request.headers.get('X-Paystack-Signature')
        if not signature:
            return jsonify({'error': 'Missing signature'}), 400
        
        # Verify signature (Paystack sends raw body)
        secret = current_app.config['PAYSTACK_SECRET_KEY']
        computed_signature = hmac.new(
            secret.encode('utf-8'),
            request.data,
            hashlib.sha512
        ).hexdigest()
        
        if computed_signature != signature:
            current_app.logger.warning('Invalid Paystack webhook signature')
            return jsonify({'error': 'Invalid signature'}), 400
        
        data = request.get_json()
        event_type = data.get('event')
        
        if event_type == 'charge.success':
            payment_data = data.get('data', {})
            reference = payment_data.get('reference')
            amount = payment_data.get('amount', 0) / 100  # Convert from kobo to Naira
            metadata = payment_data.get('metadata', {})
            
            # Find or create transaction
            transaction = Transaction.query.filter_by(reference=reference).first()
            if not transaction:
                # Create transaction from metadata
                user_id = metadata.get('user_id')
                event_id = metadata.get('event_id')
                quantity = metadata.get('quantity', 1)
                
                if not user_id or not event_id:
                    current_app.logger.error(f'Missing metadata in Paystack webhook: {metadata}')
                    return jsonify({'error': 'Missing metadata'}), 400
                
                transaction = Transaction(
                    user_id=user_id,
                    event_id=event_id,
                    provider='paystack',
                    reference=reference,
                    amount=amount,
                    status='pending'
                )
                db.session.add(transaction)
                db.session.flush()
            
            # Calculate fees
            platform_fee, organizer_amount = calculate_platform_fee(amount)
            
            # Mark transaction as success
            transaction.mark_success(payment_data, platform_fee, organizer_amount)
            
            # Update tickets
            tickets = Ticket.query.filter_by(paystack_ref=reference).all()
            if not tickets:
                # Create tickets if they don't exist
                event = Event.query.get(transaction.event_id)
                user = User.query.get(transaction.user_id)
                quantity = metadata.get('quantity', 1)
                
                for i in range(quantity):
                    ticket = Ticket(
                        event_id=event.id,
                        user_id=user.id,
                        paystack_ref=reference,
                        payment_status='success',
                        amount_paid=event.price,
                        date_purchased=datetime.utcnow()
                    )
                    # Generate QR code
                    qr_data = f"ticket_id:{ticket.id}:event_id:{event.id}"
                    qr_img = qrcode.make(qr_data)
                    buffered = BytesIO()
                    qr_img.save(buffered, format="PNG")
                    ticket.qr_code = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    db.session.add(ticket)
                
                db.session.flush()
                tickets = Ticket.query.filter_by(paystack_ref=reference).all()
            
            # Update ticket statuses
            for ticket in tickets:
                ticket.payment_status = 'success'
            
            # Update organizer earnings
            event = Event.query.get(transaction.event_id)
            if event:
                organizer = User.query.get(event.organizer_id)
                if organizer:
                    organizer.earnings += organizer_amount
            
            db.session.commit()
            
            # Send confirmation email
            if tickets:
                try:
                    send_ticket_confirmation_email(user, event, tickets)
                except Exception as e:
                    current_app.logger.error(f'Failed to send ticket email: {str(e)}')
            
            return jsonify({'status': 'success'}), 200
        
        return jsonify({'status': 'ignored'}), 200
        
    except Exception as e:
        current_app.logger.error(f'Paystack webhook error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payment.route('/paystack/initialize', methods=['POST'])
@login_required
def initialize_payment():
    """Initialize Paystack payment for tickets."""
    data = request.get_json()
    event_id = data.get('event_id')
    quantity = data.get('quantity', 1)
    email = data.get('email', current_user.email)
    
    if not event_id or not email:
        return jsonify({'error': 'Missing required fields'}), 400
    
    event = Event.query.get_or_404(event_id)
    total_amount = event.price * quantity
    amount_kobo = int(total_amount * 100)  # Convert to kobo
    
    # Generate unique reference
    import secrets
    reference = f"PT-{secrets.token_hex(8)}"
    
    # Create pending transaction
    transaction = Transaction(
        user_id=current_user.id,
        event_id=event.id,
        provider='paystack',
        reference=reference,
        amount=total_amount,
        status='initialized'
    )
    db.session.add(transaction)
    
    # Create pending tickets
    tickets = []
    for i in range(quantity):
        ticket = Ticket(
            event_id=event.id,
            user_id=current_user.id,
            paystack_ref=reference,
            payment_status='pending',
            amount_paid=event.price,
            date_purchased=datetime.utcnow()
        )
        db.session.add(ticket)
        tickets.append(ticket)
    
    db.session.commit()
    
    # Initialize Paystack payment
    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "amount": amount_kobo,
        "reference": reference,
        "callback_url": url_for('payment.verify_payment', _external=True),
        "metadata": {
            "user_id": current_user.id,
            "event_id": event.id,
            "quantity": quantity,
            "custom_fields": [
                {
                    "display_name": "Event",
                    "variable_name": "event_name",
                    "value": event.name
                }
            ]
        }
    }
    
    try:
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if result.get('status'):
            return jsonify({
                'authorization_url': result['data']['authorization_url'],
                'access_code': result['data']['access_code'],
                'reference': reference
            }), 200
        else:
            return jsonify({'error': 'Failed to initialize payment'}), 400
            
    except requests.exceptions.RequestException as e:
        db.session.rollback()
        current_app.logger.error(f'Paystack initialization error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@payment.route('/paystack/verify', methods=['GET'])
@login_required
def verify_payment():
    """Verify Paystack payment after redirect."""
    reference = request.args.get('reference')
    
    if not reference:
        flash('Payment reference missing', 'danger')
        return redirect(url_for('main.events'))
    
    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}"
    }
    
    try:
        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        response.raise_for_status()
        payment_data = response.json()
        
        if payment_data['data']['status'] == 'success':
            # Webhook should have already processed this, but verify tickets exist
            tickets = Ticket.query.filter_by(paystack_ref=reference, user_id=current_user.id).all()
            if tickets:
                event = tickets[0].event
                flash(f'Payment successful! {len(tickets)} ticket(s) purchased for {event.name}', 'success')
                return redirect(url_for('main.event_detail', event_id=event.id))
            else:
                flash('Payment verified but tickets not found. Please contact support.', 'warning')
                return redirect(url_for('main.events'))
        else:
            flash('Payment verification failed', 'danger')
            return redirect(url_for('main.events'))
            
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Paystack verification error: {str(e)}')
        flash('Error verifying payment', 'danger')
        return redirect(url_for('main.events'))

@payment.route('/flutterwave/initialize', methods=['POST'])
@login_required
def initialize_flutterwave_payment():
    """Initialize Flutterwave payment (similar structure to Paystack)."""
    data = request.get_json()
    event_id = data.get('event_id')
    quantity = data.get('quantity', 1)
    email = data.get('email', current_user.email)
    
    if not event_id or not email:
        return jsonify({'error': 'Missing required fields'}), 400
    
    event = Event.query.get_or_404(event_id)
    total_amount = event.price * quantity
    
    import secrets
    reference = f"PT-FW-{secrets.token_hex(8)}"
    
    headers = {
        "Authorization": f"Bearer {current_app.config['FLUTTERWAVE_SECRET_KEY']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "tx_ref": reference,
        "amount": total_amount,
        "currency": "NGN",
        "redirect_url": url_for('payment.verify_flutterwave_payment', _external=True),
        "customer": {
            "email": email,
            "phonenumber": current_user.phone or "",
            "name": current_user.username
        },
        "meta": {
            "user_id": current_user.id,
            "event_id": event.id,
            "quantity": quantity
        },
        "customizations": {
            "title": "PartyTicket Payment",
            "description": f"Payment for {event.name}"
        }
    }
    
    try:
        response = requests.post('https://api.flutterwave.com/v3/payments', headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if result.get('status') == 'success':
            # Create pending transaction
            transaction = Transaction(
                user_id=current_user.id,
                event_id=event.id,
                provider='flutterwave',
                reference=reference,
                amount=total_amount,
                status='initialized'
            )
            db.session.add(transaction)
            
            # Create pending tickets
            for i in range(quantity):
                ticket = Ticket(
                    event_id=event.id,
                    user_id=current_user.id,
                    paystack_ref=reference,  # Reusing field for Flutterwave ref
                    payment_status='pending',
                    amount_paid=event.price,
                    date_purchased=datetime.utcnow()
                )
                db.session.add(ticket)
            
            db.session.commit()
            
            return jsonify({
                'link': result['data']['link']
            }), 200
        else:
            return jsonify({'error': 'Failed to initialize payment'}), 400
            
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Flutterwave initialization error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@payment.route('/flutterwave/verify', methods=['GET'])
@login_required
def verify_flutterwave_payment():
    """Verify Flutterwave payment."""
    transaction_id = request.args.get('transaction_id')
    
    if not transaction_id:
        flash('Transaction ID missing', 'danger')
        return redirect(url_for('main.events'))
    
    headers = {
        "Authorization": f"Bearer {current_app.config['FLUTTERWAVE_SECRET_KEY']}"
    }
    
    try:
        response = requests.get(f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify', headers=headers)
        response.raise_for_status()
        payment_data = response.json()
        
        if payment_data['data']['status'] == 'successful':
            reference = payment_data['data']['tx_ref']
            amount = payment_data['data']['amount']
            metadata = payment_data['data'].get('meta', {})
            
            # Find transaction
            transaction = Transaction.query.filter_by(reference=reference).first()
            if transaction:
                platform_fee, organizer_amount = calculate_platform_fee(amount)
                transaction.mark_success(payment_data['data'], platform_fee, organizer_amount)
                
                # Update tickets
                tickets = Ticket.query.filter_by(paystack_ref=reference, user_id=current_user.id).all()
                for ticket in tickets:
                    ticket.payment_status = 'success'
                    # Generate QR if not exists
                    if not ticket.qr_code:
                        qr_data = f"ticket_id:{ticket.id}:event_id:{ticket.event_id}"
                        qr_img = qrcode.make(qr_data)
                        buffered = BytesIO()
                        qr_img.save(buffered, format="PNG")
                        ticket.qr_code = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                # Update organizer earnings
                event = Event.query.get(transaction.event_id)
                if event:
                    organizer = User.query.get(event.organizer_id)
                    if organizer:
                        organizer.earnings += organizer_amount
                
                db.session.commit()
                
                # Send email
                if tickets:
                    try:
                        send_ticket_confirmation_email(current_user, event, tickets)
                    except Exception as e:
                        current_app.logger.error(f'Failed to send ticket email: {str(e)}')
                
                flash(f'Payment successful! {len(tickets)} ticket(s) purchased.', 'success')
                return redirect(url_for('main.event_detail', event_id=event.id))
            else:
                flash('Transaction not found', 'danger')
                return redirect(url_for('main.events'))
        else:
            flash('Payment verification failed', 'danger')
            return redirect(url_for('main.events'))
            
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Flutterwave verification error: {str(e)}')
        flash('Error verifying payment', 'danger')
        return redirect(url_for('main.events'))
