import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage  # <-- You’ll need this page object
from utils.data_reader import get_login_data
from utils.logger import get_logger

logger = get_logger(__name__)

@allure.epic("Login Module")
@allure.feature("Login Functionality")
@pytest.mark.parametrize("username,password,expected", get_login_data())
def test_login(driver, username, password, expected):
    # Attach the test data safely here
    allure.attach(
        f"Username: {username}, Password: {password}, Expected: {expected}",
        name="Test Data",
        attachment_type=allure.attachment_type.TEXT
    )

    login_page = LoginPage(driver)

    with allure.step("Open login page"):
        login_page.open_login_page()

    with allure.step("Perform login"):
        result = login_page.login(username, password)

    with allure.step("Verify login result"):
        try:
            assert result == expected, f"Login test failed for {username}"
            allure.attach(driver.get_screenshot_as_png(),
                          name=f"{username}_login_success",
                          attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            allure.attach(driver.get_screenshot_as_png(),
                          name=f"{username}_login_failure",
                          attachment_type=allure.attachment_type.PNG)
            raise


@allure.epic("Login Module")
@allure.feature("Logout Functionality")
def test_login_logout(driver):
    """
    Test Case ID: TC_LOGIN_06
    Title: Logout functionality
    Steps:
      1. Login
      2. Click Logout
    Expected Result:
      User redirected to login page
    """
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    with allure.step("Step 1: Login with valid credentials"):
        login_page.open_login_page()
        login_page.login("admin", "admin123")  # use valid test credentials

    with allure.step("Step 2: Perform logout"):
        dashboard_page.logout()

    with allure.step("Verify logout redirection"):
        assert login_page.is_login_page_displayed(), "User was not redirected to login page after logout"
        allure.attach(driver.get_screenshot_as_png(),
                      name="logout_result",
                      attachment_type=allure.attachment_type.PNG)
