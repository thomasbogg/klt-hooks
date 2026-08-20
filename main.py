from flask import Flask, request
import json
import os
from revolut import process_revolut_merchant_callback, verify_revolut_payload_signature
from default.settings import REVOLUT_MERCHANT_API_SIGNING_KEY, REVOLUT_BOOKING_DEPOSIT_WEBHOOK_SIGNING_KEY, WISE_WEBHOOK_PUBLIC_KEY
from correspondence.self.functions import contact_self
from postgres_bookings import IN_PROGRESS_EVENTS, FAILURE_STATUS_BY_EVENT, mark_payment_in_progress, mark_payment_authenticated, mark_payment_paid, mark_payment_failed
from wise import verify_wise_payload_signature, log_invalid_wise_callback


app = Flask(__name__)


@app.route("/revolut/callback", methods=["POST"])
def revolut_merchant_callback():
    try:
        if verify_revolut_payload_signature(request.headers, request.data, REVOLUT_MERCHANT_API_SIGNING_KEY):

            data = json.loads(request.data)
            if not data['event'] == 'ORDER_COMPLETED':
                _contact_self_for_error(f"Received unexpected event type: {data['event']}", request.data.decode('utf-8'), dict(request.headers))
            else:
                process_revolut_merchant_callback(data)

    except Exception as e:
        _contact_self_for_error(str(e), request.data.decode('utf-8'), dict(request.headers))

    return ('', 204) # Return 204 to indicate that the callback was received, even if there was an error processing it


@app.route("/revolut/booking-deposit-callback", methods=["POST"])
def revolut_booking_deposit_callback():
    """Separate webhook subscription (own signing key, own event list) from the tourist-tax route
    above - writes into klt-web's shared Postgres tables via postgres_bookings.py, not the legacy
    SQLite layer default/database/ uses. See bookings/models.py::Payment in klt-web."""
    return ('', 204)
    try:
        if verify_revolut_payload_signature(request.headers, request.data, REVOLUT_BOOKING_DEPOSIT_WEBHOOK_SIGNING_KEY):
            data = json.loads(request.data)
            event = data['event']
            order_id = data['order_id']

            if event in IN_PROGRESS_EVENTS:
                found = mark_payment_in_progress(order_id, event)
            elif event == 'ORDER_PAYMENT_AUTHENTICATED':
                found = mark_payment_authenticated(order_id)
            elif event == 'ORDER_COMPLETED':
                result = mark_payment_paid(order_id)
                found = result != 'not_found'
                if result == 'conflict':
                    _contact_self_for_error(
                        f"Payment received for order {order_id} but its dates now conflict with another "
                        f"booking - flagged as 'Payment received - needs review', calendar NOT double-booked. "
                        f"Manually resolve which guest keeps the dates (refund one, or contact them to rebook).",
                        request.data.decode('utf-8'), dict(request.headers),
                    )
            elif event in FAILURE_STATUS_BY_EVENT:
                found = mark_payment_failed(order_id, event)
            else:
                _contact_self_for_error(f"Received unexpected event type: {event}", request.data.decode('utf-8'), dict(request.headers))
                found = True

            if not found:
                _contact_self_for_error(f"No booking payment found for order_id: {order_id}", request.data.decode('utf-8'), dict(request.headers))

    except Exception as e:
        _contact_self_for_error(str(e), request.data.decode('utf-8'), dict(request.headers))

    return ('', 204)


@app.route("/wise/balance-update-callback", methods=["POST"])
def wise_balance_update_callback():
    """Receives Wise's account-deposit webhook. Wise automation is paused as of 2026-08-18 -
    Personal API tokens can't retrieve balance statements for Portugal-based accounts, which
    blocks the reference-matching this would need to actually confirm a payment - so this stays
    logging-only. Do not wire this to postgres_bookings.py-style payment confirmation until that's
    resolved. Signature verification is real (RSA-SHA256 against WISE_WEBHOOK_PUBLIC_KEY, see
    wise.py) but the key itself is currently unset - see default/settings.py for why - so every
    request fails verification for now. That's expected given this is a public URL with no other
    auth, so it's only escalated (via email) when a key IS configured and still fails; while unset,
    failures are just logged, not emailed, to avoid spamming on ordinary/test traffic.
    """
    is_test = request.headers.get('X-Test-Notification', '').lower() == 'true'
    verified = verify_wise_payload_signature(request.headers, request.data, WISE_WEBHOOK_PUBLIC_KEY)

    if not verified and WISE_WEBHOOK_PUBLIC_KEY:
        log_invalid_wise_callback(dict(request.headers), request.data.decode('utf-8', errors='replace'))

    try:
        data = json.loads(request.data)
        print(f"[wise webhook] verified={verified} test={is_test} event_type={data.get('event_type')} data={data.get('data')}", flush=True)
    except Exception as e:
        print(f"[wise webhook] verified={verified} failed to parse body: {e} - raw: {request.data.decode('utf-8', errors='replace')}", flush=True)

    return {"status": "ok"}, 200


def _contact_self_for_error(e: str, data: str, headers: dict) -> None:
    contact_self(
        subject=f"Error occurred: {e}",
        body=f"Error: {e}\nData: {data}\nHeaders: {headers}",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)