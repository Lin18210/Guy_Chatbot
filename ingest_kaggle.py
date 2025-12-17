import kagglehub
import pandas as pd
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Config
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=os.environ.get("MISTRAL_API_KEY"),
)
MODEL_NAME = "mistralai/devstral-2512:free"

# 2. Download Data
print("⬇️ Downloading Kaggle Dataset...")
path = kagglehub.dataset_download("ddosad/ecommerce-customer-service-satisfaction")
# The download returns a folder path. We need to find the CSV inside.
csv_path = os.path.join(path, "Customer_support_data.csv")

# 3. Load & Clean
print(f"📂 Loading {csv_path}...")
df = pd.read_csv(csv_path)

# Drop rows where 'Customer_Remarks' is missing
df = df.dropna(subset=['Customer_Remarks'])


keywords = ['late', 'waiting', 'rude', 'price', 'cost', 'expensive', 'refund', 'money', 'service', 'time']
pattern = '|'.join(keywords)
relevant_df = df[df['Customer_Remarks'].str.contains(pattern, case=False, na=False)].head(20) # Limit to 20 for testing

print(f"✅ Found {len(relevant_df)} relevant customer complaints.")

# 4. The "Synthetic" Generator
new_training_data = []

print("🧠 Synthesizing 'Guy Heart' responses...")

system_instruction = """
You are Guy, the lead photographer at Guy Heart Photography. 
Your style is warm, artistic, and candid. 
You keep replies short, friendly, and professional.
Use emojis sparingly (📷, ✨).
If a customer complains about 'shipping' or 'delivery', assume they mean 'photo gallery delivery'.
"""

for index, row in relevant_df.iterrows():
    customer_input = row['Customer_Remarks']
    
    # Ask the AI to write the IDEAL response
    prompt = f"Customer says: '{customer_input}'. Write a response."
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ]
        )
        ai_reply = completion.choices[0].message.content
        
        # Add to my dataset
        entry = {
            "client_sequence": customer_input,
            "chat_history": [],
            "real_consultant_reply": ai_reply 
        }
        new_training_data.append(entry)
        print(f"   Generated pair #{len(new_training_data)}")
        
    except Exception as e:
        print(f"   Error generating row: {e}")

# 5. Save to File
output_file = "kaggle_conversations.py"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("# Auto-generated from Kaggle Dataset\n\n")
    f.write("kaggle_data = " + json.dumps(new_training_data, indent=4))

print(f"🎉 Success! Generated {len(new_training_data)} training examples in {output_file}")