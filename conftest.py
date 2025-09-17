import logging
import pytest
import allure
from utils.driver_factory import DriverFactory

# Configure logging only once
logger = logging.getLogger("automation")
logger.setLevel(logging.INFO)

if not logger.handlers:  #Prevent duplicate handlers
    file_handler = logging.FileHandler("reports/logs/test.log")
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


@pytest.fixture
def driver():
    logger.info("Initializing WebDriver")
    driver = DriverFactory.get_driver()
    yield driver
    logger.info("Quitting WebDriver")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results, screenshots, and logs into Allure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        driver = item.funcargs.get("driver", None)  # get driver if fixture is used

        if rep.failed:
            logger.error(f"Test {item.name} FAILED")

            # Attach screenshot if driver exists
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
