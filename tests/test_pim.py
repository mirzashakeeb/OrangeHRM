import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage

@pytest.mark.usefixtures("driver")
class TestPIM:

    def test_add_employee_with_login(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)

        # --- Login ---
        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        # --- Go to PIM ---
        dashboard_page.go_to_pim()

        # --- Add Employee ---
        pim_page.click_add_employee()
        pim_page.enter_first_name("mirza")
        pim_page.enter_last_name("shakeeb")

        # --- Toggle Create Login & Enter Credentials ---
        pim_page.toggle_create_login()
        pim_page.enter_username("mirzasha123")
        pim_page.enter_password("Password@123")
        pim_page.enter_confirm_password("Password@123")

        # --- Save ---
        pim_page.click_save()
        pim_page.wait_for_employee_list()

    def test_edit_employee(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)

        # --- Login ---
        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded()

        # --- Go to PIM ---
        dashboard_page.go_to_pim()

        # --- Search for Employee ---
        pim_page.search_employee("mirza shakeeb farhan baig")

        # --- Click Edit and Wait for Form ---
        pim_page.click_edit_employee("mirza shakeeb farhan baig")

        # --- Save ---
        pim_page.click_save()
