import subprocess
import requests
import sys

# Step 1: Identify Your Chrome Browser Version
try:
    # Use subprocess to run the appropriate command based on the OS
    if sys.platform == "darwin":  # macOS
        chrome_version = subprocess.check_output(
            ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
            universal_newlines=True
        ).strip()
        print(chrome_version)
    elif sys.platform == "linux" or sys.platform == "linux2":  # Linux
        chrome_version = subprocess.check_output(
            ["google-chrome", "--version"],
            universal_newlines=True
        ).strip()
    else:
        raise ChromeVersionError("Unsupported OS")
except Exception as e:
    print(f"Error retrieving Chrome version: {e}")
    exit(1)

# Step 2: Construct the LATEST_RELEASE URL
latest_release_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_version.split('.')[0]}"

# Rest of the script remains the same as in the previous response
