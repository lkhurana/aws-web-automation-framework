import time
from selenium.webdriver.common.by import By
from src.config import (
    WEB_URL,
    USERNAME,
    PASSWORD
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
        time.sleep(2)

        # Locate the username and password fields and sign-in button
        username_input = driver.find_element(By.ID, "login_field")
        password_input = driver.find_element(By.ID, "password")
        sign_in_button = driver.find_element(By.NAME, "commit")

        # Fill in the login form
        logger.info('Entering user credentials...')
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        # Click the sign-in button
        sign_in_button.click()
        logger.info('Sign in button clicked.')

        # Wait for a while to observe the result
        time.sleep(5)

    finally:
        logger.info(f"Current URL after login attempt: {driver.current_url}")

        # Close the WebDriver
        driver.quit()
        logger.info('Chrome driver closed. Script ended.')