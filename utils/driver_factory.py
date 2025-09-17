import platform
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        # Force ChromeDriver version 109 (last supported for Win8)
        service = Service(ChromeDriverManager(driver_version="109.0.5414.74").install())
        driver = webdriver.Chrome(service=service, options=options)

        # 🔹 Attach environment details to Allure
        DriverFactory.attach_env_info(driver)

        return driver

    @staticmethod
    def attach_env_info(driver):
        """Attach environment details to Allure report"""
        try:
            browser_name = driver.capabilities.get("browserName", "Unknown")
            browser_version = driver.capabilities.get("browserVersion", "Unknown")
            os_name = platform.system()
            os_version = platform.version()

            env_info = (
                f"Browser: {browser_name} {browser_version}\n"
                f"OS: {os_name} {os_version}\n"
                f"Platform: {platform.platform()}"
            )

            allure.attach(
                env_info,
                name="Test Environment",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as e:
            allure.attach(
                str(e),
                name="Environment Info Error",
                attachment_type=allure.attachment_type.TEXT
            )
