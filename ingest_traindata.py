import os
from pypdf import PdfReader
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

# Supabase Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

PDF_PATH = r"c:\Developement\ChatBot\Traindata\Guy Heart Photography Competitor Summary and Pricing.pdf"

def extract_text_from_pdf(pdf_path):
    print(f"📄 Reading {pdf_path}...")
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(f"✅ Extracted {len(text)} characters.")
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

def append_knowledge_to_supabase(new_text):
    print("📞 Fetching current Knowledge Base...")
    try:
        # Get the latest KB
        response = supabase.table('prompts').select("*").eq('name', 'knowledge_base').order('created_at', desc=True).limit(1).execute()
        
        current_kb = ""
        if response.data:
            current_kb = response.data[0]['prompt']
            print("✅ Found existing Knowledge Base.")
        else:
            print("⚠️ No existing Knowledge Base found. Creating new...")

        # Simple duplicate check (very basic)
        if new_text[:50] in current_kb:
            print("⚠️ This data might already be in the Knowledge Base. Appending anyway for safety, but check for duplicates.")
            
        # Append new info
        updated_kb = current_kb + "\n\n### PRICING AND PACKAGES ###\n" + new_text
        
        # Save as new entry
        data = {
            "name": "knowledge_base",
            "prompt": updated_kb,
            "metadata": {"reason": "Added Pricing and Packages from PDF"}
        }
        
        supabase.table('prompts').insert(data).execute()
        print("✅ Pricing data appended to Knowledge Base successfully!")
        
    except Exception as e:
        print(f"❌ DB Error: {e}")

if __name__ == "__main__":
    if os.path.exists(PDF_PATH):
        content = extract_text_from_pdf(PDF_PATH)
        if content:
            append_knowledge_to_supabase(content)
    else:
        print(f"❌ File not found: {PDF_PATH}")
