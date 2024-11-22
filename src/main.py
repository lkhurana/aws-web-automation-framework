from src.log_handler import setup_logging, send_log_email
from src.automation.driver_setup import get_driver
from src.automation.login import automate_login
from src.automation.book_course import book_BikeIntense
from src.utils import get_credential
from src.config import RECIPIENT_PARAM_NAME

if __name__ == "__main__":
    # Initialize logging
    LOG_FILENAME = 'automation_script.log'
    logger = setup_logging(LOG_FILENAME)

    # Set up the WebDriver
    logger.info('Initializing Chrome driver...')
    driver = get_driver()

    # Run the automation
    logger.info("Starting the automation script...")
    automate_login(logger, driver)
    booking_status = book_BikeIntense(logger, driver)

    # Send logs via email
    logger.info("Sending logs via email...")
    send_log_email(LOG_FILENAME, get_credential(RECIPIENT_PARAM_NAME), booking_status)

    # Close the WebDriver
    driver.quit()
    logger.info('Chrome driver closed. Script ended.')
    logger.info("Automation script finished.")