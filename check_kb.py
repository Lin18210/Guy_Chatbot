import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

print("Fetching latest Knowledge Base...")
response = supabase.table('prompts').select("*").eq('name', 'knowledge_base').order('created_at', desc=True).limit(1).execute()

if response.data:
    kb = response.data[0]['prompt']
    print("\n=== CURRENT KNOWLEDGE BASE ===")
    print(kb)
    print("\n=== CHECK ===")
    print(f"Contains contact? {bool('guyheartphotography11@gmail.com' in kb)}")
    print(f"Contains booking? {bool('book_appointment' in kb)}")
else:
    print("No knowledge base found!")
