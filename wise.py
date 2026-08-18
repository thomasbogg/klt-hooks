import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from werkzeug.datastructures import Headers

from correspondence.self.functions import contact_self


def verify_wise_payload_signature(headers: Headers, raw_data: bytes, public_key_pem: str) -> bool:
    """RSA-SHA256 (PKCS1v15) verification of Wise's X-Signature-SHA256 header against the raw
    request body, per Wise's official reference implementation:
    https://github.com/transferwise/digital-signatures-examples/tree/main/verify-webhook-signature

    Returns False (not verified) if public_key_pem is empty - this is deliberate, not a bug. As of
    2026-08-18 only a labelled-sandbox key was ever confirmed; the real production key was never
    found (Wise doesn't publish it, and Personal API tokens don't expose an endpoint for it). Don't
    fall back to the sandbox key here - a wrong key would either reject every real request or, far
    worse, create false confidence that verification is happening when it isn't actually checking
    against Wise's real signing key.
    """
    if not public_key_pem:
        return False

    signature_b64 = headers.get('X-Signature-SHA256')
    if not signature_b64:
        return False

    try:
        signature = base64.b64decode(signature_b64)
        public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))
        public_key.verify(signature, raw_data, padding.PKCS1v15(), hashes.SHA256())
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False


def log_invalid_wise_callback(headers: dict, raw_data: str) -> None:
    contact_self(
        subject="Invalid or unverified Wise callback received",
        body=(
            "Received a Wise callback that failed signature verification (or verification isn't "
            "configured yet - see WISE_WEBHOOK_PUBLIC_KEY in default/settings.py).\n"
            f"Headers: {headers}\n"
            f"Data: {raw_data}"
        ),
    )
