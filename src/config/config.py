import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# URLs and website related config
WEB_URL = 'https://github.com/login'  # The URL for the website you want to automate
USERNAME = os.getenv('GIT_USERNAME')  # Replace with your credentials
PASSWORD = os.getenv('GIT_PASSWORD')  # Replace with your credentials

