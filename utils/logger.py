import logging
import os
from datetime import datetime
import allure


def get_logger(name):
    # log file path
    log_dir = os.path.join(os.getcwd(), "reports", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # configure logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def log_to_allure(level, message):
    """
    Utility function to also send logs to Allure report.
    Example:
        log_to_allure("INFO", "Login successful")
    """
    try:
        allure.attach(
            message,
            name=f"Log - {level}",
            attachment_type=allure.attachment_type.TEXT
        )
    except Exception:
        # Fallback: if allure not active, just ignore
        pass
