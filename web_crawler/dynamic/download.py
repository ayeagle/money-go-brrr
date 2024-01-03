from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# # Initialize the web driver (e.g., Chrome or Firefox)
# driver = webdriver.Chrome(executable_path='/Users/AlexanderYeagle/Desktop/chromedriver/chromedriver_mac_arm64')

# # Navigate to the web page with the download button
# driver.get('https://trends.google.as/trends/explore?q=Celtics&date=now%201-d&geo=US&hl=en-US')

# Replace 'path/to/chromedriver' with the actual path to your chromedriver executable
chrome_driver_path = '/Users/AlexanderYeagle/Desktop/chromedriver/chromedriver_mac_arm64'

# Set the Chrome WebDriver service
service = Service(chrome_driver_path)

# Initialize the web driver with the specified service
driver = webdriver.Chrome(service=service)



try:
    # Find all download buttons on the page
    download_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//button[contains(text(), "Download")]'))
    )

    # Click the first download button (index 0)
    if download_buttons:
        download_buttons[0].click()

        # Wait for the download to complete (you may need to adjust the sleep duration)
        import time
        time.sleep(5)  # Wait for 5 seconds (adjust as needed)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the web browser
    driver.quit()
