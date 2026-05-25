import os
from openai import OpenAI

# Read the OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# If the key is missing, stop the app immediately with a clear error message
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env file")

# Create one OpenAI client that the whole app will share
# Every router will import this client instead of making their own
openai_client = OpenAI(api_key=api_key)
