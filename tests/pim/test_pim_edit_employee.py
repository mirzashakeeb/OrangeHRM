import pytest
import allure
from pages.pim_page import PIMPage

@pytest.mark.usefixtures("driver")
class TestEditEmployee:

    @allure.title("Search employee, edit nickname, and verify update")
    def test_search_and_edit_nickname(self, driver, login):
        """
        Test Steps:
        1. Navigate to PIM
        2. Search employee by name
        3. Click edit button
        4. Update nickname
        5. Save
        6. Verify nickname updated
        """

        # Step 1: Login and go to dashboard
        dashboard_page = login
        pim_page = PIMPage(driver)

        with allure.step("Navigate to PIM module"):
            dashboard_page.go_to_pim()

        # Employee details
        employee_name = "mirza shakeeb farhan baig"
        new_nickname = "MZ"

        with allure.step(f"Search for employee: {employee_name}"):
            pim_page.search_employee(employee_name)

        with allure.step(f"Edit employee '{employee_name}'"):
            pim_page.click_edit_button(employee_name)
            pim_page.update_nickname(new_nickname)
            pim_page.click_save()

        with allure.step("Validate nickname updated"):
            # Re-open edit page to verify value
            pim_page.search_employee(employee_name)
            pim_page.click_edit_button(employee_name)
            updated_value = pim_page.get_nickname_value()
            assert updated_value == new_nickname, (
                f"Expected nickname '{new_nickname}' but got '{updated_value}'"
            )
