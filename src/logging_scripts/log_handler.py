import logging
from logging.handlers import RotatingFileHandler
from src.config.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USER_PARAM_NAME,
    SMTP_PASS_PARAM_NAME
)
from src.utils import send_email, get_credential

def setup_logging(log_filename):
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
    # Read the log file content
    try:
        with open(log_filename, 'r') as log_file:
            log_content = log_file.read()
        
        send_email(subject, log_content, recipient_email, SMTP_SERVER, SMTP_PORT, get_credential(SMTP_USER_PARAM_NAME), get_credential(SMTP_PASS_PARAM_NAME))
        logging.info("Log email sent successfully.")

    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")