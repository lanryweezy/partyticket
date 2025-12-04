from flask import current_app, render_template, url_for
from flask_mail import Message
from app import mail, db
from app.models import Ticket, Event, User
import qrcode
import base64
from io import BytesIO
from datetime import datetime


def _ensure_ticket_qr(ticket: Ticket) -> None:
    """Generate and store a QR code for a ticket if it does not already have one."""
    if ticket.qr_code:
        return

    qr_data = f"ticket_id:{ticket.id}:event_id:{ticket.event_id}"
    qr_img = qrcode.make(qr_data)
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    ticket.qr_code = qr_code_base64


def _generate_calendar_link(event: Event) -> str:
    """Generate Google Calendar link for event."""
    start_time = event.date.strftime('%Y%m%dT%H%M%S')
    end_time = (event.date.replace(hour=event.date.hour + 3)).strftime('%Y%m%dT%H%M%S')
    title = event.name.replace(' ', '+')
    location = event.location.replace(' ', '+')
    details = event.description[:200].replace(' ', '+')
    
    return (f"https://calendar.google.com/calendar/render?"
            f"action=TEMPLATE&text={title}&dates={start_time}/{end_time}"
            f"&details={details}&location={location}")


def send_ticket_confirmation_email(user: User, event: Event, tickets: list[Ticket]) -> None:
    """
    Send a beautiful HTML ticket confirmation email with QR codes to the buyer.
    This is a best-effort helper; it logs errors but does not raise.
    """
    if not user or not user.email:
        return

    try:
        # Ensure all tickets have QR codes
        for ticket in tickets:
            _ensure_ticket_qr(ticket)
        db.session.commit()

        # Generate calendar link
        calendar_link = _generate_calendar_link(event)

        subject = f"🎫 Your ticket(s) for {event.name} - PartyTicket Nigeria"
        msg = Message(
            subject=subject,
            recipients=[user.email],
        )

        # Render beautiful HTML template
        msg.html = render_template(
            'emails/ticket_confirmation.html',
            user=user,
            event=event,
            tickets=tickets,
            calendar_link=calendar_link
        )

        mail.send(msg)
        current_app.logger.info(f"Ticket confirmation email sent to {user.email}")
    except Exception as e:
        current_app.logger.error(f"Failed to send ticket confirmation email: {e}")


def send_organizer_notification(event: Event, tickets_sold: int, total_capacity: int = None) -> None:
    """Send notification to organizer when tickets are selling well or sold out."""
    organizer = event.organizer
    if not organizer or not organizer.email:
        return
    
    try:
        percentage = (tickets_sold / total_capacity * 100) if total_capacity else 0
        
        if percentage >= 100:
            subject = f"🎉 {event.name} is SOLD OUT!"
            message = f"Congratulations! Your event '{event.name}' is completely sold out with {tickets_sold} tickets sold!"
        elif percentage >= 80:
            subject = f"🔥 {event.name} is Almost Sold Out!"
            message = f"Great news! Your event '{event.name}' is {percentage:.0f}% sold out ({tickets_sold}/{total_capacity} tickets)."
        else:
            return  # Don't send for low sales
        
        msg = Message(
            subject=subject,
            recipients=[organizer.email],
            html=f"""
            <h2>{subject}</h2>
            <p>{message}</p>
            <p>Event: {event.name}</p>
            <p>Date: {event.date.strftime('%A, %B %d, %Y at %I:%M %p')}</p>
            <p>Location: {event.location}</p>
            <p>Keep up the great work!</p>
            <p>Best regards,<br>PartyTicket Nigeria</p>
            """
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send organizer notification: {e}")


