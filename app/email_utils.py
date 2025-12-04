from flask import current_app
from flask_mail import Message
from app import mail, db
from app.models import Ticket, Event, User
import qrcode
import base64
from io import BytesIO


def _ensure_ticket_qr(ticket: Ticket) -> None:
    """Generate and store a QR code for a ticket if it does not already have one."""
    if ticket.qr_code:
        return

    qr_data = f"ticket_id:{ticket.id}"
    qr_img = qrcode.make(qr_data)
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    ticket.qr_code = qr_code_base64


def send_ticket_confirmation_email(user: User, event: Event, tickets: list[Ticket]) -> None:
    """
    Send a ticket confirmation email with QR codes to the buyer.
    This is a best-effort helper; it logs errors but does not raise.
    """
    if not user or not user.email:
        return

    try:
        # Ensure all tickets have QR codes
        for ticket in tickets:
            _ensure_ticket_qr(ticket)
        db.session.commit()

        subject = f"Your ticket(s) for {event.name}"
        msg = Message(
            subject=subject,
            recipients=[user.email],
        )

        ticket_list_html = "".join(
            f"<li>Ticket ID: {t.id}</li>"
            for t in tickets
        )

        # Use QR code of the first ticket as primary visual
        first_qr = tickets[0].qr_code if tickets and tickets[0].qr_code else None
        qr_img_html = (
            f'<p><img src="data:image/png;base64,{first_qr}" alt="Ticket QR Code" '
            f'style="max-width:200px;height:auto;"/></p>'
            if first_qr
            else ""
        )

        msg.html = f"""
        <p>Hi {user.username},</p>
        <p>Thank you for your purchase on <strong>PartyTicket Nigeria</strong>.</p>
        <p><strong>Event:</strong> {event.name}<br>
           <strong>Date:</strong> {event.date.strftime('%A, %B %d, %Y at %I:%M %p')}<br>
           <strong>Location:</strong> {event.location}</p>
        <p><strong>Tickets:</strong></p>
        <ul>
            {ticket_list_html}
        </ul>
        {qr_img_html}
        <p>Please present this QR code (or your Ticket ID) at the event entrance for verification.</p>
        <p>If you did not make this purchase, please contact support immediately.</p>
        <p>Best regards,<br>PartyTicket Nigeria</p>
        """

        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send ticket confirmation email: {e}")


