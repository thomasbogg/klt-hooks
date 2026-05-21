import hashlib
import hmac
from werkzeug.datastructures import Headers

from correspondence.self.functions import new_email_to_self, send_email_to_self
from correspondence.guest.functions import new_guest_arrival_email, send_guest_email
from default.booking.booking import Booking
from default.database.database import Database
from default.database.functions import get_database, get_tourist_tax_booking
from default.settings import REVOLUT_API_SIGNING_KEY
from wrapper import pull_database


@pull_database
def process_revolut_callback(data: dict) -> None:
    """
    Process the Revolut callback data for an order completion event.
    
    Args:
        data: The data received from the Revolut callback, expected to contain order information.
    
    Returns:
        None
    """
    orderId = data['order_id']

    database = get_database()
    booking = _get_tourist_tax_booking(database, orderId)

    if booking.charges.touristtax.paid:
        database.close()
        return
        
    booking.charges.touristtax.paid = True
    booking.update()
    database.close()

    total = booking.charges.touristtax.total

    ## EMAIL self for reference check
    user, message = new_email_to_self(subject = f"Revolut payment received for {booking.guest.fullName}")
    body = message.body
    body.paragraph(f"Received a payment of €{'{:.2f}'.format(total)} for order {orderId} via Revolut.")
    body.paragraph(f"Booking {booking.id} has been updated at touristtax table row {booking.charges.touristtax.id}.")
    send_email_to_self(user, message)

    ## EMAIL guest to confirm receipt of tourist tax payment
    user, message = new_guest_arrival_email(topic=f'Tourist Tax Paid', booking=booking)
    body = message.body
    body.paragraph(f"Thank you very much for your tourist tax payment of €{'{:.2f}'.format(total)}.")
    body.paragraph(f"This email serves as confirmation of your payment.")
    body.paragraph(f"If you have questions or concerns, please do not hesitate to contact us.")
    send_guest_email(user, message)


def verify_revolut_payload_signature(headers: Headers, raw_data: bytes) -> bool:
    timestamp = headers.get('Revolut-Request-Timestamp')
    payload_to_sign = 'v1.' + timestamp + '.' + raw_data.decode('utf-8')
    signature = 'v1=' + hmac.new(bytes(REVOLUT_API_SIGNING_KEY, 'utf-8'), msg = bytes(payload_to_sign, 'utf-8'), digestmod = hashlib.sha256).hexdigest()
    isRevolut = signature == headers.get('Revolut-Signature')
    if not isRevolut:
        log_invalid_revolut_callback(timestamp, payload_to_sign, signature, headers.get('Revolut-Signature'), REVOLUT_API_SIGNING_KEY)
    return isRevolut


def log_invalid_revolut_callback(timestamp, payload_to_sign, signature, received_signature, signing_key):
    user, message = new_email_to_self(subject = "Invalid Revolut callback received")
    message.body.paragraph("Received an invalid Revolut callback. The payload signature verification failed.")
    message.body.paragraph(f"Timestamp: {timestamp}")
    message.body.paragraph(f"Payload to sign: {payload_to_sign}")
    message.body.paragraph(f"Calculated signature: {signature}")
    message.body.paragraph(f"Received signature: {received_signature}")
    message.body.paragraph(f"Signing key used: {signing_key}")
    send_email_to_self(user, message)


def _get_tourist_tax_booking(database: Database, orderId: str) -> Booking | None:
    """
    Retrieve the booking associated with the given order ID for tourist tax calculation.
    
    Args:
        database: The database instance to query.
        orderId: The order ID from the Revolut callback to search for.
        
    Returns:
        The booking object associated with the order ID, or None if not found.
    """
    search = get_tourist_tax_booking(database, orderId)

    select = search.guests.select()
    select.firstName()
    select.lastName()
    select.email()
    select.preferredLanguage()

    select = search.properties.select()
    select.name()

    select = search.touristtax.select()
    select.total()

    return search.fetchone()