import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrangeHRMLoginTest:
    LOGIN_URL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
    USERNAME = 'Admin'
    PASSWORD = 'admin123'
    USERNAME_XPATH = "//input[@name='username']"
    PASSWORD_XPATH = "//input[@name='password']"
    LOGIN_BUTTON_XPATH = "//button[@type='submit']"
    DASHBOARD_URL_FRAGMENT = '/dashboard'

    @staticmethod
    def get_driver():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        return driver

    @staticmethod
    def login(driver):
        try:
            driver.get(OrangeHRMLoginTest.LOGIN_URL)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, OrangeHRMLoginTest.USERNAME_XPATH))
            )
            username_field = driver.find_element(By.XPATH, OrangeHRMLoginTest.USERNAME_XPATH)
            password_field = driver.find_element(By.XPATH, OrangeHRMLoginTest.PASSWORD_XPATH)
            login_button = driver.find_element(By.XPATH, OrangeHRMLoginTest.LOGIN_BUTTON_XPATH)
            username_field.clear()
            username_field.send_keys(OrangeHRMLoginTest.USERNAME)
            password_field.clear()
            password_field.send_keys(OrangeHRMLoginTest.PASSWORD)
            login_button.click()
            # Wait for dashboard page to load
            WebDriverWait(driver, 15).until(
                EC.url_contains(OrangeHRMLoginTest.DASHBOARD_URL_FRAGMENT)
            )
            return True
        except Exception as e:
            driver.save_screenshot('error_orangehrm_login.png')
            raise RuntimeError(f"Login test failed: {str(e)}")
    
    @staticmethod
    def validate_dashboard(driver):
        try:
            # Dashboard page has a unique element: "Dashboard" header
            dashboard_header_xpath = "//h6[text()='Dashboard']"
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, dashboard_header_xpath))
            )
            assert OrangeHRMLoginTest.DASHBOARD_URL_FRAGMENT in driver.current_url, \
                f"Expected dashboard URL fragment not found: {driver.current_url}"
            assert driver.find_element(By.XPATH, dashboard_header_xpath).is_displayed(), \
                "Dashboard header not visible after login."
        except Exception as e:
            driver.save_screenshot('error_orangehrm_dashboard.png')
            raise AssertionError(f"Dashboard validation failed: {str(e)}")

@pytest.mark.ci
def test_automate_login_functionality_for_orangehrm():
    """
    Test Case: Automate login functionality for OrangeHRM
    Jira: KAN-15
    Steps:
      1. Navigate to the login page
      2. Enter valid username
      3. Enter valid password
      4. Click on Login button
    Expected Result:
      User should be redirected to the dashboard page.
    """
    driver = None
    try:
        driver = OrangeHRMLoginTest.get_driver()
        login_success = OrangeHRMLoginTest.login(driver)
        assert login_success, "Login process did not complete successfully."
        OrangeHRMLoginTest.validate_dashboard(driver)
    finally:
        if driver:
            driver.quit()
