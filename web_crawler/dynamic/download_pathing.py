import os
import zipfile

import requests

# Latest release URL for ChromeDriver
latest_release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"

try:
    # Send a GET request to the latest release URL
    response = requests.get(latest_release_url)
    response.raise_for_status()

    # Get the version of ChromeDriver from the response
    chrome_driver_version = response.text.strip()

    # Construct the URL to download ChromeDriver
    download_url = f"https://chromedriver.storage.googleapis.com/{chrome_driver_version}/chromedriver_mac64.zip"

    # Specify the path to save the downloaded ZIP file
    download_path = "chromedriver_mac64.zip"

    # Send a GET request to download ChromeDriver
    response = requests.get(download_url)
    response.raise_for_status()

    # Save the ZIP file to the specified path
    with open(download_path, "wb") as file:
        file.write(response.content)

    # Extract the contents of the ZIP file
    with zipfile.ZipFile(download_path, "r") as zip_ref:
        zip_ref.extractall("/path/to/chromedriver/directory")

    print(f"ChromeDriver version {chrome_driver_version} downloaded and extracted successfully.")

    # Remove the downloaded ZIP file
    os.remove(download_path)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
