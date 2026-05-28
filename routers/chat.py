from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import time
from services.openai_client import openai_client
from services.database import log_message
from routers.scrape import session_data

# Create a router for chat routes
router = APIRouter()

# This defines the shape of data we expect from the frontend
class ChatRequest(BaseModel):
    user_message: str
    conversation_history: List[dict]
    webpage_content: str = ""

# This endpoint receives a message and returns the AI reply
@router.post("/chat")
async def chat(request: ChatRequest):
    # Safety net — this should not happen because the frontend disables
    # the mic until a URL is loaded, but we handle it gracefully just in case
    if not request.webpage_content:
        return {"reply": "Please load a webpage first, then ask me a question about it."}

    # WhisperRAG is a RAG-only app — the AI must stay focused on the webpage
    # We explicitly tell it to refuse off-topic questions so users cannot
    # use it as a general chatbot (e.g. ask for jokes, general knowledge etc.)
    system_prompt = f"""You are WhisperRAG, a voice assistant that answers questions strictly based on the webpage content provided below.

Your only job is to help the user understand and explore the content of the loaded webpage.

Rules you must follow:
- Only answer questions that are directly about the webpage content below
- When the user says "this", "the page", "the article", "the website", "the content", "extract" — they mean the webpage below
- If a specific fact is not in the content, say "I could not find that in the article"
- If the user asks something completely unrelated to the webpage (jokes, general knowledge, maths, etc.), say "I can only answer questions about the loaded webpage. Try asking me something about it."
- Do not invent or guess facts that are not present in the content
- Keep answers clear and concise — this is a voice app, so avoid bullet points and markdown

Webpage content:
{request.webpage_content}"""

    # Start building the messages list with the system prompt
    messages = []
    messages.append({"role": "system", "content": system_prompt})

    # Add the conversation history so the AI remembers previous messages
    for history_message in request.conversation_history:
        messages.append(history_message)

    # Add the latest user message at the end
    messages.append({"role": "user", "content": request.user_message})

    # Only keep the last 10 messages to control token costs
    # We always keep the system prompt (index 0) plus the last 10 messages
    if len(messages) > 11:
        recent_messages = messages[1:][-10:]
        messages = [messages[0]] + recent_messages

    # Record the start time so we can measure GPT latency
    gpt_start = time.time()

    # Send everything to GPT-4o-mini and get a response
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Calculate how long the GPT call took in milliseconds
    gpt_latency_ms = int((time.time() - gpt_start) * 1000)

    # Extract the AI's reply text from the response
    ai_reply = response.choices[0].message.content

    # Log this message to Supabase — silently, doesn't affect the user
    # total_latency_ms is the same as gpt_latency_ms for now
    # (we can add Whisper + TTS latency later)
    try:
        log_message(
            session_id=session_data["session_id"],
            question=request.user_message,
            answer=ai_reply,
            gpt_latency_ms=gpt_latency_ms,
            total_latency_ms=gpt_latency_ms
        )
    except Exception as db_error:
        # Log the error but don't break the app — DB logging is non-critical
        print(f"Supabase logging error: {str(db_error)}")

    # Return the reply to the frontend
    return {"reply": ai_reply}
