from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Force ChromeDriver 109 to match Chrome 109 on Win8
    driver_path = ChromeDriverManager(driver_version="109.0.5414.74").install()
    print(f"Using ChromeDriver: {driver_path}")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Classic headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Initialize driver
    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    # Open Google and print title
    driver.get("https://www.google.com")
    print("Page title is:", driver.title)

    # Print browser version
    capabilities = driver.capabilities
    print("Browser name:", capabilities.get("browserName"))
    print("Browser version:", capabilities.get("browserVersion"))

    driver.quit()
    print("ChromeDriver 109 verification completed successfully!")

if __name__ == "__main__":
    main()
