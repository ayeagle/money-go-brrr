import requests
from bs4 import BeautifulSoup

# Define the search query
search_query = "your search keyword"

# Create a user agent to mimic a web browser (optional)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.0.0 Safari/537.36"
}

# Perform a Google search
url = f"https://www.google.com/search?q={search_query}"
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the search results
    soup = BeautifulSoup(response.text, "html.parser")

    print(soup)

    # Find and extract search result links
    search_results = soup.find_all("a", href=True)

    # Print the search result links
    for link in search_results:
        print(link["href"])
else:
    print("Failed to retrieve search results")
