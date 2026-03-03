"""
set_transaction_status.py
============================
Python equivalent of UiPath's SetTransactionStatus.xaml +
RetryCurrentTransaction.xaml combined.

Handles:
  - Marking transaction Success / Business Exception / System Exception
  - Retry loop for SystemException up to Config["MaxRetryNumber"]
  - Writing failed transactions out to Exceptions/Business or
    Exceptions/System (equivalent of UiPath's exception screenshots
    + "Add Queue Item" for failed items)
"""

import logging
import os
import time
import traceback

from framework.exceptions import BusinessException, SystemException
from framework.get_transaction_data import TransactionItem, TransactionStatus
from framework.process_transaction import process_transaction


def _write_exception_record(folder: str, transaction: TransactionItem, logger: logging.Logger):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{transaction.reference}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Reference: {transaction.reference}\n")
        f.write(f"Status: {transaction.status}\n")
        f.write(f"Retry count: {transaction.retry_count}\n")
        f.write(f"Error: {transaction.error_message}\n")
    logger.info(f"Exception record written to {path}")


def process_with_retries(transaction: TransactionItem, config, logger: logging.Logger,
                          resources: dict, stats: dict) -> None:
    max_retries = int(config.get("MaxRetryNumber", 3))
    retry_delay = float(config.get("RetryDelaySeconds", 2))

    while True:
        try:
            logger.info(f"Processing transaction: {transaction.reference}")
            process_transaction(transaction, config, logger, resources)

            transaction.status = TransactionStatus.SUCCESS
            stats["success"] += 1
            logger.info(f"Transaction {transaction.reference} succeeded.")
            return

        except BusinessException as exc:
            # Business exceptions are NEVER retried — matches UiPath exactly.
            transaction.status = TransactionStatus.BUSINESS_EXCEPTION
            transaction.error_message = str(exc)
            stats["business_exceptions"] += 1
            logger.warning(f"Business exception on {transaction.reference}: {exc}")
            _write_exception_record(
                config.get("BusinessExceptionsFolder", "Exceptions/Business"),
                transaction, logger
            )
            return

        except SystemException as exc:
            transaction.retry_count += 1
            transaction.error_message = str(exc)
            logger.error(
                f"System exception on {transaction.reference} "
                f"(attempt {transaction.retry_count}/{max_retries}): {exc}"
            )
            logger.debug(traceback.format_exc())

            if transaction.retry_count >= max_retries:
                transaction.status = TransactionStatus.SYSTEM_EXCEPTION
                stats["system_exceptions"] += 1
                logger.error(f"Max retries reached for {transaction.reference}.")
                _write_exception_record(
                    config.get("SystemExceptionsFolder", "Exceptions/System"),
                    transaction, logger
                )
                return
            else:
                time.sleep(retry_delay)
                continue  # retry same transaction

        except Exception as exc:
            # Unclassified/unexpected error — do not loop forever.
            transaction.status = TransactionStatus.FAILED
            transaction.error_message = str(exc)
            stats["failed"] += 1
            logger.critical(f"Unhandled exception on {transaction.reference}: {exc}")
            logger.debug(traceback.format_exc())
            _write_exception_record(
                config.get("SystemExceptionsFolder", "Exceptions/System"),
                transaction, logger
            )
            return
