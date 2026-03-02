"""
close_all_applications.py
============================
Python equivalent of UiPath's CloseAllApplications.xaml.
Cleans up resources opened in init_all_applications.py
(browser, DB connections, etc.), always run in a finally block.
"""

import logging


def close_all_applications(resources: dict, logger: logging.Logger):
    """
    Replace with real cleanup, e.g.:
        if resources.get("driver"):
            resources["driver"].quit()
        if resources.get("db_conn"):
            resources["db_conn"].close()
    """
    logger.info("Closing applications / releasing resources...")
    resources.clear()
