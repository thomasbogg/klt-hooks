"""Writes booking-deposit and booking-balance payment state directly into klt-web's shared
Postgres database.

Deliberately separate from default/database/ - that's the legacy SQLite framework (synced to/from
Google Drive via wrapper.py's @pull_database), which is a different, disconnected database from
this one. Do NOT decorate anything here with that machinery.

Schema is owned by klt-web's Django migrations (bookings/models.py) - this module has no
migration-time safety net against a future column rename there. If a webhook starts failing after
a klt-web schema change, check bookings/models.py::Booking/Payment/BalancePayment first.
"""
from datetime import timedelta

import psycopg

from default.settings import (
    POSTGRES_DATABASE_HOST,
    POSTGRES_DATABASE_PORT,
    POSTGRES_DATABASE_NAME,
    POSTGRES_DATABASE_USER,
    POSTGRES_DATABASE_PASSWORD,
)

# ORDER_PAYMENT_AUTHENTICATED is deliberately NOT here - it gets its own handling (see
# mark_payment_authenticated below), since it's the point a Revolut bank-transfer payment can go
# quiet for up to 2 business days before ORDER_COMPLETED, unlike these two which just mean "guest
# still clicking through checkout".
IN_PROGRESS_EVENTS = (
    'ORDER_PAYMENT_AUTHORISATION_STARTED',
    'ORDER_PAYMENT_AUTHENTICATION_CHALLENGED',
)
FAILURE_STATUS_BY_EVENT = {
    'ORDER_PAYMENT_DECLINED': 'declined',
    'ORDER_PAYMENT_FAILED': 'failed',
    'ORDER_CANCELLED': 'cancelled',
}

# Booking status literals duplicated from klt-web's env_settings.py (VALID_BOOKING_STATUSES,
# PROVISIONAL_BOOKING_STATUSES) - this module can't import klt-web's Django code (separate
# deployables, see module docstring above). Keep in sync if either tuple changes there. Lists, not
# tuples: psycopg3 (unlike psycopg2) doesn't expand a tuple parameter into an IN-list - these are
# passed to = ANY(%s) instead, which needs a list/array.
_BLOCKING_VALID_STATUSES = ['Booking confirmed', 'Guests have departed', 'Guests on-site', 'Holiday completed']
_BLOCKING_PROVISIONAL_STATUSES = ['Provisional booking', 'Dates agreed and held', 'Awaiting payment']


def _add_business_days(start, business_days):
    """Mirrors bookings/utils.py::add_business_days() in klt-web - keep them in sync if that
    changes. Duplicated rather than imported: this module can't import klt-web's Django code."""
    current = start
    added = 0
    while added < business_days:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday-Friday
            added += 1
    return current


def _connect():
    return psycopg.connect(
        host=POSTGRES_DATABASE_HOST,
        port=POSTGRES_DATABASE_PORT,
        dbname=POSTGRES_DATABASE_NAME,
        user=POSTGRES_DATABASE_USER,
        password=POSTGRES_DATABASE_PASSWORD,
    )


def mark_payment_in_progress(order_id: str, event_type: str) -> bool:
    """Payment attempt detected but not yet resolved - extend the calendar hold rather than let it
    lapse mid-payment. Returns False if no Payment row matches order_id (nothing to update)."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE booking_payments
                SET status = 'in_progress', last_event_type = %s, in_progress_at = now()
                WHERE revolut_order_id = %s
                RETURNING booking_id
                """,
                (event_type, order_id),
            )
            row = cur.fetchone()
            if row is None:
                return False
            booking_id = row[0]

            cur.execute(
                """
                UPDATE bookings
                SET hold_expires_at = now() + (
                    SELECT (revolut_hold_extension_minutes || ' minutes')::interval
                    FROM booking_settings WHERE id = 1
                )
                WHERE id = %s
                """,
                (booking_id,),
            )
        conn.commit()
    return True


def mark_payment_authenticated(order_id: str) -> bool:
    """ORDER_PAYMENT_AUTHENTICATED: the guest approved payment at their own bank. Card payments
    settle in seconds from here (ORDER_COMPLETED will already have fired or fires imminently);
    Open Banking bank transfers can take up to 2 business days to clear. Since Revolut doesn't
    expose which payment method was used, swap the hold to the full payment-clearing window rather
    than the short flat extension used for the pre-authentication events - see bookings/utils.py's
    payment_clearing_expiry() in klt-web for the equivalent Wise-path logic. Returns False if no
    Payment row matches order_id."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE booking_payments
                SET status = 'in_progress', last_event_type = 'ORDER_PAYMENT_AUTHENTICATED', in_progress_at = now()
                WHERE revolut_order_id = %s
                RETURNING booking_id, in_progress_at
                """,
                (order_id,),
            )
            row = cur.fetchone()
            if row is None:
                return False
            booking_id, in_progress_at = row

            cur.execute("SELECT payment_clearing_business_days FROM booking_settings WHERE id = 1")
            (business_days,) = cur.fetchone()
            new_hold_expiry = _add_business_days(in_progress_at, business_days)

            cur.execute(
                "UPDATE bookings SET hold_expires_at = %s WHERE id = %s",
                (new_hold_expiry, booking_id),
            )
        conn.commit()
    return True


