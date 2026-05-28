import os
from supabase import create_client

# Load Supabase credentials from environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

# Raise clear errors if credentials are missing
if not supabase_url:
    raise ValueError("SUPABASE_URL is not set in .env file")
if not supabase_key:
    raise ValueError("SUPABASE_SERVICE_KEY is not set in .env file")

# Create the Supabase client — used for all database operations
supabase = create_client(supabase_url, supabase_key)


# This function creates a new session row when a URL is loaded
# Returns the session ID so we can link messages to it
def create_session(url, domain, page_title, scraped_chars):
    # Insert a new row into the sessions table
    result = supabase.table("sessions").insert({
        "url": url,
        "domain": domain,
        "page_title": page_title,
        "scraped_chars": scraped_chars
    }).execute()

    # Return the ID of the newly created session
    return result.data[0]["id"]


# This function logs a question and answer to the messages table
# session_id links this message to the session it belongs to
def log_message(session_id, question, answer, gpt_latency_ms, total_latency_ms):
    # Insert a new row into the messages table
    supabase.table("messages").insert({
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "gpt_latency_ms": gpt_latency_ms,
        "total_latency_ms": total_latency_ms
    }).execute()
