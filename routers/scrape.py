from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scraper import scrape_webpage

# Create a router for scrape routes
router = APIRouter()

# Maximum number of URLs allowed per session — abuse prevention
MAX_URLS_PER_SESSION = 5

# In-memory storage — stores the current webpage content and session info
# This resets every time the server restarts (fine for MVP)
session_data = {
    "webpage_content": "",   # the scraped text from the current URL
    "page_title": "",        # the title of the loaded page
    "urls_loaded": 0         # how many URLs have been loaded this session
}

# This defines the shape of data we expect from the frontend
class ScrapeRequest(BaseModel):
    url: str

# This endpoint receives a URL, scrapes it, and stores the content
@router.post("/scrape")
async def load_webpage(request: ScrapeRequest):
    # Check if the user has hit the URL limit for this session
    if session_data["urls_loaded"] >= MAX_URLS_PER_SESSION:
        raise HTTPException(
            status_code=429,
            detail=f"Maximum of {MAX_URLS_PER_SESSION} URLs allowed per session"
        )

    # Scrape the webpage using our scraper service
    scraped_text = scrape_webpage(request.url)

    # Store the scraped content in memory
    session_data["webpage_content"] = scraped_text

    # Extract a simple page title from the URL to show in the sidebar
    # We just use the domain name as the title for now
    url_parts = request.url.replace("https://", "").replace("http://", "")
    page_title = url_parts.split("/")[0]
    session_data["page_title"] = page_title

    # Increment the URL counter for this session
    session_data["urls_loaded"] = session_data["urls_loaded"] + 1

    # Return confirmation to the frontend
    return {
        "message": "Webpage loaded successfully",
        "page_title": page_title,
        "character_count": len(scraped_text)
    }

# This endpoint returns the currently stored webpage content
# The chat router uses this to get the RAG context
@router.get("/scrape")
async def get_webpage_content():
    return {
        "webpage_content": session_data["webpage_content"],
        "page_title": session_data["page_title"]
    }

# This endpoint clears the stored webpage content
# Called when the user clicks "Clear conversation"
@router.delete("/scrape")
async def clear_webpage():
    # Wipe the stored content — fixes the V1 bug where clear didn't clear RAG
    session_data["webpage_content"] = ""
    session_data["page_title"] = ""

    # Return confirmation
    return {"message": "Webpage content cleared"}
