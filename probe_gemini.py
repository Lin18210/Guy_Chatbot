import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

api_key = os.environ.get("GEMINI_API_KEY")
print(f"Key: {api_key[:10]}...")

client = genai.Client(api_key=api_key)

models_to_try = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-pro",
    "models/gemini-1.5-flash"
]

print("--- Probing Models ---")
for model_name in models_to_try:
    print(f"\nTrying: {model_name}")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Ping",
        )
        print(f"SUCCESS with {model_name}: {response.text}")
        break 
    except Exception as e:
        print(f"FAILED {model_name}: {e}")
