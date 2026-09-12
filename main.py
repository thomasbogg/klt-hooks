from datetime import datetime, timedelta, timezone

from flask import Flask, request
from markupsafe import escape
import json
import os
from revolut import process_revolut_merchant_callback, verify_revolut_payload_signature
from default.settings import (
    REVOLUT_MERCHANT_API_SIGNING_KEY, REVOLUT_BOOKING_DEPOSIT_WEBHOOK_SIGNING_KEY,
    REVOLUT_BUSINESS_TRANSFER_WEBHOOK_SIGNING_KEY, WISE_WEBHOOK_PUBLIC_KEY,
    SAGE_CLIENT_ID, SAGE_CLIENT_SECRET, KLT_WEBHOOK_URL,
)
from correspondence.self.functions import contact_self
from postgres_bookings import (
    IN_PROGRESS_EVENTS, FAILURE_STATUS_BY_EVENT, mark_payment_in_progress, mark_payment_authenticated,
    mark_payment_paid, mark_payment_failed, mark_balance_payment_in_progress, mark_balance_payment_paid,
    mark_balance_payment_failed, mark_tourist_tax_in_progress, mark_tourist_tax_paid, mark_tourist_tax_failed,
    mark_supplementary_payment_in_progress, mark_supplementary_payment_authenticated,
    mark_supplementary_payment_paid, mark_supplementary_payment_failed, mark_sage_connected,
)
from postgres_business_payouts import mark_transfer_paid, mark_transfer_failed
from sage_oauth import exchange_code_for_tokens
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
    """Deposit, balance, tourist-tax, AND supplementary-payment events for klt-web bookings (own
    signing key, own event list, separate from the tourist-tax route above) - writes into klt-web's
    shared Postgres tables via postgres_bookings.py, not the legacy SQLite layer default/database/
    uses. See bookings/models.py::Payment/BalancePayment/TouristTax/SupplementaryPayment in
    klt-web.

    SUSPENDED as of 2026-08-20 (the bare 204 below) - Revolut delivers every event to every
    registered webhook on the account regardless of which one "owns" it, so this route was seeing
    the legacy tourist-tax route's own callbacks too and alerting on them as unrecognised. Stays
    off until the tourist-tax route is retired (it's on the old system klt-web is replacing, not
    this one) - re-enabling before then just reintroduces the same false-alert noise. klt-web
    itself isn't publicly deployed yet either (see reference_klt_web_dev_env in memory), so real
    guests are still on the old system for tourist-tax collection regardless - retiring the legacy
    route is a later, separate decision tied to deployment, not part of adding klt-web's own
    tourist-tax feature (2026-08-30) or its later supplementary-payment one (2026-09). The dispatch
    below (deposit first, balance next, tourist tax next, supplementary payment last as a further
    fallback) is otherwise ready to go once that's resolved. Note supplementary_payment's 'paid'
    branch only flips status - applying the staged date-change/guest-add is real Django ORM logic
    this module can't run, see postgres_bookings.py's own section header comment for that trio."""
    return ('', 204)
    try:
        if verify_revolut_payload_signature(request.headers, request.data, REVOLUT_BOOKING_DEPOSIT_WEBHOOK_SIGNING_KEY):
            data = json.loads(request.data)
            event = data['event']
            order_id = data['order_id']

            if event in IN_PROGRESS_EVENTS or event == 'ORDER_PAYMENT_AUTHENTICATED':
                if event in IN_PROGRESS_EVENTS:
                    found = mark_payment_in_progress(order_id, event)
                else:
                    found = mark_payment_authenticated(order_id)
                if not found:
                    found = mark_balance_payment_in_progress(order_id, event)
                if not found:
                    found = mark_tourist_tax_in_progress(order_id, event)
                if not found:
                    # Unlike the balance/tourist-tax fallbacks above, this one keeps the deposit's
                    # own in-progress/authenticated split (see mark_supplementary_payment_
                    # authenticated()'s own docstring) - a kind='date_change' row holds real
                    # calendar dates the same way the deposit's own booking does, so it deserves
                    # the same fidelity; balance/tourist-tax don't hold any dates at all by this
                    # stage, so a flat extension has always been enough for them.
                    if event in IN_PROGRESS_EVENTS:
                        found = mark_supplementary_payment_in_progress(order_id, event)
                    else:
                        found = mark_supplementary_payment_authenticated(order_id)
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
                elif not found:
                    found = mark_balance_payment_paid(order_id)
                    if not found:
                        found = mark_tourist_tax_paid(order_id)
                    if not found:
                        found = mark_supplementary_payment_paid(order_id)
            elif event in FAILURE_STATUS_BY_EVENT:
                found = mark_payment_failed(order_id, event)
                if not found:
                    found = mark_balance_payment_failed(order_id, event)
                if not found:
                    found = mark_tourist_tax_failed(order_id, event)
                if not found:
                    found = mark_supplementary_payment_failed(order_id, event)
            else:
                _contact_self_for_error(f"Received unexpected event type: {event}", request.data.decode('utf-8'), dict(request.headers))
                found = True

            if not found:
                _contact_self_for_error(f"No booking payment found for order_id: {order_id}", request.data.decode('utf-8'), dict(request.headers))

    except Exception as e:
        _contact_self_for_error(str(e), request.data.decode('utf-8'), dict(request.headers))

    return ('', 204)


