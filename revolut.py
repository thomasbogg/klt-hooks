import hashlib
import hmac
from werkzeug.datastructures import Headers

from correspondence.self.functions import new_email_to_self, send_email_to_self
from correspondence.guest.functions import new_guest_arrival_email, send_guest_email
from default.database.rows.touristtax import Touristtax
from default.database.database import Database
from default.database.functions import open_database, get_touristtax_payment
from default.dates import dates
from wrapper import pull_database


@pull_database
def process_revolut_merchant_callback(data: dict) -> None:
    """
    Process the Revolut callback data for an order completion event.
    
    Args:
        data: The data received from the Revolut callback, expected to contain order information.
    
    Returns:
        None
    """
    orderId = data['order_id']

    database = open_database()
    touristtax = _get_touristtax_payment(database, orderId)

    if touristtax and touristtax.paid:
        database.close()
        return

    touristtax = Touristtax(database)
    touristtax.orderId = orderId
    touristtax.date = dates.date()        
    touristtax.paid = True
    touristtax.insert()
    database.close()


def verify_revolut_payload_signature(headers: Headers, raw_data: bytes, signing_secret: str) -> bool:
    timestamp = headers.get('Revolut-Request-Timestamp')
    payload_to_sign = 'v1.' + timestamp + '.' + raw_data.decode('utf-8')
    signature = 'v1=' + hmac.new(bytes(signing_secret, 'utf-8'), msg = bytes(payload_to_sign, 'utf-8'), digestmod = hashlib.sha256).hexdigest()
    isRevolut = signature == headers.get('Revolut-Signature')
    if not isRevolut:
        log_invalid_revolut_callback(timestamp, payload_to_sign, signature, headers.get('Revolut-Signature'), signing_secret)
    return isRevolut


def log_invalid_revolut_callback(timestamp, payload_to_sign, signature, received_signature, signing_secret):
    user, message = new_email_to_self(subject = "Invalid Revolut callback received")
    message.body.paragraph("Received an invalid Revolut callback. The payload signature verification failed.")
    message.body.paragraph(f"Timestamp: {timestamp}")
    message.body.paragraph(f"Payload to sign: {payload_to_sign}")
    message.body.paragraph(f"Calculated signature: {signature}")
    message.body.paragraph(f"Received signature: {received_signature}")
    message.body.paragraph(f"Signing key used: {signing_secret}")
    send_email_to_self(user, message)


def _get_touristtax_payment(database: Database, orderId: str) -> Touristtax | None:
    """
    Retrieve the booking associated with the given order ID for tourist tax calculation.
    
    Args:
        database: The database instance to query.
        orderId: The order ID from the Revolut callback to search for.
        
    Returns:
        The Touristtax object associated with the order ID, or None if not found.
    """
    search = get_touristtax_payment(database, orderId)
    return search.fetchone()