import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

@allure.epic("Admin Module")
@allure.feature("User Management")
class TestEditUser:

    @allure.story("Edit existing user")
    def test_edit_existing_user(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        admin_page = AdminPage(driver)

        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        admin_page.open_admin_tab()

        existing_username = "ameenrahman1"
        admin_page.search_user(username=existing_username, role="ESS", status="Enabled")

        admin_page.edit_user(username=existing_username, new_role="Admin", new_status="Disabled")

        admin_page.wait_for_success_message()
        assert admin_page.is_visible(admin_page.success_message)
