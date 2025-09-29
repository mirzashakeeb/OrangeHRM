import os
import logging
import pytest
import allure
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# Ensure logs folder exists
os.makedirs("reports/logs", exist_ok=True)

# Configure logging
logger = logging.getLogger("automation")
logger.setLevel(logging.INFO)

if not logger.handlers:  # Prevent duplicate handlers
    file_handler = logging.FileHandler("reports/logs/test.log")
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

# ---------------- WebDriver Fixture ----------------
@pytest.fixture
def driver():
    logger.info("Initializing WebDriver fixture")
    driver_instance = None
    try:
        driver_instance = DriverFactory.get_driver()
        yield driver_instance
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise
    finally:
        if driver_instance:
            driver_instance.quit()
            logger.info("WebDriver instance quit successfully")

# ---------------- Login Fixture ----------------
@pytest.fixture
def login(driver):
    """Logs in as Admin and returns DashboardPage"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    login_page.open_login_page()
    login_page.login("Admin", "admin123")
    assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load after login"
    return dashboard_page

# ---------------- Pytest Allure Hook ----------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results, screenshots, and logs into Allure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        driver = item.funcargs.get("driver", None)

        if rep.failed:
            logger.error(f"Test {item.name} FAILED")

            # Attach screenshot
            if driver:
                try:
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"{item.name}_failure",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    logger.error(f"Could not capture screenshot: {e}")

            # Attach log file
            try:
                with open("reports/logs/test.log", "r") as log_file:
                    allure.attach(
                        log_file.read(),
                        name=f"{item.name}_logs",
                        attachment_type=allure.attachment_type.TEXT
                    )
            except Exception as e:
                logger.error(f"Could not attach log file: {e}")

        elif rep.passed:
            logger.info(f"Test {item.name} PASSED")
