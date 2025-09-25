import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

@allure.epic("Admin Module")
@allure.feature("User Management")
class TestAddUser:

    @allure.story("Add new user")
    def test_add_user(self, login_as_admin):
        admin_page = login_as_admin
        username = "ramesh"
        employee_name = "Ramesh Kumar B"

        admin_page.click_add_button()
        admin_page.add_new_user(
            role="Admin",
            emp_name=employee_name,
            username=username,
            status="Enabled",
            password="ramesh1234"
        )
        admin_page.wait_for_success_message()

        assert admin_page.is_visible(admin_page.success_message)
