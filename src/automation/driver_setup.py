from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_driver():
    """
    Initializes and returns a headless Chrome WebDriver instance.

    This function configures Chrome options for headless operation, disables
    sandboxing, and reduces shared memory usage, making it suitable for environments
    with limited display and memory resources (such as server-based or CI environments).
    The ChromeDriver executable is automatically installed and managed.

    Returns:
        selenium.webdriver.Chrome: A Chrome WebDriver instance with configured options.
    """
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless if not debugging
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    return driver