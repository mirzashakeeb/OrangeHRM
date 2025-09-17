import pytest
import allure
from pages.login_page import LoginPage
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
        except AssertionError as e:
            allure.attach(driver.get_screenshot_as_png(),
                          name=f"{username}_login_failure",
                          attachment_type=allure.attachment_type.PNG)
            raise
