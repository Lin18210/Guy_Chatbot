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

def save_knowledge_to_supabase(text):
    print("💾 Saving to Supabase as 'knowledge_base'...")
    data = {
        "name": "knowledge_base",
        "prompt": text,
        "metadata": {"source": "Guy Heart Photography Competitor Summary and Pricing.pdf"}
    }
    
    try:
        supabase.table('prompts').insert(data).execute()
        print("✅ Saved successfully!")
    except Exception as e:
        print(f"❌ DB Error: {e}")

if __name__ == "__main__":
    if os.path.exists(PDF_PATH):
        content = extract_text_from_pdf(PDF_PATH)
        if content:
            save_knowledge_to_supabase(content)
    else:
        print(f"❌ File not found: {PDF_PATH}")
