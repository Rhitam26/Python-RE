"""
process_transaction.py
========================
Python equivalent of UiPath's ProcessTransaction.xaml.
This is where the ACTUAL business logic for one transaction lives.

Raise BusinessException for expected/rule-based failures (bad data,
validation errors) -> not retried.

Raise SystemException for unexpected/technical failures (timeouts,
app crashes, element not found) -> retried by the framework.
"""

import logging

from framework.exceptions import BusinessException, SystemException
from framework.get_transaction_data import TransactionItem


def process_transaction(transaction: TransactionItem, config, logger: logging.Logger,
                         resources: dict) -> None:
    """
    Replace this body with your real per-transaction automation logic.
    `resources` is whatever init_all_applications() returned
    (browser driver, DB connection, etc.)
    """
    invoice = transaction.data

    # ---- Example business-rule validation ----
    if invoice.get("amount", 0) < 0:
        raise BusinessException(
            f"Invoice {invoice.get('id')} has a negative amount: {invoice.get('amount')}"
        )

    # ---- Example simulated technical failure ----
    if invoice.get("amount", 0) > 100000:
        raise SystemException(
            f"Timeout calling invoicing API for {invoice.get('id')}"
        )

    # ---- Example successful processing ----
    logger.info(f"Invoice {invoice.get('id')} processed: ${invoice.get('amount'):.2f}")
