import logging
from logging.handlers import RotatingFileHandler

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