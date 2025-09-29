import pytest
import allure
from pages.pim_page import PIMPage

@pytest.mark.usefixtures("driver")
class TestPIMAddEmployee:

    @allure.title("Add Employee with login credentials")
    def test_add_employee_with_login(self, driver, login):
        dashboard_page = login
        pim_page = PIMPage(driver)

        dashboard_page.go_to_pim()
        pim_page.click_add_employee()
        pim_page.enter_first_name("mirza")
        pim_page.enter_last_name("shakeeb")
        pim_page.set_login_credentials("mirzasha123", "Password@123", "Password@123")
        pim_page.click_save()
        pim_page.wait_for_element(pim_page.employee_list_header)
