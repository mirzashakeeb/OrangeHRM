import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class DashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators
        self.dashboard_header = (By.XPATH, "//h6[text()='Dashboard']")
        self.pim_module = (By.XPATH, "//span[text()='PIM']")
        self.leave_module = (By.XPATH, "//span[text()='Leave']")
        self.recruitment_module = (By.XPATH, "//span[text()='Recruitment']")
        self.assign_leave = (By.XPATH, "//button[@title='Assign Leave']")
        self.leave_list = (By.XPATH, "//button[@title='Leave List']")
        self.time_sheets = (By.XPATH, "//button[@title='Timesheets']")
        self.apply_leave = (By.XPATH, "//button[@title='Apply Leave']")
        # Logout locators
        self.user_dropdown = (By.CLASS_NAME,"oxd-userdropdown-img")
        self.logout_link = (By.XPATH, "//a[text()='Logout']")

    @allure.step("Validate Dashboard is loaded")
    def is_dashboard_loaded(self):
        """Check if Dashboard page is visible"""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.dashboard_header)
            )
            logger.info("Dashboard is loaded")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="dashboard_loaded",
                          attachment_type=allure.attachment_type.PNG)
            return True
        except TimeoutException:
            logger.error("Dashboard not loaded")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="dashboard_not_loaded",
                          attachment_type=allure.attachment_type.PNG)
            return False

    @allure.step("Navigate to PIM Module")
    def go_to_pim(self):
        self.click(self.pim_module)
        logger.info("Navigated to PIM Module")

    @allure.step("Navigate to Leave Module")
    def go_to_leave(self):
        self.click(self.leave_module)
        logger.info("Navigated to Leave Module")

    @allure.step("Navigate to Recruitment Module")
    def go_to_recruitment(self):
        self.click(self.recruitment_module)
        logger.info("Navigated to Recruitment Module")

    @allure.step("Click Assign Leave in Quick Launch")
    def click_assign_leave(self):
        self.click(self.assign_leave)
        logger.info("Clicked Assign Leave from Quick Launch")

    @allure.step("Click Leave List in Quick Launch")
    def click_leave_list(self):
        self.click(self.leave_list)
        logger.info("Clicked Leave List from Quick Launch")

    @allure.step("Click time sheets in Quick Launch")
    def click_time_sheets(self):
        self.click(self.time_sheets)
        logger.info("Clicked time sheets from Quick Launch")

    @allure.step("Click Apply Leave from Quick Launch")
    def click_apply_leave(self):
        self.click(self.apply_leave)
        logger.info("Clicked Apply Leave from Quick Launch")

    @allure.step("Perform Logout")
    def logout(self):
        """Click user dropdown → Logout"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.user_dropdown)
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.logout_link)
            ).click()

            logger.info("Logout successful")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="logout_success",
                          attachment_type=allure.attachment_type.PNG)
        except TimeoutException:
            logger.error("Logout failed – elements not found")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="logout_failure",
                          attachment_type=allure.attachment_type.PNG)
            raise
