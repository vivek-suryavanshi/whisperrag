# WhisperRAG V2 — Project Bible

## 1. What This App Does
WhisperRAG is a voice RAG chatbot.
- User pastes a webpage URL
- User speaks a question by voice
- AI reads the webpage and answers out loud
- Answers are grounded in the webpage only — no hallucination

Live V1 version: https://whisperrag.streamlit.app
GitHub V1: https://github.com/vivek-suryavanshi/whisperrag

---

## 2. Why V2 Exists — What Broke in V1
V1 was built on Streamlit. These problems were identified:
- Audio autoplay blocked by browser — needed a "Continue" button hack
- Page reruns on every single interaction — bad for voice UX
- Mic state was unclear — user didn't know if recording or idle
- URL limit was bypassable — just refresh and limit resets
- Clear conversation did not clear RAG context — a bug
- Everything in one file (app.py) — hard to maintain or scale
- No separation of concerns — UI and logic mixed together

V2 fixes all of these properly.

---

## 3. UI Design — MUST Follow Exactly

### Theme
- Light white background — NOT dark
- Clean minimal — no clutter
- Font: system sans-serif

### Layout — Two columns
Left sidebar (260px wide):
- WhisperRAG logo + microphone icon at top
- URL input field with placeholder "https://example.com"
- Load Page button — purple #7F77DD
- Active page indicator when URL is loaded — shows page title not raw URL
- Clear conversation button at bottom

Right main area:
- Mode banner at top
  Green background when webpage loaded — "Web RAG mode"
  Blue background when no webpage — "General mode"
- Chat history in middle
  User messages — right aligned, purple #7F77DD background
  AI messages — left aligned, grey #F5F5F5 background
  Audio player embedded inside AI message bubble
- Single large mic button centred at bottom (64px circle)
- Transcription text shown above mic button after recording

### Mic Button — 4 States
- Idle: grey #E0E0E0 circle, microphone icon, "Click to speak"
- Recording: red #E24B4A circle, pulsing animation, "Recording..."
- Thinking: purple #7F77DD circle, spinning animation, "Thinking..."
- Speaking: green #1D9E75 circle, wave animation, "Speaking..."

### What is NOT in the UI
- NO text input box
- NO separate Continue button
- NO dark theme
- NO multiple input options confusing the user

---

## 4. Tech Stack

Backend: FastAPI Python
Frontend: Single HTML/JS file served by FastAPI
STT: OpenAI Whisper (whisper-1)
LLM: OpenAI GPT-4o-mini
TTS: OpenAI TTS Nova voice
Scraping: requests + BeautifulSoup4
Deploy: Render (later)

One API key needed — OPENAI_API_KEY only for MVP.

---

## 5. File Structure

whisperrag-v2/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── transcribe.py
│   ├── chat.py
│   ├── speak.py
│   └── scrape.py
├── services/
│   ├── __init__.py
│   ├── openai_client.py
│   └── scraper.py
├── static/
│   └── index.html
├── requirements.txt
├── .env.example
├── CLAUDE.md
└── README.md

---

## 6. Build Order — ONE FILE AT A TIME

Build in this exact order:
1. CLAUDE.md — this file (done)
2. requirements.txt
3. .env.example
4. main.py
5. services/__init__.py
6. services/openai_client.py
7. services/scraper.py
8. routers/__init__.py
9. routers/transcribe.py
10. routers/chat.py
11. routers/speak.py
12. routers/scrape.py
13. static/index.html
14. README.md

After each file:
- Explain what the file does in plain English
- Explain why it exists
- Wait for my approval before next file

---

## 7. Coding Style — STRICT RULES

I am a learner. Follow these rules on every single file:

### Comments
- Add a comment above every function explaining what it does
- Add inline comments on any line that is not obvious
- Use plain English in comments — no jargon

### Code style
- Simple readable variable names — no abbreviations
- No list comprehensions — write full for loops
- No lambda functions — write full def functions
- Break long lines into multiple short lines
- Always use f-strings for string formatting

### Environment variables — always write it this way
import os
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env file")

Never use bash tricks to check environment variables.

### Terminal commands — only simple readable versions
Good: pip install -r requirements.txt
Bad: pip install -r requirements.txt 2>/dev/null && echo "done"

### Before creating each file
1. Tell me the filename
2. Explain what it does in plain English
3. Explain why it exists in the project
4. Show me the code
5. Wait for me to say "yes" or "go ahead"
6. Then create the file

### Never do these
- Never create multiple files at once
- Never run the app unless I ask
- Never push to GitHub
- Never assume — always ask if unsure
- Never use bash one-liners or clever shortcuts

---

## 8. How to Run Locally

# Create virtual environment
python -m venv .venv

# Activate it on Mac
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

# Copy env file and add your key
cp .env.example .env

# Run the server
uvicorn main:app --reload

# Open in browser
http://localhost:8000

---

## 9. API Endpoints

GET    /                 serves index.html frontend
GET    /health           check if server is running
POST   /api/transcribe   audio file to text via Whisper
POST   /api/chat         text and history to GPT reply
POST   /api/speak        text to audio via TTS
POST   /api/scrape       URL to scraped and stored content
DELETE /api/scrape       clear stored webpage content

---

## 10. Key Decisions Made

- OpenAI only — one API key, simplest setup
- No database for MVP — in memory storage is fine
- No user login for MVP — single user demo app
- No automatic GitHub push — manual only
- Render for deployment — free tier, simple
- BeautifulSoup for scraping — simple, no JS rendering needed
- Max 8000 chars from scraped page — token cost control
- Max 5 URLs per session — abuse prevention
- Conversation history — last 10 messages only — token cost control
