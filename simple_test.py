import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    print(f"Testing Gemini Flash with key: {api_key[:10]}...")
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hello"
    )
    print("Success:", response.text)
except Exception as e:
    print(f"Failed: {e}")
