"""
Main.py
=======
Python equivalent of UiPath REFramework's Main.xaml.
Orchestrates the full state machine:

    INIT -> GET TRANSACTION DATA -> PROCESS TRANSACTION (loop) -> END PROCESS

Run with:
    python Main.py
"""

import sys

from framework.init_all_settings import init_all_settings
from framework.init_all_applications import init_all_applications
from framework.get_transaction_data import TransactionDataSource, get_transaction_data
from framework.set_transaction_status import process_with_retries
from framework.close_all_applications import close_all_applications
from framework.exceptions import SystemException


# Sample "queue" data — replace with Orchestrator Queue / DB / CSV read.
SAMPLE_TRANSACTIONS = [
    {"id": "INV-001", "amount": 250.0},
    {"id": "INV-002", "amount": -10.0},    # -> Business Exception
    {"id": "INV-003", "amount": 999999},   # -> System Exception (simulated, retried)
    {"id": "INV-004", "amount": 75.5},
]


def main():
    stats = {
        "processed": 0,
        "success": 0,
        "business_exceptions": 0,
        "system_exceptions": 0,
        "failed": 0,
    }

    # ---------------- INIT ----------------
    try:
        config, logger = init_all_settings(config_path="Data/config.json")
        logger.info("=== INIT: starting initialization ===")
        resources = init_all_applications(config, logger)
    except SystemException as exc:
        print(f"FATAL: Initialization failed: {exc}")
        sys.exit(1)

    # ---------------- MAIN LOOP ----------------
    logger.info("=== MAIN LOOP: Get Transaction Data -> Process Transaction ===")
    source = TransactionDataSource(SAMPLE_TRANSACTIONS)

    try:
        while True:
            transaction = get_transaction_data(source, logger)
            if transaction is None:
                break

            process_with_retries(transaction, config, logger, resources, stats)
            stats["processed"] += 1

    finally:
        # ---------------- END PROCESS ----------------
        logger.info("=== END PROCESS: cleaning up ===")
        close_all_applications(resources, logger)

        logger.info("=== EXECUTION SUMMARY ===")
        for key, value in stats.items():
            logger.info(f"{key.replace('_', ' ').title()}: {value}")


if __name__ == "__main__":
    main()
