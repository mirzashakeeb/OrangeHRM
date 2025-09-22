import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username = (By.NAME, "username")
        self.password = (By.NAME, "password")
        self.login_btn = (By.XPATH, "//button[@type='submit']")
        self.error_msg = (By.XPATH, "//p[@class='oxd-alert-content-text']")
        self.dashboard_header = (By.XPATH, "//h6[text()='Dashboard']")

    @allure.step("Open OrangeHRM login page")
    def open_login_page(self):
        self.open_url("https://opensource-demo.orangehrmlive.com/")

    @allure.step("Login with username: {1} and password: {2}")
    def login(self, user, pwd):
        self.type(self.username, user)
        self.type(self.password, pwd)
        self.click(self.login_btn)

        # Success case
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.dashboard_header)
            )
            logger.info("Login successful – Dashboard loaded")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="dashboard_loaded",
                          attachment_type=allure.attachment_type.PNG)
            return "success"
        except TimeoutException:
            logger.warning("Dashboard not found, checking error message")

        # Failure case
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.error_msg)
            )
            logger.error("Login failed – Error message displayed")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="login_error",
                          attachment_type=allure.attachment_type.PNG)
            return "failure"
        except TimeoutException:
            logger.error("Login failed – Neither dashboard nor error message appeared")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="login_unknown_failure",
                          attachment_type=allure.attachment_type.PNG)
            return "failure"

    @allure.step("Verify if login page is displayed")
    def is_login_page_displayed(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.login_btn)
            )
            logger.info("Login page is displayed")
            return True
        except TimeoutException:
            logger.error("Login page not displayed")
            return False
