import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utils.logger import get_logger
import time

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
        self.existing_user = (By.XPATH,"//i[@class='oxd-icon bi-caret-down-fill']")
        self.search_button = (By.XPATH, "//button[normalize-space()='Search']")
        self.reset_button = (By.XPATH, "//button[normalize-space()='Reset']")
        self.add_button = (By.XPATH, "//button[normalize-space()='Add']")
        self.delete_button = (By.XPATH, "//button[normalize-space()='Delete Selected']")

        # --- Add User form locators ---
        self.add_user_role = self.user_role_dropdown
        self.add_employee_name = self.employee_name_field
        self.add_username = self.username_field
        self.add_status = self.status_dropdown
        self.add_password = (By.XPATH, "(//input[@type='password'])[1]")
        self.add_confirm_password = (By.XPATH, "(//input[@type='password'])[2]")
        self.save_button = (By.XPATH, "//button[normalize-space()='Save']")

        # --- Validation locators ---
        self.success_message = (By.XPATH, "//div[contains(@class,'oxd-toast--success')]")
        self.loader = (By.CSS_SELECTOR, "div.oxd-form-loader")

    @allure.step("Open Admin Tab")
    def open_admin_tab(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.admin_tab)
        ).click()
        logger.info("Opened Admin Tab")


    # ---------------- ADD USER ----------------

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

        # Employee autocomplete handling
        emp_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.add_employee_name)
        )
        emp_input.clear()
        emp_input.send_keys(emp_name)

        # Wait for loader to disappear if any
        WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located(self.loader)
        )

        # Wait for the first suggestion and click it
        first_suggestion_xpath = "//div[@role='listbox']//span[1]"
        first_suggestion = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, first_suggestion_xpath))
        )
        first_suggestion.click()
        logger.info(f"Selected first employee suggestion for '{emp_name}'")

        # Fill remaining fields
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


    # ---------------- SEARCH USER ----------------

    @allure.step("Search user: {username}")
    def search_user(self, username="", role=None, emp_name="", status=None):
        # Enter username
        if username:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.username_field)
            ).clear()
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.username_field)
            ).send_keys(username)

        # Select role if provided
        if role:
            self.select_dropdown(self.user_role_dropdown, role)

        # Enter employee name
        if emp_name:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.employee_name_field)
            ).clear()
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.employee_name_field)
            ).send_keys(emp_name)

        # Select status if provided
        if status:
            self.select_dropdown(self.status_dropdown, status)

        # Click search button
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


    # ---------------- DELETE USER----------------

    from selenium.webdriver.common.keys import Keys
    import time

    @allure.step("Search and Delete user: {username}")
    def delete_user(self, username: str):
        """Search for a user and delete them."""

        # ----Search for the user----
        search_input = (By.XPATH, "//label[normalize-space()='Username']/../following-sibling::div//input")
        search_button = (By.XPATH, "//button[normalize-space()='Search']")

        input_element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(search_input)
        )
        input_element.clear()
        input_element.send_keys(username)
        input_element.send_keys(Keys.ESCAPE)  # close any dropdown

        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(search_button)
        ).click()
        logger.info(f"Searched for user: {username}")

        # ----Click Delete button safely----
        delete_button = (By.XPATH, "(//button[@class='oxd-icon-button oxd-table-cell-action-space'])[1]")
        btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(delete_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.3)  # optional: wait for page animation
        btn.click()
        logger.info("Clicked Delete button")

        # ----Confirm deletion safely----
        confirm_button = (By.XPATH, "//button[normalize-space()='Yes, Delete']")
        btn_confirm = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(confirm_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_confirm)
        time.sleep(0.3)
        btn_confirm.click()
        logger.info(f"Confirmed deletion of user: {username}")

    #--------------EDITING USER--------------------

    @allure.step("Edit user: {username}")
    def edit_user(self, username, new_role=None, new_status=None,
                  change_password=False, new_password=None,change_password_checkbox =None):
        """
        Edit user details: role, status and optionally change password.
        """
        # Locate the pencil icon for the specific user row
        edit_icon = (
            By.XPATH,
            f"//div[text()='{username}']/ancestor::div[contains(@class,'oxd-table-row')]"
            "//i[@class='oxd-icon bi-pencil-fill']"
        )

        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(edit_icon)
        ).click()

        if new_role:
            self.select_dropdown(self.add_user_role, new_role)

        if new_status:
            self.select_dropdown(self.add_status, new_status)

        # Save changes
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.save_button)
        ).click()

        logger.info(
            f"Edited user {username} → "
            f"Role={new_role}, Status={new_status}, PasswordChanged={change_password}"
        )

    # ---------------- RESET PASSWORD -------------------

    @allure.step("Reset password for user: {username}")
    def reset_password(self, username, new_password):

        # Locators
        change_password_checkbox = (By.XPATH, "//span[@class='oxd-checkbox-input oxd-checkbox-input--active --label-right oxd-checkbox-input']")
        new_password_input = (By.XPATH, "(//input[@type='password'])[1]")
        confirm_password_input = (By.XPATH, "(//input[@type='password'])[2]")
        edit_icon = (
            By.XPATH,
            f"//div[text()='{username}']/ancestor::div[contains(@class,'oxd-table-row')]"
            "//i[@class='oxd-icon bi-pencil-fill']"
        )

        # --- Open Edit Page for Employee ---
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(edit_icon)
        ).click()
        logger.info(f"Opened edit form for {username}")

        # --- Toggle Change Password Checkbox ---
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(change_password_checkbox)
        ).click()
        logger.info("Checked 'Change Password' checkbox")

        # --- Enter New Password ---
        pwd = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(new_password_input)
        )
        pwd.clear()
        pwd.send_keys(new_password)
        logger.info("Entered new password")

        # --- Confirm New Password ---
        confirm_pwd = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(confirm_password_input)
        )
        confirm_pwd.clear()
        confirm_pwd.send_keys(new_password)
        logger.info("Confirmed new password")

        # --- Click Save ---
        save_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.save_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
        time.sleep(0.3)
        save_btn.click()
        logger.info(f"Password successfully reset for user: {username}")

    #-------------CHECK MANDATORY FIELD----------------

    @allure.step("Check mandatory field validation")
    def check_mandatory_fields(self):
        # Wait until Save button is visible and clickable
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.save_button)
        )

        # Click Save
        self.click(self.save_button)

        # Wait until at least one error message appears
        error_messages = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, "//span[contains(@class,'oxd-input-field-error-message')]")
            )
        )

        # Return only non-empty error texts
        return [err.text for err in error_messages if err.text.strip()]
