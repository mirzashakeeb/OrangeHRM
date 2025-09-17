import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

@allure.epic("Admin Module")
@allure.feature("User Management")
class TestAdminPage:

    @allure.story("Full Admin flow: Add, Search, Reset, Delete user")
    def test_admin_full_flow(self, driver):
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        admin_page = AdminPage(driver)

        # Step 1: Login as Admin
        with allure.step("Login as Admin"):
            login_page.open_login_page()
            login_page.login("Admin", "admin123")
            assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load"

        # Step 2: Navigate to Admin tab
        with allure.step("Open Admin tab"):
            admin_page.open_admin_tab()

        # Step 3: Add new user
        username_to_add = "test_admin2"
        employee_name = "Amelia  Amelia"
        with allure.step(f"Add new user: {username_to_add}"):
            admin_page.click_add_button()  # Waits for Add User form
            admin_page.add_new_user(
                role="Admin",
                emp_name=employee_name,  # Employee autocomplete handled
                username=username_to_add,
                status="Enabled",
                password="Test@1234"
            )
            admin_page.wait_for_success_message()
            assert admin_page.is_visible(admin_page.success_message), "Success message not displayed"

        # Step 4: Search the newly added user
        with allure.step(f"Search for user: {username_to_add}"):
            admin_page.search_user(
                username=username_to_add,
                role="Admin",
                emp_name=employee_name,
                status="Enabled"
            )

        # Step 5: Reset search filters
        with allure.step("Reset search filters"):
            admin_page.reset_search()

        # Step 6: Delete the user
        with allure.step(f"Delete user: {username_to_add}"):
            admin_page.delete_user(username=username_to_add)
            admin_page.wait_for_success_message()
            assert admin_page.is_visible(admin_page.success_message), "User deletion failed"
