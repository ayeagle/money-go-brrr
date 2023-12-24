import requests

# Step 1: Identify Your Chrome Browser Version
chrome_version = input("Enter your Chrome browser version (e.g., 72.0.3626.81): ")

# Step 2: Construct the LATEST_RELEASE URL
latest_release_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_version.split('.')[0]}"

# Step 3: Retrieve the ChromeDriver Version
try:
    response = requests.get(latest_release_url)
    chrome_driver_version = response.text.strip()
    print(f"ChromeDriver version to use: {chrome_driver_version}")
except Exception as e:
    print(f"Error retrieving ChromeDriver version: {e}")
    exit(1)

# Step 4: Construct the URL to Download ChromeDriver
chrome_driver_url = f"https://chromedriver.storage.googleapis.com/{chrome_driver_version}/chromedriver_mac64.zip"

# Step 5: Download ChromeDriver
try:
    response = requests.get(chrome_driver_url)
    with open(f"chromedriver_{chrome_driver_version}.zip", "wb") as driver_file:
        driver_file.write(response.content)
    print(f"ChromeDriver {chrome_driver_version} downloaded successfully.")
except Exception as e:
    print(f"Error downloading ChromeDriver: {e}")
    exit(1)
