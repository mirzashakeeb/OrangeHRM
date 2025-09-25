import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@allure.epic("Dashboard Module")
@allure.feature("Dashboard Functionality")
@pytest.mark.usefixtures("driver")  # uses the driver from conftest.py
class TestDashboard:

    @allure.story("Load dashboard after login")
    def test_dashboard_loads_after_login(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        # Step 1: Login
        login_page.open_login_page()
        result = login_page.login("Admin", "admin123")

        # Step 2: Validate login success
        assert result == "success"
        assert dashboard_page.is_dashboard_loaded()

    @allure.story("Navigate to PIM page")
    def test_navigate_to_pim(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        # Step 3: Navigate to PIM
        dashboard_page.go_to_pim()

    @allure.story("Navigate to Leave page")
    def test_navigate_to_leave(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        # Step 3: Navigate to Leave
        dashboard_page.go_to_leave()

    @allure.story("Navigate assign leave")
    def test_assign_leave_button(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        # Step 3: Click Assign Leave
        dashboard_page.click_assign_leave()


    @allure.story("Navigate to Leave List page")
    def test_leave_list_button(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        # Step 3: Click Leave List
        dashboard_page.click_leave_list()
