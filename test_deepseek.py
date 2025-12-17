import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

api_key = os.environ.get("Deepseek_API_KEY")
print(f"DeepSeek Key: {api_key[:10]}...")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

model = "tngtech/deepseek-r1t2-chimera:free"

print(f"Testing model: {model}")

try:
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Hello, are you working?"}],
    )
    print("Success:", completion.choices[0].message.content)
except Exception as e:
    print(f"Failed: {e}")
