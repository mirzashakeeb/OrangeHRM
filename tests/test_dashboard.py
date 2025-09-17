import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.apply_leave_page import ApplyLeavePage


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

    @allure.epic("Leave Module")
    @allure.feature("Leave Functionality")
    @allure.story("Navigate to Apply Leave")
    def test_apply_leave(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        apply_leave_page = ApplyLeavePage(driver)

        # Step 1 : Login
        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        # Step 2: Open Apply Leave form
        dashboard_page.click_apply_leave()

        # Step 3: Fill out the form
        apply_leave_page.select_leave_type("CAN - Personal")
        apply_leave_page.enter_from_date("2025-09-10")
        apply_leave_page.enter_to_date("2025-09-12")
        apply_leave_page.enter_comment("Vacation leave for family trip")

        # Step 4 : Submit
        apply_leave_page.submit()

        # Step 5 : Validate success
        assert apply_leave_page.is_leave_applied(), "❌ Leave was not applied successfully"