@app.route("/revolut/business-transfer-callback", methods=["POST"])
def revolut_business_transfer_callback():
    """Revolut Business API transfer-state webhook (owner payouts) - a separate
    product/subscription/signing key from both routes above, writing into klt-web's
    finance_payout_records via postgres_business_payouts.py rather than the booking_payments
    table. Deliberately not decorated with @pull_database, same reasoning as
    revolut_booking_deposit_callback above. Payload field names (transfer id/state) are a
    best-effort guess pending confirmation against Revolut's Business API docs during sandbox
    testing - adjust data.get(...) below if the real payload shape differs."""
    try:
        if verify_revolut_payload_signature(request.headers, request.data, REVOLUT_BUSINESS_TRANSFER_WEBHOOK_SIGNING_KEY):
            data = json.loads(request.data)
            transfer_id = data.get('transfer_id') or data.get('id')
            state = data.get('state') or data.get('event')

            if state == 'completed':
                found = mark_transfer_paid(transfer_id)
            elif state in ('failed', 'declined', 'cancelled'):
                found = mark_transfer_failed(transfer_id)
            else:
                found = True  # pending/created etc - nothing terminal to record yet

            if not found:
                _contact_self_for_error(
                    f"No payout record found for transfer_id: {transfer_id}",
                    request.data.decode('utf-8'), dict(request.headers),
                )

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


@app.route("/sage/oauth-callback", methods=["GET"])
def sage_oauth_callback():
    """Where klt-web's staff/views.py::StaffSageConnectView sends Sage's OAuth2 authorization
    redirect (2026-09-09, per Thomas). klt-web only ever runs as 127.0.0.1 on someone's own
    machine (see CLAUDE.md), never a real deployed URL - klt-hooks is the only piece of this
    system with a real, publicly-reachable HTTPS URL, so it's the redirect target instead, exactly
    the same "publicly reachable, writes into klt-web's Postgres" role it already plays for
    Revolut/Wise. Unlike those, this is a GET a human's own browser lands on directly (not a
    server-to-server webhook), so it renders a small confirmation page rather than returning a
    bare status code - Thomas is sitting there watching this happen.

    `state` is klt-web's own Settings page URL, round-tripped unchanged through Sage's redirect
    (StaffSageConnectView put it there) - used only as the "return to Settings" link on the
    confirmation page below, never trusted for anything else. Restricted to http(s) as basic
    open-redirect hygiene, though the practical risk is low - reaching this point at all already
    requires a genuine Sage authorization_code, which only exists after Thomas himself logs in and
    consents on Sage's own site."""
    state = request.args.get('state', '')
    return_url = state if state.startswith(('http://', 'https://')) else ''
    code = request.args.get('code')
    error = request.args.get('error')

    if error or not code:
        _contact_self_for_error(
            f"Sage OAuth callback error: {error or 'no code returned'}",
            request.query_string.decode(), dict(request.headers),
        )
        return _sage_result_page(f"Sage One connection failed: {error or 'no authorization code returned'}.", return_url)

    # Must exactly match the redirect_uri StaffSageConnectView used to build the authorize
    # request - Sage validates the two match, same as any standard OAuth2 implementation. Built
    # from KLT_WEBHOOK_URL (env var), NOT request.base_url/request.url - Railway terminates TLS at
    # its edge and forwards plain HTTP internally, so Flask's own idea of "this request's scheme"
    # can report http:// even though the public URL (and what StaffSageConnectView sent Sage) was
    # https://, silently breaking the exact-match check this endpoint has no Werkzeug ProxyFix
    # middleware to correct.
    redirect_uri = f'{KLT_WEBHOOK_URL}sage/oauth-callback'
    tokens = exchange_code_for_tokens(SAGE_CLIENT_ID, SAGE_CLIENT_SECRET, code, redirect_uri)
    if tokens is None:
        _contact_self_for_error(
            "Sage OAuth token exchange failed", request.query_string.decode(), dict(request.headers),
        )
        return _sage_result_page("Sage One connection failed: token exchange was rejected.", return_url)

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=tokens['expires_in'])
    mark_sage_connected(tokens['access_token'], tokens['refresh_token'], expires_at)
    return _sage_result_page("Sage One connected successfully.", return_url)


def _sage_result_page(message: str, return_url: str) -> str:
    link = f'<p><a href="{escape(return_url)}">Return to Settings</a></p>' if return_url else ''
    return f"<html><body><p>{escape(message)}</p>{link}</body></html>"


def _contact_self_for_error(e: str, data: str, headers: dict) -> None:
    contact_self(
        subject=f"Error occurred: {e}",
        body=f"Error: {e}\nData: {data}\nHeaders: {headers}",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)