def mark_payment_paid(order_id: str) -> str:
    """Deposit paid in full. Confirms the booking unless its dates now conflict with another
    booking that currently holds the calendar (e.g. this hold expired and someone else's booking
    legitimately took the dates before this late ORDER_COMPLETED arrived) - in that case the
    payment is still recorded as paid (the money is real), but the booking is flipped to a
    non-blocking 'needs review' status instead of 'Booking confirmed', and the caller is expected
    to alert a human (see main.py). Returns 'not_found', 'confirmed', or 'conflict'."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE booking_payments
                SET status = 'paid', last_event_type = 'ORDER_COMPLETED', paid_at = now()
                WHERE revolut_order_id = %s
                RETURNING booking_id
                """,
                (order_id,),
            )
            row = cur.fetchone()
            if row is None:
                return 'not_found'
            booking_id = row[0]

            cur.execute(
                "SELECT property_id, arrival_date, departure_date FROM bookings WHERE id = %s",
                (booking_id,),
            )
            property_id, arrival_date, departure_date = cur.fetchone()

            # Mirrors BookingQuerySet.holding()/overlapping() in klt-web's bookings/models.py.
            cur.execute(
                """
                SELECT 1 FROM bookings
                WHERE property_id = %s
                  AND id != %s
                  AND arrival_date < %s
                  AND departure_date > %s
                  AND (
                    enquiry_status = ANY(%s)
                    OR (enquiry_status = ANY(%s) AND hold_expires_at IS NULL)
                    OR (enquiry_status = ANY(%s) AND hold_expires_at > now())
                  )
                LIMIT 1
                """,
                (
                    property_id, booking_id, departure_date, arrival_date,
                    _BLOCKING_VALID_STATUSES, _BLOCKING_PROVISIONAL_STATUSES, _BLOCKING_PROVISIONAL_STATUSES,
                ),
            )
            conflict = cur.fetchone() is not None

            status = 'Payment received - needs review' if conflict else 'Booking confirmed'
            cur.execute(
                "UPDATE bookings SET enquiry_status = %s, last_updated = now() WHERE id = %s",
                (status, booking_id),
            )
        conn.commit()
    return 'conflict' if conflict else 'confirmed'


def mark_payment_failed(order_id: str, event_type: str) -> bool:
    """Payment explicitly declined/failed/cancelled - release the hold now rather than waiting out
    the timer, and record a status distinct from 'Awaiting payment' for admin visibility. Returns
    False if no Payment row matches order_id."""
    status = FAILURE_STATUS_BY_EVENT.get(event_type, 'failed')
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE booking_payments
                SET status = %s, last_event_type = %s, failed_at = now()
                WHERE revolut_order_id = %s
                RETURNING booking_id
                """,
                (status, event_type, order_id),
            )
            row = cur.fetchone()
            if row is None:
                return False
            booking_id = row[0]

            cur.execute(
                """
                UPDATE bookings
                SET enquiry_status = 'Payment failed', last_updated = now()
                WHERE id = %s
                """,
                (booking_id,),
            )
        conn.commit()
    return True


# --- Balance-payment mutators (booking_balance_payments, klt-web's BalancePayment model) -------
#
# Deliberately NOT a "try booking_payments, then fall back to booking_balance_payments" branch
# bolted onto the four functions above: the deposit stage's hold-extension/date-conflict logic
# exists because the deposit is what holds the calendar slot open. By the time a balance payment
# exists at all, the booking is already confirmed and the slot is already locked in - there's no
# hold to extend and no conflict to check, so these are deliberately simpler, standalone functions
# rather than reused/branched versions of the deposit ones. As of 2026-08-20 these are wired but
# unreachable in production - see main.py's revolut_booking_deposit_callback(), whose route-level
# guard returns before any dispatch code (deposit or balance) ever runs.

def mark_balance_payment_in_progress(order_id: str, event_type: str) -> bool:
    """Covers IN_PROGRESS_EVENTS and ORDER_PAYMENT_AUTHENTICATED alike - unlike the deposit
    version, there's no hold to extend either way, so both collapse to the same simple status
    update. Returns False if no BalancePayment row matches order_id."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE booking_balance_payments
                SET status = 'in_progress', last_event_type = %s, in_progress_at = now()
                WHERE revolut_order_id = %s
                RETURNING booking_id
                """,
                (event_type, order_id),
            )
            found = cur.fetchone() is not None
        conn.commit()
    return found


def mark_balance_payment_paid(order_id: str) -> bool:
    """Balance paid in full. No conflict check and no enquiry_status change - the booking is
    already 'Booking confirmed' from the deposit stage, and there's no separate status literal for
    "balance also paid" in klt-web's env_settings.VALID_BOOKING_STATUSES to set it to. Returns
    False if no BalancePayment row matches order_id."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE booking_balance_payments
                SET status = 'paid', last_event_type = 'ORDER_COMPLETED', paid_at = now()
                WHERE revolut_order_id = %s
                RETURNING booking_id
                """,
                (order_id,),
            )
            found = cur.fetchone() is not None
        conn.commit()
    return found


def mark_balance_payment_failed(order_id: str, event_type: str) -> bool:
    """Balance payment explicitly declined/failed/cancelled - just record it, since there's no
    hold to release and the booking's own enquiry_status stays 'Booking confirmed' either way (the
    guest can simply retry). Returns False if no BalancePayment row matches order_id."""
    status = FAILURE_STATUS_BY_EVENT.get(event_type, 'failed')
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE booking_balance_payments
                SET status = %s, last_event_type = %s, failed_at = now()
                WHERE revolut_order_id = %s
                RETURNING booking_id
                """,
                (status, event_type, order_id),
            )
            found = cur.fetchone() is not None
        conn.commit()
    return found
