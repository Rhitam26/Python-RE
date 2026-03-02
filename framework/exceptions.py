"""
exceptions.py
=============
Python equivalent of UiPath's BusinessRuleException / SystemException model.

- BusinessException: expected, rule-based failure (bad data, validation failure).
  -> Transaction is marked "Business Rule Exception", logged, and skipped
     WITHOUT retry (matches UiPath behavior exactly).

- SystemException: unexpected/technical failure (app crash, timeout, element
  not found, connection lost).
  -> Transaction is retried up to Config["MaxRetryNumber"] times before
     being marked "System Exception" and moved on.
"""


class BusinessException(Exception):
    """
    Raise this for business-rule violations, e.g.:
        raise BusinessException("Invoice amount cannot be negative")
    Never retried. Recorded in Exceptions/Business.
    """

    def __init__(self, message: str, details: str = ""):
        self.message = message
        self.details = details
        super().__init__(message)


class SystemException(Exception):
    """
    Raise this for technical/unexpected failures, e.g.:
        raise SystemException("Timeout calling invoicing API")
    Retried up to MaxRetryNumber. Recorded in Exceptions/System if
    retries are exhausted.
    """

    def __init__(self, message: str, details: str = ""):
        self.message = message
        self.details = details
        super().__init__(message)
