import requests
import time
from conversations import sample_data as manual_data

try:
    from kaggle_conversations import kaggle_data
    print(f"📂 Loaded {len(kaggle_data)} Kaggle examples.")
except ImportError:
    kaggle_data = []
    print("⚠️ No Kaggle data found. Run 'ingest_kaggle.py' first.")

# Combine both datasets
full_dataset = manual_data + kaggle_data

BASE_URL = "http://127.0.0.1:5000"

def run_training():
    print(f"🚀 Starting Training Session with {len(full_dataset)} examples...")
    
    for i, item in enumerate(full_dataset):
        print(f"\n--- Processing Item #{i+1} ---")
        
        payload = {
            "clientSequence": item["client_sequence"],
            "chatHistory": item.get("chat_history", []),
            "consultantReply": item["real_consultant_reply"]
        }
        
        try:
            res = requests.post(f"{BASE_URL}/improve-ai", json=payload)
            if res.status_code == 200:
                print("✅ AI Improved!")
            else:
                print("❌ Error:", res.text)
        except Exception as e:
            print(f"Connection Error: {e}")
            
        time.sleep(2) 

if __name__ == "__main__":
    run_training()