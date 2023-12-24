from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--no-sandbox")  # Disable sandbox mode (may be required on some systems)

# Initialize ChromeDriver with the specified options
driver = webdriver.Chrome(executable_path='/path/to/chromedriver', chrome_options=chrome_options)

# Your Selenium automation code here

# Close the browser when done
driver.quit()
