import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Import all the routers (each handles a different part of the API)
from routers import transcribe, chat, speak, scrape

# Create the FastAPI app with a name and description
app = FastAPI(
    title="WhisperRAG V2",
    description="A voice RAG chatbot powered by OpenAI"
)

# Connect each router to the app under the /api path
app.include_router(transcribe.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(speak.router, prefix="/api")
app.include_router(scrape.router, prefix="/api")

# Serve the static folder so the browser can load index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

# This route serves the frontend when someone visits http://localhost:8000
@app.get("/")
def serve_frontend():
    # Return the index.html file from the static folder
    return FileResponse("static/index.html")

# This route is a simple health check — useful to confirm the server is running
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "WhisperRAG V2 is running"}
