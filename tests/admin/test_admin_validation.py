import pytest
import allure

@allure.epic("Admin Module")
@allure.feature("User Management")
class TestValidation:

    @allure.story("Mandatory fields validation")
    def test_mandatory_fields_validation(self, login_as_admin):
        admin_page = login_as_admin
        admin_page.open_admin_tab()
        admin_page.click_add_button()
        errors = admin_page.check_mandatory_fields()
        assert errors, "Expected validation errors but none displayed"
