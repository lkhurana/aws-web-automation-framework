import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils import get_credential
from src.config import (
    WEB_URL,
    LOGIN_USER_PARAM_NAME,
    LOGIN_PASS_PARAM_NAME
)

def automate_login(logger,driver):
    """
    Automates the login process for GitHub using Selenium.

    This function opens the GitHub login page, enters the username and password 
    credentials, and clicks the sign-in button. It then logs the current URL after 
    the login attempt and closes the WebDriver.

    Args:
        logger (logging.Logger): Logger instance to record log messages.
        driver (selenium.webdriver.Chrome): The Selenium WebDriver instance used to 
            control the Chrome browser.

    Procedure:
        1. Navigates to the GitHub login page specified by `WEB_URL`.
        2. Waits for the page to load.
        3. Locates and fills in the login form fields for username and password.
        4. Clicks the sign-in button to submit the form.
        5. Waits briefly to allow for page redirection after login.
        6. Logs the resulting URL after the login attempt.
        7. Closes the WebDriver instance and logs the closure.

    Note:
        Constants `WEB_URL`, `USERNAME`, and `PASSWORD` should be defined in the config 
        file prior to calling this function, as they are used within this function to 
        specify the login URL and credentials.

    Raises:
        selenium.common.exceptions.NoSuchElementException: If any of the form elements 
            (username, password, or sign-in button) are not found on the page.

    """
    try:
        # Open GitHub login page
        logger.info(f'Navigating to {WEB_URL}...')
        driver.get(WEB_URL)

        # Wait for the page to load
        time.sleep(10)
        try:
            logger.info('Finding cookies element..')
            # Find the shadow host element
            shadow_host = driver.find_element(By.CSS_SELECTOR, "div#usercentrics-root")
            # Access the shadow root using JavaScript
            shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
            # Find the cookie accept button inside the shadow root
            accept_button = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-deny-all-button']")

            # Click the accept button
            accept_button.click()
            logger.info('Accepted the cookies.')
        
        except:
            None

        time.sleep(random.uniform(4, 8))

        # go to the login page by clicking on the button
        cookies_button = driver.find_element(By.XPATH, "//a[@class='coh-style-link-primary lfg-login-btn']")
        cookies_button.click()
        time.sleep(random.uniform(4, 8))

        # Locate the username and password fields and sign-in button
        username_input = driver.find_element(By.ID, "inputEmail")
        password_input = driver.find_element(By.ID, "inputPassword")

        # Fill in the login form
        logger.info('Entering user credentials...')
        username_input.send_keys(get_credential(LOGIN_USER_PARAM_NAME))
        time.sleep(random.uniform(3, 5))
        password_input.send_keys(get_credential(LOGIN_PASS_PARAM_NAME))
        time.sleep(random.uniform(3, 5))

        # Click the sign-in button
        password_input.send_keys(Keys.RETURN)
        logger.info('Sign in button clicked.')

        # Wait for a while to observe the result
        time.sleep(random.uniform(8, 15))

    finally:
        logger.info(f"Current URL after login attempt: {driver.current_url}")