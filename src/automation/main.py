
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Enter your credentials 
USERNAME = "test@example.com"  # Replace with your GitHub username
PASSWORD = "password"  # Replace with your GitHub password
WEB_URL = 'https://github.com/login'

# Set up the WebDriver
print('Initializing Chrome driver...')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    # Open GitHub login page
    print('Opening login page...')
    driver.get(WEB_URL)

    # Wait for the page to load
    time.sleep(2)

    # Locate the username and password fields and sign-in button
    username_input = driver.find_element(By.ID, "login_field")
    password_input = driver.find_element(By.ID, "password")
    sign_in_button = driver.find_element(By.NAME, "commit")

    # Fill in the login form
    print('Entering user credentials...')
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    # Click the sign-in button
    sign_in_button.click()
    print('Sign in button clicked.')

    # Wait for a while to observe the result
    time.sleep(5)

finally:
    print(f"Current URL after login: {driver.current_url}")

    # Close the WebDriver
    driver.quit()
    print('Chrome driver closed. Script ended.')
