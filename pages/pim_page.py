import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class PIMPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # --- PIM Add Employee Page locators ---
        self.add_employee_btn = (By.XPATH, "//button[normalize-space()='Add']")
        self.first_name_input = (By.NAME, "firstName")
        self.last_name_input = (By.NAME, "lastName")

        # Toggle & login details (works ON and OFF)
        self.create_login_toggle = (By.XPATH, "//span[@class='oxd-switch-input oxd-switch-input--active --label-right']")
        self.user_name = (By.XPATH, "//input[@autocomplete='off' and not(@type) and contains(@class, 'oxd-input')]")
        self.create_password = (By.XPATH, "(//input[@type='password'])[1]")  # first password field
        self.confirm_password = (By.XPATH, "(//input[@type='password'])[2]")  # second password field

        self.save_btn = (By.XPATH, "//button[normalize-space()='Save']")

        self.employee_list =(By.XPATH,"//h6[text()='Personal Details']")

    @allure.step("Click Add Employee button")
    def click_add_employee(self):
        self.click(self.add_employee_btn)
        logger.info("Clicked Add Employee button")

    @allure.step("Enter First Name: {first_name}")
    def enter_first_name(self, first_name):
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.first_name_input)
        )
        self.type(self.first_name_input, first_name)

    @allure.step("Enter Last Name: {last_name}")
    def enter_last_name(self, last_name):
        self.type(self.last_name_input, last_name)

    @allure.step("Toggle Create Login Details and wait for fields")
    def toggle_create_login(self):
        # Click the toggle
        self.click(self.create_login_toggle)
        logger.info("Toggled Create Login Details")

        # Wait until username field is visible
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.user_name)
        )
        logger.info("Login details fields are visible now")

    @allure.step("Enter Username: {username}")
    def enter_username(self, username):
        self.type(self.user_name, username)

    @allure.step("Enter Password")
    def enter_password(self, password):
        self.type(self.create_password, password)

    @allure.step("Confirm Password")
    def enter_confirm_password(self, confirm_password):
        self.type(self.confirm_password, confirm_password)

    @allure.step("Click Save button")
    def click_save(self):
        self.click(self.save_btn)
        logger.info("Clicked Save button")

    @allure.step("Wait for Personal Details page")
    def wait_for_employee_list(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.employee_list)
        )
        logger.info("Personal Details page is visible")
