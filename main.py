from flask import Flask, request
import json
import os
from revolut import process_revolut_merchant_callback, verify_revolut_payload_signature
from default.settings import REVOLUT_MERCHANT_API_SIGNING_KEY, REVOLUT_BOOKING_DEPOSIT_WEBHOOK_SIGNING_KEY
from correspondence.self.functions import contact_self
from postgres_bookings import IN_PROGRESS_EVENTS, FAILURE_STATUS_BY_EVENT, mark_payment_in_progress, mark_payment_paid, mark_payment_failed


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
    try:
        if verify_revolut_payload_signature(request.headers, request.data, REVOLUT_BOOKING_DEPOSIT_WEBHOOK_SIGNING_KEY):
            data = json.loads(request.data)
            event = data['event']
            order_id = data['order_id']

            if event in IN_PROGRESS_EVENTS:
                found = mark_payment_in_progress(order_id, event)
            elif event == 'ORDER_COMPLETED':
                found = mark_payment_paid(order_id)
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
    """Receives Wise's 'Account deposit events' (balances#update) webhook - registered manually via
    the Wise account UI, not the API, so there's no signing secret to load from settings the way the
    Revolut routes have. Interim/bootstrap version: NOT SIGNATURE-VERIFIED YET (Wise verifies via
    RSA-SHA256 against their published public key, not a per-subscription secret - the key itself
    still needs pinning down) and doesn't yet look anything up or mark anything paid - it only logs
    what arrives so a real event's exact shape can be inspected. Do not wire this to
    postgres_bookings.py-style payment confirmation until signature verification is added; until
    then this endpoint must not be trusted to represent a real, unforged payment notification.
    """
    is_test = request.headers.get('X-Test-Notification', '').lower() == 'true'
    try:
        data = json.loads(request.data)
        print(f"[wise webhook] test={is_test} event_type={data.get('event_type')} data={data.get('data')}", flush=True)
    except Exception as e:
        print(f"[wise webhook] failed to parse body: {e} - raw: {request.data.decode('utf-8', errors='replace')}", flush=True)

    return {"status": "ok"}, 200


def _contact_self_for_error(e: str, data: str, headers: dict) -> None:
    contact_self(
        subject=f"Error occurred: {e}",
        body=f"Error: {e}\nData: {data}\nHeaders: {headers}",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)