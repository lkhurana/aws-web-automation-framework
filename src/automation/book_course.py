from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from src.utils import get_weekday_int

BOOKING_URL = "https://mein.fitnessfirst.de/member/courses"
weekdays_de = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']


def book_BikeIntense(logger,driver):
    try:
        booking_status = "Attempt started"

        logger.info(f'Navigating to {BOOKING_URL}...')
        driver.get(BOOKING_URL)
        time.sleep(5)

        look_for_weekday = get_weekday_int()+1
        weekday_de = weekdays_de[look_for_weekday]
        logger.info(f'Looking for BikeIntense course on {weekday_de}')

        # Get the current time (in seconds) and set the duration of attempts
        start_time = time.time()
        attempts = 0
        duration = 10 * 60  # 10 minutes in seconds

        while (time.time() - start_time) < duration:
                try:
                    # Locate the button based on its class and text content
                    course_button = driver.find_element(By.XPATH,"//button[contains(@class, 'btn btn-secondary btn-class-select') and contains(text(), 'BikeIntense')]")
                    # Click the button to select the course
                    course_button.click()
                    time.sleep(random.uniform(5, 10))

                    look_for_element = driver.find_element(By.XPATH, f"//a[contains(@id, '{weekday_de}')]/ancestor::div[1]/following-sibling::div[1][contains(@class, 'card')]")
                    logger.info(f'Element for {weekday_de} found. Card ID: {str(look_for_element.get_attribute("id"))}')

                    # Try to locate the booking button
                    button = look_for_element.find_element(By.XPATH, ".//button[contains(@class, 'btn btn-primary')]")
                    logger.info('Booking button found!')

                    # Get the button's text
                    button_text = button.text.strip()

                    # Check if the button's text contains "buchen"
                    if "buchen" in button_text:
                        button.click()  # Click the button if it says "buchen"
                        logger.info("Booking button clicked!")
                        booking_status = f"Success! Booked the BikeIntense course for {weekday_de}"
                    else:
                        logger.info(f"Button says '{button_text}', not clicking.")
                        booking_status = f"Reminder: You have booked the BikeIntense course for {weekday_de}"
                    break

                except:
                    # If button not found, refresh the page
                    logger.info(f'Booking button not found.. Refreshing the page... (Attempt {attempts + 1})')
                    booking_status = f"Booking button not found for {weekday_de}!"
                    driver.refresh()
                    time.sleep(random.uniform(5,12))
                    attempts += 1

                raise Exception("Failed to locate the booking button after multiple attempts.")
            
        time.sleep(random.uniform(10, 20))

    finally:
        logger.info(f"Current URL after course booking attempt: {driver.current_url}")
        return booking_status
