import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.environ.get("GEMINI_API_KEY")
print(f"Key: {api_key[:10]}...")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print(f"Requesting: {url.replace(api_key, 'HIDDEN_KEY')}")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Models found:")
        for m in data.get('models', []):
            print(f" - {m['name']}")
    else:
        print("Error Response:")
        print(response.text)
except Exception as e:
    print(f"Request Failed: {e}")
