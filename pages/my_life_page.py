import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class MyLifePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.my_life_tab = (By.XPATH, "//span[text()='My Info']")
        self.personal_details_section = (By.XPATH, "//h6[text()='Personal Details']")

    @allure.step("Open My Info tab")
    def open_my_life_tab(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.my_life_tab)
        ).click()
        logger.info("Opened My Info tab")

    @allure.step("Check if Personal Details is displayed")
    def is_personal_details_displayed(self):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.personal_details_section)
        )
        displayed = element.is_displayed()
        logger.info(f"Personal Details displayed: {displayed}")
        return displayed
