from flask import Blueprint, request, jsonify, current_app, url_for
import requests
import json
import hashlib
import hmac

payment = Blueprint('payment', __name__)

@payment.route('/flutterwave/initialize', methods=['POST'])
def initialize_flutterwave_payment():
    data = request.get_json()
    email = data.get('email')
    amount = data.get('amount')  # in kobo
    reference = data.get('reference')
    currency = data.get('currency', 'NGN')

    if not all([email, amount, reference]):
        return jsonify({'error': 'Missing required fields'}), 400

    headers = {
        "Authorization": f"Bearer {current_app.config['FLUTTERWAVE_SECRET_KEY']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "tx_ref": reference,
        "amount": amount,
        "currency": currency,
        "redirect_url": url_for('payment.verify_flutterwave_payment', _external=True),
        "customer": {
            "email": email,
            "phonenumber": data.get('phone', ''),
            "name": data.get('name', '')
        },
        "customizations": {
            "title": "PartyTicket Payment",
            "description": "Payment for event ticket"
        }
    }

    try:
        response = requests.post('https://api.flutterwave.com/v3/payments', headers=headers, json=payload)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@payment.route('/flutterwave/verify', methods=['GET'])
def verify_flutterwave_payment():
    transaction_id = request.args.get('transaction_id')

    if not transaction_id:
        return jsonify({'error': 'Missing transaction_id'}), 400

    headers = {
        "Authorization": f"Bearer {current_app.config['FLUTTERWAVE_SECRET_KEY']}"
    }

    try:
        response = requests.get(f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify', headers=headers)
        response.raise_for_status()
        payment_data = response.json()

        if payment_data['data']['status'] == 'successful':
            # Here you would update your database based on the transaction_id
            # For example, mark a ticket as paid or an invitation as paid
            return jsonify({'message': 'Payment verified successfully', 'status': 'success', 'data': payment_data['data']}), 200
        else:
            return jsonify({'message': 'Payment verification failed', 'status': 'failed', 'data': payment_data['data']}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Paystack routes (keeping existing functionality)
@payment.route('/paystack/initialize', methods=['POST'])
def initialize_payment():
    data = request.get_json()
    email = data.get('email')
    amount = data.get('amount') # in kobo
    reference = data.get('reference')

    if not all([email, amount, reference]):
        return jsonify({'error': 'Missing required fields'}), 400

    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "amount": amount,
        "reference": reference,
        "callback_url": url_for('payment.verify_payment', _external=True)
    }

    try:
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=payload)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@payment.route('/paystack/verify', methods=['GET'])
def verify_payment():
    reference = request.args.get('reference')

    if not reference:
        return jsonify({'error': 'Missing reference'}), 400

    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}"
    }

    try:
        response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        response.raise_for_status()
        payment_data = response.json()

        if payment_data['data']['status'] == 'success':
            # Here you would update your database based on the reference
            # For example, mark a ticket as paid or an invitation as paid
            return jsonify({'message': 'Payment verified successfully', 'status': 'success'}), 200
        else:
            return jsonify({'message': 'Payment verification failed', 'status': 'failed'}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500