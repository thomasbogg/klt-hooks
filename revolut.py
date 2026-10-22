import hashlib
import hmac

import requests
from werkzeug.datastructures import Headers

from correspondence.self.functions import contact_self
from default.settings import REVOLUT_MERCHANT_API_SECRET_KEY

MERCHANT_ORDER_URL = 'https://merchant.revolut.com/api/1.0/orders/{}'


def verify_revolut_payload_signature(headers: Headers, raw_data: bytes, signing_secret: str) -> bool:
    timestamp = headers.get('Revolut-Request-Timestamp')
    received_signature = headers.get('Revolut-Signature')
    if not timestamp or not received_signature:
        # Not a Revolut call at all (a probe, a scanner, a wrong URL): Revolut always sends both
        # headers. Refused quietly - it must not email an error to anyone who finds the address.
        return False
    payload_to_sign = 'v1.' + timestamp + '.' + raw_data.decode('utf-8')
    signature = 'v1=' + hmac.new(bytes(signing_secret, 'utf-8'), msg = bytes(payload_to_sign, 'utf-8'), digestmod = hashlib.sha256).hexdigest()
    isRevolut = hmac.compare_digest(signature.encode(), received_signature.encode())
    if not isRevolut:
        log_invalid_revolut_callback(timestamp, payload_to_sign, signature, received_signature)
    return isRevolut


def log_invalid_revolut_callback(timestamp, payload_to_sign, signature, received_signature):
    contact_self(
        subject="Invalid Revolut callback received",
        body=(
            "Received an invalid Revolut callback. The payload signature verification failed.\n"
            f"Timestamp: {timestamp}\n"
            f"Payload to sign: {payload_to_sign}\n"
            f"Calculated signature: {signature}\n"
            f"Received signature: {received_signature}"
        ),
    )


def revolut_order_state(order_id: str) -> str | None:
    """The order's state as Revolut itself holds it ('completed', 'pending', 'cancelled', ...), or
    None when it cannot be read. A signed webhook is not taken at its word where money is concerned
    (2026-10-22, after Railway's environment-variable breach exposed the signing secret): the
    booking route only records ORDER_COMPLETED once Revolut confirms the order really is
    completed, so a leaked secret alone can never mark an unpaid booking paid."""
    try:
        response = requests.get(
            MERCHANT_ORDER_URL.format(order_id),
            headers={'Authorization': f'Bearer {REVOLUT_MERCHANT_API_SECRET_KEY}'}, timeout=15,
        )
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    state = response.json().get('state')
    return state.lower() if isinstance(state, str) else None
