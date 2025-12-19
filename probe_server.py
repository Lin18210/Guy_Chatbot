
import requests

try:
    response = requests.get("http://127.0.0.1:5000/")
    print(f"Status: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
