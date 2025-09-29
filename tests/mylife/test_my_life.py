import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.my_life_page import MyLifePage

@pytest.mark.usefixtures("driver")
class TestMyLifePage:

    def test_personal_details_displayed(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        my_life_page = MyLifePage(driver)

        # Login
        login_page.open_login_page()
        login_page.login("Admin", "admin123")
        assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load"

        # Open My Info tab
        my_life_page.open_my_life_tab()

        # Check Personal Details
        assert my_life_page.is_personal_details_displayed(), "Personal Details section is not displayed"
