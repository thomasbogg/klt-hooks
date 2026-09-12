"""Writes owner-payout transfer state directly into klt-web's shared Postgres database - the
Revolut Business API sibling of postgres_bookings.py (guest deposit payments). Same conventions:
plain psycopg3 connections, no ORM, no @pull_database (that's the legacy SQLite/Google-Drive sync
path only, see postgres_bookings.py's own docstring for why).

Schema is owned by klt-web's Django migrations (finance/models.py::PayoutRecord,
finance/migrations/0007_payoutrecord_revolut_fields.py). This module has no migration-time safety
net against a future column rename there - if this starts failing after a klt-web schema change,
check finance/models.py::PayoutRecord first.
"""
import psycopg

from default.settings import (
    POSTGRES_DATABASE_HOST,
    POSTGRES_DATABASE_PORT,
    POSTGRES_DATABASE_NAME,
    POSTGRES_DATABASE_USER,
    POSTGRES_DATABASE_PASSWORD,
)


def _connect():
    return psycopg.connect(
        host=POSTGRES_DATABASE_HOST,
        port=POSTGRES_DATABASE_PORT,
        dbname=POSTGRES_DATABASE_NAME,
        user=POSTGRES_DATABASE_USER,
        password=POSTGRES_DATABASE_PASSWORD,
    )


def mark_transfer_paid(transfer_id: str) -> bool:
    """Transfer state reached 'completed' - funds have actually settled. Does not touch paid_at
    (that stays "when staff actioned this payout", set at PayoutRecord creation time - see that
    model's own docstring in klt-web). Returns False if no PayoutRecord matches transfer_id."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE finance_payout_records
                SET status = 'paid', last_event_type = 'TransferStateChanged'
                WHERE revolut_transfer_id = %s
                RETURNING id
                """,
                (transfer_id,),
            )
            row = cur.fetchone()
        conn.commit()
    return row is not None


def mark_transfer_failed(transfer_id: str) -> bool:
    """Transfer state reached a terminal failure ('failed'/'declined'/'cancelled'). No automated
    retry path exists once this happens (matches bookings.models.Payment.status='failed' having
    none either) - a failed live transfer needs a manual out-of-band fix. Returns False if no
    PayoutRecord matches transfer_id."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE finance_payout_records
                SET status = 'failed', last_event_type = 'TransferStateChanged', failed_at = now()
                WHERE revolut_transfer_id = %s
                RETURNING id
                """,
                (transfer_id,),
            )
            row = cur.fetchone()
        conn.commit()
    return row is not None
