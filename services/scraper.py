import requests
from bs4 import BeautifulSoup

# Maximum number of characters we will take from a webpage
# This keeps OpenAI token costs under control
MAX_CHARS = 8000

# This function takes a URL and returns clean text from that webpage
def scrape_webpage(url):
    # Fetch the raw HTML from the URL
    response = requests.get(url, timeout=10)

    # Raise an error if the request failed (e.g. 404, 500)
    response.raise_for_status()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style tags — we don't want code or CSS in our text
    for unwanted_tag in soup(["script", "style"]):
        unwanted_tag.decompose()

    # Extract all the visible text from the page
    raw_text = soup.get_text()

    # Clean up the text line by line
    cleaned_lines = []
    for line in raw_text.splitlines():
        # Strip extra whitespace from each line
        stripped_line = line.strip()
        # Only keep lines that actually have content
        if stripped_line:
            cleaned_lines.append(stripped_line)

    # Join all the clean lines into one block of text
    full_text = "\n".join(cleaned_lines)

    # Trim to the maximum character limit to control token usage
    trimmed_text = full_text[:MAX_CHARS]

    return trimmed_text
