import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

@allure.epic("Admin Module")
@allure.feature("User Management")
class TestSearchUser:

    @allure.story("Search existing user")
    def test_search_existing_user(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        admin_page = AdminPage(driver)

        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        admin_page.open_admin_tab()

        existing_username = "Ameen2"
        existing_employee = "Ameen K Rahman"
        admin_page.search_user(username=existing_username,role="Admin",emp_name=existing_employee,status="Enabled")

        user_rows = driver.find_elements("xpath", f"//div[text()='{existing_username}']")
        assert len(user_rows) > 0, f"User '{existing_username}' not found in search results"
