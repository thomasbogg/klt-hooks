"""Writes booking-deposit payment state directly into klt-web's shared Postgres database.

Deliberately separate from default/database/ - that's the legacy SQLite framework (synced to/from
Google Drive via wrapper.py's @pull_database), which is a different, disconnected database from
this one. Do NOT decorate anything here with that machinery.

Schema is owned by klt-web's Django migrations (bookings/models.py) - this module has no
migration-time safety net against a future column rename there. If a webhook starts failing after
a klt-web schema change, check bookings/models.py::Booking/Payment first.
"""
import psycopg

from default.settings import (
    POSTGRES_DATABASE_HOST,
    POSTGRES_DATABASE_PORT,
    POSTGRES_DATABASE_NAME,
    POSTGRES_DATABASE_USER,
    POSTGRES_DATABASE_PASSWORD,
)

IN_PROGRESS_EVENTS = (
    'ORDER_PAYMENT_AUTHORISATION_STARTED',
    'ORDER_PAYMENT_AUTHENTICATION_CHALLENGED',
    'ORDER_PAYMENT_AUTHENTICATED',
)
FAILURE_STATUS_BY_EVENT = {
    'ORDER_PAYMENT_DECLINED': 'declined',
    'ORDER_PAYMENT_FAILED': 'failed',
    'ORDER_CANCELLED': 'cancelled',
}


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


def mark_payment_paid(order_id: str) -> bool:
    """Deposit paid in full - confirm the booking. Returns False if no Payment row matches order_id."""
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
                return False
            booking_id = row[0]

            cur.execute(
                """
                UPDATE bookings
                SET enquiry_status = 'Booking confirmed', last_updated = now()
                WHERE id = %s
                """,
                (booking_id,),
            )
        conn.commit()
    return True


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
