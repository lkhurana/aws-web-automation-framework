import logging
from logging.handlers import RotatingFileHandler
from src.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USER_PARAM_NAME,
    SMTP_PASS_PARAM_NAME
)
from src.utils import send_email, get_credential

def setup_logging(log_filename):
    """
    Set up logging configuration for the project.

    This function configures logging with a rotating file handler and a console handler.
    The log file is cleared each time the function is called, and new log entries are 
    appended to it. Logs are written both to the file and the console, with a maximum file 
    size of 5 MB and up to two backup files being kept. 

    Args:
        log_filename (str): The path to the log file where logs will be written.

    Returns:
        logging.Logger: A logger instance configured with the specified handlers.
    """
    # Clear the log file (open in write mode to truncate)
    open(log_filename, 'w').close()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create file handler
    file_handler = RotatingFileHandler(log_filename, maxBytes=5*1024*1024, backupCount=2)  # 5 MB per file
    file_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Add a console handler, so that the logs appear on the console in addition to the file
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def send_log_email(log_filename, recipient_email, subject = 'Automation Script Logs'):
    """
    Send the contents of the log file as an email.

    This function reads the contents of a specified log file and sends them as the 
    body of an email to a designated recipient. The email credentials are retrieved 
    from AWS Parameter Store to ensure secure access. If the email fails to send, 
    an error is logged.

    Args:
        log_filename (str): The path to the log file to be read and sent.
        recipient_email (str): The recipient's email address.
        subject (str): The subject line for the email (default is 'Automation Script Logs').

    Returns:
        None
    """
    # Read the log file content
    try:
        with open(log_filename, 'r') as log_file:
            log_content = log_file.read()
        
        send_email(subject, log_content, recipient_email, SMTP_SERVER, SMTP_PORT, get_credential(SMTP_USER_PARAM_NAME), get_credential(SMTP_PASS_PARAM_NAME))
        logging.info("Log email sent successfully.")

    except Exception as e:
        #logging.error(f"Failed to send email: {str(e)}")
        logging.error("Failed to send email.")