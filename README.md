# WhisperRAG V2 🎙️

A voice RAG chatbot. Paste a URL, ask a question by voice, get a spoken answer grounded in that webpage.

## What it does
- User pastes a webpage URL
- User speaks a question
- AI reads the webpage and answers out loud
- Answers are grounded in the webpage only — no hallucination

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: Single HTML/JS file
- Speech to Text: OpenAI Whisper
- AI replies: OpenAI GPT-4o-mini
- Text to Speech: OpenAI TTS Nova voice
- Scraping: BeautifulSoup4

## Setup

### 1. Clone the repo
git clone https://github.com/your-username/whisperrag-v2
cd whisperrag-v2

### 2. Create a virtual environment
python -m venv .venv

### 3. Activate it (Mac)
source .venv/bin/activate

### 4. Install packages
pip install -r requirements.txt

### 5. Add your API key
cp .env.example .env

Then open .env and replace the placeholder with your real OpenAI API key.
Get your key here: https://platform.openai.com/api-keys

### 6. Run the server
uvicorn main:app --reload

### 7. Open in browser
http://localhost:8000

## How to use
1. Paste a webpage URL in the left sidebar and click Load Page
2. Click the microphone button and ask a question
3. The AI will answer based on that webpage and speak the reply out loud
4. Click Clear Conversation to start fresh

## API Endpoints
| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | / | Serves the frontend |
| GET | /health | Check if server is running |
| POST | /api/transcribe | Audio file to text via Whisper |
| POST | /api/chat | Text and history to GPT reply |
| POST | /api/speak | Text to audio via TTS |
| POST | /api/scrape | URL to scraped content |
| DELETE | /api/scrape | Clear stored webpage content |

## Limits
- Max 5 URLs per session
- Max 8000 characters scraped per page
- Last 10 messages kept in conversation history

## V1
Live V1 (Streamlit): https://whisperrag.streamlit.app
V1 GitHub: https://github.com/vivek-suryavanshi/whisperrag
