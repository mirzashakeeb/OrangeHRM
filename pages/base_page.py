import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.logger import get_logger
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException

logger = get_logger(__name__)


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    @allure.step("Open URL: {1}")
    def open_url(self, url):
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    @allure.step("Get page title")
    def get_title(self):
        title = self.driver.title
        logger.info(f"Page title fetched: {title}")
        return title

    @allure.step("Find element: {1}")
    def find_element(self, locator):
        try:
            logger.info(f"Locating element: {locator}")
            return WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element not found: {locator}")

            # Attach screenshot to Allure on failure
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"{locator[1]}_not_found",
                attachment_type=allure.attachment_type.PNG
            )

            # Save screenshot locally as well
            screenshot_path = f"screenshots/{locator[1]}_not_found.png"
            self.driver.save_screenshot(screenshot_path)
            logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

    @allure.step("Type '{2}' into element: {1}")
    def type(self, locator, text):
        element = self.find_element(locator)
        safe_text = "********" if "password" in locator[1].lower() else text
        logger.info(f"Typing into element {locator}: {safe_text}")
        element.clear()
        element.send_keys(text)

    @allure.step("Click element: {1}")
    def click(self, locator):
        element = self.find_element(locator)
        logger.info(f"Clicking element: {locator}")
        element.click()

    @allure.step("Select option '{2}' from dropdown: {1}")
    def select_dropdown(self, locator, option_text):
        try:
            # Click dropdown field
            dropdown = self.find_element(locator)
            dropdown.click()
            logger.info(f"Opened dropdown: {locator}")

            # Retry in case of stale element
            option_locator = (By.XPATH, f"//div[@role='listbox']//span[text()='{option_text}']")
            option = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(option_locator)
            )

            try:
                option.click()
            except StaleElementReferenceException:
                logger.warning(f"Stale element when selecting '{option_text}', retrying...")
                option = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable(option_locator)
                )
                option.click()

            logger.info(f"Selected option: {option_text}")

        except TimeoutException:
            logger.error(f"Option '{option_text}' not found in dropdown {locator}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"dropdown_{locator[1]}_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    @allure.step("Check if element is visible: {locator}")
    def is_visible(self, locator):
        """Return True if element is visible within timeout, else False."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.find_element(*locator).is_displayed()
            )
            logger.info(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element not visible: {locator}")
            return False
        except StaleElementReferenceException:
            logger.warning(f"Stale element: {locator}")
            return False