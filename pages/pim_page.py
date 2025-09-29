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
        self.timeout = 10

        # ---------- Add Employee locators ----------
        self.add_employee_btn = (By.XPATH, "//button[normalize-space()='Add']")
        self.first_name_input = (By.NAME, "firstName")
        self.last_name_input = (By.NAME, "lastName")
        self.create_login_toggle = (By.XPATH, "//span[contains(@class,'oxd-switch-input')]")
        self.user_name_input = (By.XPATH, "(//label[text()='Username']/../following-sibling::div//input)[1]")
        self.password_input = (By.XPATH, "(//input[@type='password'])[1]")
        self.confirm_password_input = (By.XPATH, "(//input[@type='password'])[2]")
        self.save_btn = (By.XPATH, "//button[normalize-space()='Save']")
        self.employee_list_header = (By.XPATH, "//h6[text()='Personal Details']")

        # ---------- Edit/Search Employee locators ----------
        self.search_input = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
        self.search_button = (By.XPATH, "//button[@type='submit']")
        self.job_title_input = (By.XPATH, "//label[text()='Job Title']/../following-sibling::div//input")
        self.nickname_input = (By.XPATH, "//label[text()='Nickname']/../following-sibling::div/input")

    # ---------- Common Helper ----------
    @allure.step("Wait for element to be visible: {locator}")
    def wait_for_element(self, locator, timeout=None):
        """Wait until the element is visible and return it"""
        wait_time = timeout if timeout else self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )

    # ---------- Add Employee ----------
    @allure.step("Click Add Employee button")
    def click_add_employee(self):
        self.click(self.add_employee_btn)
        logger.info("Clicked Add Employee button")

    @allure.step("Enter First Name: {first_name}")
    def enter_first_name(self, first_name):
        self.wait_for_element(self.first_name_input).send_keys(first_name)

    @allure.step("Enter Last Name: {last_name}")
    def enter_last_name(self, last_name):
        self.wait_for_element(self.last_name_input).send_keys(last_name)

    @allure.step("Toggle Create Login Details")
    def toggle_create_login(self):
        self.click(self.create_login_toggle)
        logger.info("Toggled Create Login Details")
        self.wait_for_element(self.user_name_input)

    @allure.step("Enter Username: {username}")
    def enter_username(self, username):
        self.wait_for_element(self.user_name_input).send_keys(username)

    @allure.step("Enter Password")
    def enter_password(self, password):
        self.wait_for_element(self.password_input).send_keys(password)

    @allure.step("Confirm Password")
    def enter_confirm_password(self, confirm_password):
        self.wait_for_element(self.confirm_password_input).send_keys(confirm_password)

    @allure.step("Set login credentials: {username}")
    def set_login_credentials(self, username, password, confirm_password):
        self.toggle_create_login()
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)

    # ---------- Search Employee ----------
    @allure.step("Search employee by name: {employee_name}")
    def search_employee(self, employee_name):
        """Search for an employee by name and wait for results to load"""
        search_box = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.search_input)
        )
        search_box.clear()
        search_box.send_keys(employee_name)
        self.click(self.search_button)
        logger.info(f"Searched employee: {employee_name}")

        # Wait for the row with the employee name to appear
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//div[text()='{employee_name}']")
            )
        )

    # ---------- Edit Employee ----------
    @allure.step("Click Edit button for employee '{employee_name}'")
    def click_edit_button(self, employee_name):
        edit_btn_locator = (By.XPATH,"//button[@ type='button']")
        edit_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(edit_btn_locator)
        )
        edit_btn.click()
        logger.info(f"Clicked Edit button for {employee_name}")

    @allure.step("Update Nickname to '{new_nickname}'")
    def update_nickname(self, new_nickname):
        nickname_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.nickname_input)
        )
        nickname_elem.clear()
        nickname_elem.send_keys(new_nickname)
        logger.info(f"Changed nickname to '{new_nickname}'")

    @allure.step("Get current nickname value")
    def get_nickname_value(self):
        """Return the current value of the Nickname field"""
        nickname_elem = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.nickname_input)
        )
        return nickname_elem.get_attribute("value")

    # ---------- Common ----------
    @allure.step("Click Save button")
    def click_save(self):
        self.click(self.save_btn)
        logger.info("Clicked Save button")