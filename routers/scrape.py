from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from services.scraper import scrape_webpage

# Create a router for scrape routes
router = APIRouter()

# Maximum number of URLs allowed per session — abuse prevention
MAX_URLS_PER_SESSION = 15

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

    # Scrape the webpage — catch errors and return friendly messages to the frontend
    try:
        scrape_result = scrape_webpage(request.url)

    # DNS failure or no network — the domain simply could not be resolved
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=400,
            detail="Could not reach that URL. Check the address and try again."
        )

    # Request took too long — server is slow or unresponsive
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=400,
            detail="The page took too long to respond. Try again or use a different URL."
        )

    # The server responded but with a 4xx or 5xx status code
    except requests.exceptions.HTTPError as error:
        raise HTTPException(
            status_code=400,
            detail=f"The page returned an error ({error.response.status_code}). Try a different URL."
        )

    # Anything else unexpected — SSL error, encoding issue, etc.
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Something went wrong loading that page: {str(error)}"
        )

    # Store the scraped text content in memory for use in chat
    session_data["webpage_content"] = scrape_result["text"]

    # Store the real page title from the HTML <title> tag
    session_data["page_title"] = scrape_result["title"]

    # Increment the URL counter for this session
    session_data["urls_loaded"] = session_data["urls_loaded"] + 1

    # Return confirmation and the real title to the frontend
    return {
        "message": "Webpage loaded successfully",
        "page_title": scrape_result["title"],
        "character_count": len(scrape_result["text"])
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

    # NOTE: urls_loaded is intentionally NOT reset here
    # Resetting it would let users bypass the limit by just clicking Clear

    # Return confirmation
    return {"message": "Webpage content cleared"}
