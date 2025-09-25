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
        self.timeout = 10  # Default wait

        # --- Add Employee Locators ---
        self.add_employee_btn = (By.XPATH, "//button[normalize-space()='Add']")
        self.first_name_input = (By.NAME, "firstName")
        self.last_name_input = (By.NAME, "lastName")
        self.create_login_toggle = (By.XPATH, "//span[@class='oxd-switch-input oxd-switch-input--active --label-right']")
        self.user_name_input = (By.XPATH, "//input[@autocomplete='off' and not(@type) and contains(@class, 'oxd-input')]")
        self.password_input = (By.XPATH, "(//input[@type='password'])[1]")
        self.confirm_password_input = (By.XPATH, "(//input[@type='password'])[2]")
        self.save_btn = (By.XPATH, "//button[normalize-space()='Save']")
        self.employee_list_header = (By.XPATH, "//h6[text()='Personal Details']")

        # --- Edit Employee Locators ---
        self.employee_table = (By.XPATH, "//div[@class='oxd-table-body']")
        self.edit_button = (By.XPATH, "//button[normalize-space()='Edit']")
        self.job_title_input = (By.XPATH, "//input[@name='jobTitle']")  # Example editable field

    # ---------------- Add Employee Methods ----------------
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

    @allure.step("Toggle Create Login Details")
    def toggle_create_login(self):
        self.click(self.create_login_toggle)
        logger.info("Toggled Create Login Details")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.user_name_input)
        )

    @allure.step("Enter Username: {username}")
    def enter_username(self, username):
        self.type(self.user_name_input, username)

    @allure.step("Enter Password")
    def enter_password(self, password):
        self.type(self.password_input, password)

    @allure.step("Confirm Password")
    def enter_confirm_password(self, confirm_password):
        self.type(self.confirm_password_input, confirm_password)

    # ---------------- Edit Employee Methods ----------------
    # Inside PIMPage class

    @allure.step("Search employee by name: {employee_name}")
    def search_employee(self, employee_name):
        search_input = (By.XPATH, "//input[@placeholder='Type for hints...'][1]")  # Replace with actual locator
        search_button = (By.XPATH, "//button[@type='submit']")  # Replace with actual locator

        self.type(search_input, employee_name)
        self.click(search_button)
        logger.info(f"Searched for employee: {employee_name}")

    @allure.step("Click Edit button for employee: {employee_name} and wait for form")
    def click_edit_employee(self, employee_name):
        # Locate the Edit button (adjust XPath if needed)
        edit_btn = (By.XPATH, "//button[@class='oxd-icon-button oxd-table-cell-action-space'][1]")
        self.click(edit_btn)
        logger.info(f"Clicked Edit button for: {employee_name}")

        # Wait until a key field in the edit form is visible (e.g., Job Title)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.job_title_input)
        )
        logger.info("Employee Edit form is loaded and ready")

    # ---------------- Common Methods ----------------
    @allure.step("Click Save button")
    def click_save(self):
        self.click(self.save_btn)
        logger.info("Clicked Save button")

