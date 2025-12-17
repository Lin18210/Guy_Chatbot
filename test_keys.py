import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

print("--- Testing Gemini API ---")
gemini_key = os.environ.get("GEMINI_API_KEY")

if not gemini_key:
    print("ERROR: GEMINI_API_KEY not found in environment.")
    exit(1)

print(f"Gemini Key: {gemini_key[:10]}... (Loaded)")

client = genai.Client(api_key=gemini_key)

print("\n1. Listing Available Models:")
try:
    for m in client.models.list():
        if "gemini" in m.name:
            print(f" - {m.name}")
except Exception as e:
    print(f"Listing failed: {e}")

print("\n2. Testing Generation (gemini-2.0-flash-exp):")
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Hello, are you working?",
    )
    print("Success:", response.text)
except Exception as e:
    print(f"Failed: {e}")

print("\n3. Testing Generation (gemini-1.5-flash):")
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hello, are you working?",
    )
    print("Success:", response.text)
except Exception as e:
    print(f"Failed: {e}")
