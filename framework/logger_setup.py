"""
logger_setup.py
===============
Sets up structured logging to console + Logs/execution.log,
equivalent to UiPath's Orchestrator "Log Message" activities
writing to the Logs folder / Orchestrator logs.
"""

import logging
import os
import sys

from framework.config import Config


def setup_logger(config: Config) -> logging.Logger:
    logger = logging.getLogger("REFramework")
    level = getattr(logging, str(config.get("LogLevel", "INFO")).upper(), logging.INFO)
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_file = config.get("LogFile")
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
