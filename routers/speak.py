from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel
from services.openai_client import openai_client

# Create a router for the speak route
router = APIRouter()

# This defines the shape of data we expect from the frontend
class SpeakRequest(BaseModel):
    text: str

# This endpoint receives text and returns spoken audio
@router.post("/speak")
async def speak(request: SpeakRequest):
    # Send the text to OpenAI TTS to convert it into speech
    tts_response = openai_client.audio.speech.create(
        model="tts-1",        # the TTS model
        voice="nova",         # Nova is a warm, natural sounding voice
        input=request.text    # the text we want spoken out loud
    )

    # Read the audio content as raw bytes
    audio_bytes = tts_response.content

    # Return the audio as an MP3 file response
    # The frontend will receive this and play it directly in the browser
    return Response(
        content=audio_bytes,
        media_type="audio/mpeg"
    )
