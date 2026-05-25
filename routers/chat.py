from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.openai_client import openai_client

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
    # Build the system prompt depending on whether a webpage is loaded
    if request.webpage_content:
        # Web RAG mode — AI must answer using only the webpage content
        system_prompt = f"""You are a helpful assistant that answers questions based only on the webpage content provided below.
If the answer is not found in the webpage content, say "I could not find that information on this page."
Do not use any outside knowledge.

Webpage content:
{request.webpage_content}"""
    else:
        # General mode — no webpage loaded, AI answers freely
        system_prompt = "You are a helpful assistant. Answer the user's questions clearly and concisely."

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

    # Send everything to GPT-4o-mini and get a response
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Extract the AI's reply text from the response
    ai_reply = response.choices[0].message.content

    # Return the reply to the frontend
    return {"reply": ai_reply}
