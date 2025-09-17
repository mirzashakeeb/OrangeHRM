import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.apply_leave_page import ApplyLeavePage


@allure.epic("Leave Module")
@allure.feature("Apply Leave Functionality")
@pytest.mark.usefixtures("driver")  # driver comes from conftest.py
class TestApplyLeave:

    @allure.story("Apply leave successfully")
    def test_apply_leave(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        apply_leave_page = ApplyLeavePage(driver)

        # Step 1: Login
        with allure.step("Login as Admin"):
            login_page.open_login_page()
            login_page.login("Admin", "admin123")
            assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load"

        # Step 2: Navigate to Apply Leave
        with allure.step("Navigate to Apply Leave page"):
            dashboard_page.click_apply_leave()

        # Step 3: Fill out leave form
        with allure.step("Fill leave form"):
            apply_leave_page.select_leave_type("CAN - Bereavement")
            apply_leave_page.enter_from_date("2025-09-15")
            apply_leave_page.enter_to_date("2025-09-18")
            apply_leave_page.enter_comment("Grant me leave sir")

        # Step 4: Submit leave
        with allure.step("Submit leave application"):
            apply_leave_page.submit()

        # Step 5: Verify leave applied
        with allure.step("Verify leave success"):
            assert apply_leave_page.is_leave_applied(), "Leave was not applied successfully"
