import time
from selenium.webdriver.support import expected_conditions as EC
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

# ---------------- FIXTURE TO LOGIN AS ADMIN ----------------
@pytest.fixture
def login_as_admin(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    admin_page = AdminPage(driver)

    login_page.open_login_page()
    login_page.login("Admin", "admin123")
    assert dashboard_page.is_dashboard_loaded()
    admin_page.open_admin_tab()

    return admin_page


# ---------------- FIXTURE TO CREATE AND CLEANUP USER ----------------
@pytest.fixture
def temp_user(driver, login_as_admin):
    admin_page = login_as_admin
    username = f"test_admin_{int(time.time())}"
    employee_name = "Thomas Kutty Benny"  # Use valid employee name

    admin_page.click_add_button()
    admin_page.add_new_user(
        role="Admin",
        emp_name=employee_name,
        username=username,
        status="Enabled",
        password="Test@1234"
    )
    admin_page.wait_for_success_message()

    yield {"username": username, "employee_name": employee_name}

    # Cleanup: Delete the user
    admin_page.search_user(username=username)
    admin_page.delete_user(username=username)
    admin_page.wait_for_success_message()


# ---------------- TEST CLASS ----------------
@allure.epic("Admin Module")
@allure.feature("User Management")
class TestAdminPage:

    @allure.story("Add new user")
    def test_add_user(self, login_as_admin):
        admin_page = login_as_admin
        username = "mirza"
        employee_name = "mirza shakeeb farhan baig"

        admin_page.click_add_button()
        admin_page.add_new_user(
            role="Admin",
            emp_name=employee_name,
            username=username,
            status="Enabled",
            password="mirza1234"
        )
        admin_page.wait_for_success_message()

        assert admin_page.is_visible(admin_page.success_message)

        # Cleanup
        #admin_page.search_user(username=username)
        #admin_page.delete_user(username=username)
        #admin_page.wait_for_success_message()

    @allure.story("Search existing user")
    def test_search_existing_user(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        admin_page = AdminPage(driver)

        # --- Login as Admin ---
        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load after login"

        # --- Open Admin Tab ---
        admin_page.open_admin_tab()

        # --- Search for an existing user ---
        existing_username = "mirza"         # Replace with actual existing username
        existing_employee = "mirza shakeeb farhan baig"      # Replace with actual employee name
        admin_page.search_user(
            username=existing_username,
            role="Admin",
            emp_name=existing_employee,
            status="Enabled"
        )

        # --- Assertion: Check user appears in search results ---
        user_rows = driver.find_elements("xpath", f"//div[text()='{existing_username}']")
        assert len(user_rows) > 0, f"User '{existing_username}' not found in search results"


    # ---------------- EDIT USER ----------------

    @allure.story("Edit existing user")
    def test_edit_existing_user(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        admin_page = AdminPage(driver)

        # Login
        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load"

        # Open Admin tab
        admin_page.open_admin_tab()

        # Search for the existing user
        existing_username = "mirza"
        admin_page.search_user(
            username=existing_username,
            role="Admin",
            status="Enabled"
        )

        #Edit user details and change password in ONE call
        admin_page.edit_user(
            username=existing_username,
            new_role="ESS",
            new_status="Disabled",
        )

        # Verify success message
        admin_page.wait_for_success_message()
        assert admin_page.is_visible(admin_page.success_message), \
            "Success message not displayed after editing"

    #----------------RESET-PASSWORD----------------------

    @allure.story("Reset password for existing user")
    def test_reset_existing_user_password(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        admin_page = AdminPage(driver)

        # ---- Login as Admin ----
        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load"

        # ---- Open Admin tab ----
        admin_page.open_admin_tab()

        # ---- Define user and new password ----
        existing_username = "mirza"  # Replace with actual existing username
        new_password = "NewPass@123"

        # ---- Reset password ----
        admin_page.reset_password(username=existing_username, new_password=new_password)
        admin_page.wait_for_success_message()
        assert admin_page.is_visible(admin_page.success_message), "Password reset success message not displayed"

        # ---- Logout Admin ----
        dashboard_page.logout()

        # ---- Verify login with new password ----
        login_page.open_login_page()
        login_page.login(existing_username, new_password)
        assert dashboard_page.is_dashboard_loaded(), "Login failed with new password"

    @allure.story("Mandatory fields validation")
    def test_mandatory_fields_validation(self, login_as_admin):
        admin_page = login_as_admin

        admin_page.click_add_button()
        errors = admin_page.check_mandatory_fields()
        assert errors, "Expected validation errors but none displayed"

    import allure

    @allure.story("Deleting Existing User")
    def test_delete_existing_user(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        admin_page = AdminPage(driver)

        # ---- Login ----
        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load after login"

        # ---- Open Admin tab ----
        admin_page.open_admin_tab()

        # ---- Search and delete user ----
        admin_page.delete_user(username="mirza")
