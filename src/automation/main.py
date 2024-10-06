import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from src.config.config import (
    WEB_URL,
    USERNAME,
    PASSWORD,
    EMAIL_RECIPIENT
)
from src.logging_scripts.log_handler import setup_logging, send_log_email

# Initialize logging
LOG_FILENAME = 'automation_script.log'
logger = setup_logging(LOG_FILENAME)

# Set up the WebDriver
logger.info('Initializing Chrome driver...')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def automate_login():
    try:
        # Open GitHub login page
        logger.info('Opening login page...')
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


if __name__ == "__main__":
    logger.info("Starting the automation script...")
    automate_login()

    # Send logs via email
    logger.info("Sending logs via email...")
    send_log_email(LOG_FILENAME,EMAIL_RECIPIENT)

    logger.info("Automation script finished.")