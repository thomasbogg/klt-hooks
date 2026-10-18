"""Writes owner-payout transfer state directly into klt-web's shared Postgres database - the
Revolut Business API sibling of postgres_bookings.py (guest deposit payments). Same conventions:
plain psycopg3 connections, no ORM, no @pull_database (that's the legacy SQLite/Google-Drive sync
path only, see postgres_bookings.py's own docstring for why).

Schema is owned by klt-web's Django migrations (finance/models.py::PayoutRecord,
finance/migrations/0007_payoutrecord_revolut_fields.py; and, since 2026-10-18, finance/models.py::
MonthEndTransfer - a month-end settlement paid through Revolut, one row per currency sent - whose
table finance_month_end_transfers is tried when no per-booking payout matches the transfer id). This module has no migration-time safety
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


# The tables a Revolut Business transfer of ours can be recorded in, tried in this order: a
# per-booking payout, then a month-end settlement (klt-web, 2026-10-18).
TRANSFER_TABLES = ('finance_payout_records', 'finance_month_end_transfers')


def _update_transfer(transfer_id: str, assignments: str) -> bool:
    """Applies `assignments` to the row recording this transfer in whichever of TRANSFER_TABLES
    holds it. True when one did."""
    with _connect() as conn:
        with conn.cursor() as cur:
            row = None
            for table in TRANSFER_TABLES:
                cur.execute(
                    f"UPDATE {table} SET {assignments} WHERE revolut_transfer_id = %s RETURNING id",
                    (transfer_id,),
                )
                row = cur.fetchone()
                if row is not None:
                    break
        conn.commit()
    return row is not None


def mark_transfer_paid(transfer_id: str) -> bool:
    """Transfer state reached 'completed' - funds have actually settled. Does not touch paid_at
    (that stays "when staff actioned this payout", set at creation time - see PayoutRecord's own
    docstring in klt-web). Returns False if no payout or month-end transfer matches transfer_id."""
    return _update_transfer(transfer_id, "status = 'paid', last_event_type = 'TransactionStateChanged'")


def mark_transfer_failed(transfer_id: str) -> bool:
    """Transfer state reached a terminal failure ('failed'/'declined'/'cancelled'). No automated
    retry path exists once this happens (matches bookings.models.Payment.status='failed' having
    none either) - a failed live transfer needs a manual out-of-band fix. Returns False if no
    payout or month-end transfer matches transfer_id."""
    return _update_transfer(
        transfer_id, "status = 'failed', last_event_type = 'TransactionStateChanged', failed_at = now()",
    )
