"""
init_all_applications.py
==========================
Python equivalent of UiPath's InitAllApplications.xaml.
Open browsers, connect to DBs/APIs, log into applications, etc.
Raise SystemException on failure so the framework exits cleanly
during Init rather than failing mid-run.
"""

import logging

from framework.exceptions import SystemException


def init_all_applications(config, logger: logging.Logger):
    """
    Replace the body of this function with real app/connection setup,
    e.g.:
        driver = webdriver.Chrome()
        driver.get(config.get("TargetUrl"))
        return {"driver": driver}
    """
    try:
        logger.info("Opening applications / connections...")
        resources = {}  # e.g. {"driver": driver, "db_conn": conn}
        return resources
    except Exception as exc:
        raise SystemException(f"Failed to initialize applications: {exc}")
