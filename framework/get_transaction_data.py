"""
get_transaction_data.py
=========================
Python equivalent of UiPath's GetTransactionData.xaml.
Fetches the next transaction item from a queue/list/DB/CSV.
Returns None when there is no more work (ends the main loop),
exactly like UiPath's "TransactionItem = Nothing" convention.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional


class TransactionStatus(Enum):
    SUCCESS = auto()
    BUSINESS_EXCEPTION = auto()
    SYSTEM_EXCEPTION = auto()
    FAILED = auto()


@dataclass
class TransactionItem:
    reference: str
    data: Any = None
    retry_count: int = 0
    status: Optional[TransactionStatus] = None
    error_message: str = ""


class TransactionDataSource:
    """
    Wraps whatever your real queue is (Orchestrator Queue, DB table,
    CSV file, list of dicts...). Swap the implementation of
    `get_next()` for your real source — everything else in the
    framework stays the same.
    """

    def __init__(self, items: list):
        self._items = items
        self._index = 0

    def get_next(self) -> Optional[TransactionItem]:
        if self._index >= len(self._items):
            return None
        raw = self._items[self._index]
        self._index += 1
        return TransactionItem(reference=str(raw.get("id", self._index)), data=raw)


def get_transaction_data(source: TransactionDataSource, logger) -> Optional[TransactionItem]:
    item = source.get_next()
    if item is None:
        logger.info("No more transaction items in queue.")
    else:
        logger.info(f"Retrieved transaction: {item.reference}")
    return item
