import hashlib
import hmac
from werkzeug.datastructures import Headers

from correspondence.self.functions import contact_self


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
