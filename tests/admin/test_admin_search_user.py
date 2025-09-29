import pytest
import allure
from pages.pim_page import PIMPage

@pytest.mark.usefixtures("driver")
class TestPIMEditEmployee:

    @allure.title("Edit existing employee details")
    def test_edit_employee(self, driver, login):
        dashboard_page = login
        pim_page = PIMPage(driver)

        dashboard_page.go_to_pim()
        pim_page.search_employee("mirza shakeeb farhan baig")
        pim_page.click_edit_employee(index=0)
        pim_page.type(pim_page.job_title_input, "Senior Developer")
        pim_page.click_save()
