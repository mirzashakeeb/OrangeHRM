import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ApplyLeavePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Locators
        self.leave_type_dropdown = (By.XPATH, "//label[text()='Leave Type']/following::div[@class='oxd-select-text-input'][1]")
        self.from_date_input = (By.XPATH, "//label[text()='From Date']/following::input[1]")
        self.to_date_input = (By.XPATH, "//label[text()='To Date']/following::input[1]")
        self.comments_input = (By.XPATH, "//textarea[@placeholder='Type here']")
        self.apply_button = (By.XPATH, "//button[normalize-space()='Apply']")

    @allure.step("Select leave type: {leave_type}")
    def select_leave_type(self, leave_type):
        self.select_dropdown(self.leave_type_dropdown, leave_type)

    @allure.step("Enter From Date: {from_date}")
    def enter_from_date(self, from_date):
        self.type(self.from_date_input, from_date)

    @allure.step("Enter To Date: {to_date}")
    def enter_to_date(self, to_date):
        self.type(self.to_date_input, to_date)

    @allure.step("Enter Comments: {comments}")
    def enter_comments(self, comments):
        self.type(self.comments_input, comments)

    @allure.step("Click Apply button")
    def click_apply(self):
        self.click(self.apply_button)
        logger.info("Clicked Apply button")
