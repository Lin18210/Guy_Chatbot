import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.environ.get("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("--- Gemini Models ---")
        found = False
        for m in data.get('models', []):
            if "gemini" in m['name'].lower():
                print(m['name'])
                found = True
        if not found:
            print("No models with 'gemini' in name found.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Request Failed: {e}")
