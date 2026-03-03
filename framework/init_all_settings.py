"""
init_all_settings.py
=====================
Python equivalent of UiPath's InitAllSettings.xaml.
Loads Config, sets up logging, and validates required settings exist.
Raises SystemException if a required setting is missing (matches
UiPath behavior of failing fast on bad config).
"""

from framework.config import Config
from framework.exceptions import SystemException
from framework.logger_setup import setup_logger


REQUIRED_SETTINGS = ["MaxRetryNumber", "RetryDelaySeconds"]


def init_all_settings(config_path: str = None):
    config = Config(config_path)
    logger = setup_logger(config)

    for key in REQUIRED_SETTINGS:
        if config.get(key) is None:
            raise SystemException(f"Missing required config setting: {key}")

    logger.info("Config and logging initialized successfully.")
    return config, logger
