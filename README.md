# WhisperRAG

A voice RAG chatbot. Paste a webpage URL, ask a question by voice, get a spoken answer grounded in that page.

## What it does
- Paste any webpage URL and click Load page
- Speak your question
- AI reads the page and answers out loud
- Answers are strictly grounded in the loaded page — no hallucination, no general chatbot

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: Single HTML/JS file served by FastAPI
- Speech to Text: OpenAI Whisper
- AI replies: OpenAI GPT-4o-mini
- Text to Speech: OpenAI TTS Nova
- Scraping: requests + BeautifulSoup4
- Database: Supabase (Postgres) — session and message logging
- LLM Observability: Langfuse — cost, latency, and trace tracking

## Setup

### 1. Clone the repo
```
git clone https://github.com/vivek-suryavanshi/whisperrag.git
cd whisperrag
```

### 2. Create a virtual environment
```
python -m venv .venv
```

### 3. Activate it (Mac)
```
source .venv/bin/activate
```

### 4. Install packages
```
pip install -r requirements.txt
```

### 5. Add your API keys
```
cp .env.example .env
```
Open `.env` and fill in your keys:
- **OpenAI** — https://platform.openai.com/api-keys
- **Supabase** — your project URL + service key from supabase.com
- **Langfuse** — public + secret key from us.cloud.langfuse.com

### 6. Run the server
```
uvicorn main:app --reload
```

### 7. Open in browser
```
http://localhost:8000
```

## How to use
1. Paste a webpage URL in the sidebar and click **Load page**
2. Click the mic button, speak your question
3. The AI answers based on that page and speaks the reply out loud
4. Ask follow-up questions — conversation history is kept
5. Click **Clear conversation** to reset and load a new page

## API Endpoints
| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | / | Serves the frontend |
| GET | /health | Check if server is running |
| POST | /api/transcribe | Audio to text via Whisper |
| POST | /api/chat | Text + history to GPT reply |
| POST | /api/speak | Text to audio via TTS |
| POST | /api/scrape | Scrape and store a URL |
| DELETE | /api/scrape | Clear stored webpage content |

## Limits
- Max 15 URLs per session
- Max 8000 characters scraped per page
- Last 10 messages kept in conversation history
