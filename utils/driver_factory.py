import platform
import logging
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("automation")
logging.basicConfig(level=logging.INFO)

class DriverFactory:
    @staticmethod
    def get_driver():
        logger.info("Starting Chrome WebDriver")

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        #options.add_argument("--disable-gpu")
        #options.add_argument("--no-sandbox")
        #options.add_argument("--disable-dev-shm-usage")
        #options.add_argument("--window-size=1920,1080")
        #options.add_argument("--disable-extensions")
        #options.add_argument("--remote-allow-origins=*")

        # Detect OS
        if platform.system() == "Windows":
            # Windows 8 local environment
            service = Service(ChromeDriverManager().install())
        else:
            # GitHub Actions / Ubuntu CI
            service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)
        DriverFactory.attach_env_info(driver)
        return driver

    @staticmethod
    def attach_env_info(driver):
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
