"""
config.py
=========
Python equivalent of UiPath's Data/Config.xlsx.
Loads all settings from Data/config.json (or config.yaml) into a dict-like
object, the same way Config.xlsx's "Settings" sheet is read into a
Dictionary<string, object> in UiPath.
"""

import json
import os
from typing import Any, Optional


class Config:
    DEFAULTS = {
        "MaxRetryNumber": 3,
        "RetryDelaySeconds": 2,
        "LogFile": "Logs/execution.log",
        "LogLevel": "INFO",
        "OrchestratorQueueName": "",
        "TransactionsFolder": "Data/Transactions",
        "OutputFolder": "Data/Output",
        "BusinessExceptionsFolder": "Exceptions/Business",
        "SystemExceptionsFolder": "Exceptions/System",
    }

    def __init__(self, config_path: Optional[str] = None):
        self.settings = dict(self.DEFAULTS)
        if config_path is None:
            config_path = os.path.join("Data", "config.json")
        if os.path.exists(config_path):
            self._load(config_path)

    def _load(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            if path.endswith(".json"):
                loaded = json.load(f)
            else:
                try:
                    import yaml
                    loaded = yaml.safe_load(f)
                except ImportError:
                    raise RuntimeError(
                        "PyYAML not installed. Run `pip install pyyaml` "
                        "or use a .json config file."
                    )
        self.settings.update(loaded or {})

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]
