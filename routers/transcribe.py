from fastapi import APIRouter, UploadFile, File, HTTPException
from services.openai_client import openai_client

# Create a router — this is like a mini app that handles transcription routes
router = APIRouter()

# This endpoint receives an audio file and returns the transcribed text
@router.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    # Check that the uploaded file is an audio file
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be an audio file"
        )

    # Read the raw bytes of the audio file
    audio_bytes = await audio_file.read()

    # Prepare the file in the format OpenAI Whisper expects
    # It needs a tuple of (filename, file bytes, content type)
    audio_tuple = (audio_file.filename, audio_bytes, audio_file.content_type)

    # Send the audio to OpenAI Whisper for transcription
    transcription_response = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_tuple
    )

    # Extract the transcribed text from the response
    transcribed_text = transcription_response.text

    # Return the transcribed text to the frontend
    return {"text": transcribed_text}
