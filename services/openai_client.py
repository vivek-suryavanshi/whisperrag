import os
from langfuse.openai import OpenAI

# Read the OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# If the key is missing, stop the app immediately with a clear error message
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env file")

# Create one OpenAI client that the whole app will share
# Using langfuse.openai instead of openai — this is the only change needed
# Langfuse automatically traces every OpenAI call: cost, latency, input, output
openai_client = OpenAI(api_key=api_key)
