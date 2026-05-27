import requests
from bs4 import BeautifulSoup

# Maximum number of characters we will take from a webpage
# This keeps OpenAI token costs under control
MAX_CHARS = 8000

# This function takes a URL and returns clean text from that webpage
def scrape_webpage(url):
    # Fetch the raw HTML from the URL
    # We send a User-Agent header so websites don't block us as a bot
    # Many sites (like Wikipedia) return 403 Forbidden without this
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    # timeout=6 — fail fast if the server doesn't respond within 6 seconds
    response = requests.get(url, headers=headers, timeout=6)

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

    # Extract the page title from the HTML <title> tag
    # BeautifulSoup already parsed the HTML above, so this is free
    page_title = ""
    if soup.title and soup.title.string:
        # .string gives us the raw title text — strip trims any surrounding whitespace
        page_title = soup.title.string.strip()

    # If the page has no <title> tag, fall back to the domain name from the URL
    if not page_title:
        url_without_protocol = url.replace("https://", "").replace("http://", "")
        page_title = url_without_protocol.split("/")[0]

    # Return both the scraped text and the real page title together
    return {
        "text": trimmed_text,
        "title": page_title
    }
