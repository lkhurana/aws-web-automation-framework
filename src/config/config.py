import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# URLs and website related config
WEB_URL = 'https://github.com/login'  # The URL for the website you want to automate
USERNAME = os.getenv('GIT_USERNAME')  # Replace with your credentials
PASSWORD = os.getenv('GIT_PASSWORD')  # Replace with your credentials

# Email related config
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')