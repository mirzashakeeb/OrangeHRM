import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import get_logger
import re

logger = get_logger(__name__)

class AdminPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # --- Admin Page locators ---
        self.admin_tab = (By.XPATH, "//span[text()='Admin']")
        self.username_field = (By.XPATH, "//label[text()='Username']/../following-sibling::div//input")
        self.user_role_dropdown = (By.XPATH, "//label[text()='User Role']/../following-sibling::div//div[contains(@class,'oxd-select-text-input')]")
        self.employee_name_field = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
        self.status_dropdown = (By.XPATH, "//label[text()='Status']/../following-sibling::div//div[contains(@class,'oxd-select-text-input')]")
        self.search_button = (By.XPATH, "//button[normalize-space()='Search']")
        self.reset_button = (By.XPATH, "//button[normalize-space()='Reset']")
        self.add_button = (By.XPATH, "//button[normalize-space()='Add']")
        self.delete_button = (By.XPATH, "//button[normalize-space()='Delete Selected']")

        # --- Add User form locators ---
        self.add_user_role = (By.XPATH, "//label[text()='User Role']/../following-sibling::div//div[contains(@class,'oxd-select-text-input')]")
        self.add_employee_name = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
        self.add_username = (By.XPATH, "//label[text()='Username']/../following-sibling::div//input")
        self.add_status = (By.XPATH, "//label[text()='Status']/../following-sibling::div//div[contains(@class,'oxd-select-text-input')]")
        self.add_password = (By.XPATH, "(//input[@type='password'])[1]")
        self.add_confirm_password = (By.XPATH, "(//input[@type='password'])[2]")
        self.save_button = (By.XPATH, "//button[normalize-space()='Save']")

        # --- Validation locators ---
        self.success_message = (By.XPATH, "//div[contains(@class,'oxd-toast--success')]")

    @allure.step("Open Admin Tab")
    def open_admin_tab(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.admin_tab)
        ).click()
        logger.info("Opened Admin Tab")

    @allure.step("Search user: {username}")
    def search_user(self, username="", role=None, emp_name="", status=None):
        if username:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.username_field)
            ).send_keys(username)
        if role:
            self.select_dropdown(self.user_role_dropdown, role)
        if emp_name:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.employee_name_field)
            ).send_keys(emp_name)
        if status:
            self.select_dropdown(self.status_dropdown, status)

        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.search_button)
        ).click()
        logger.info(f"Searched user with Username={username}, Role={role}, Employee={emp_name}, Status={status}")

    @allure.step("Reset search filters")
    def reset_search(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.reset_button)
        ).click()
        logger.info("Reset search filters")

    @allure.step("Click Add User button")
    def click_add_button(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.add_button)
        ).click()
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.add_username)
        )
        logger.info("Clicked Add button and Add User form loaded")

    @allure.step("Add new user: {username}")
    def add_new_user(self, role, emp_name, username, status, password):
        self.select_dropdown(self.add_user_role, role)

        # Employee Name input
        emp_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.add_employee_name)
        )
        emp_input.clear()
        emp_input.send_keys(emp_name)

        # Wait for suggestions container
        suggestion_container = (By.XPATH, "//div[@role='listbox']")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(suggestion_container)
        )

        # Normalize helper
        def normalize(text):
            return re.sub(r"\s+", " ", text.strip().lower())

        normalized_emp = normalize(emp_name)

        # Get all suggestions and select
        suggestions = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='listbox']//span"))
        )
        matched = False
        for sug in suggestions:
            normalized_sug = normalize(sug.text)
            if normalized_emp == normalized_sug or normalized_emp in normalized_sug:
                self.driver.execute_script("arguments[0].click();", sug)
                matched = True
                logger.info(f"Selected employee: {sug.text.strip()}")
                break

        if not matched:
            raise Exception(f"Employee '{emp_name}' not found in suggestions")

        # Fill other fields
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.add_username)
        ).send_keys(username)
        self.select_dropdown(self.add_status, status)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.add_password)
        ).send_keys(password)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.add_confirm_password)
        ).send_keys(password)
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.save_button)
        ).click()
        logger.info(f"Added new user {username}")

    @allure.step("Wait for success message")
    def wait_for_success_message(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.success_message)
        )
        logger.info("Success message displayed")

    @allure.step("Delete selected user(s)")
    def delete_user(self, username=None):
        if username:
            user_checkbox = (By.XPATH, f"//div[text()='{username}']/../preceding-sibling::div//input[@type='checkbox']")
            checkbox_element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(user_checkbox)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_element)
            self.driver.execute_script("arguments[0].click();", checkbox_element)
            logger.info(f"Selected checkbox for user: {username}")

        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.delete_button)
        ).click()
        logger.info("Clicked Delete button")
