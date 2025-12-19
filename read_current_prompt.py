
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not found in environment.")
    exit(1)

supabase: Client = create_client(url, key)

def get_current_prompt():
    """Fetches the latest active prompt from Supabase."""
    try:
        response = supabase.table('prompts').select("*").eq('name', 'live_prompt').order('created_at', desc=True).limit(1).execute()
        if response.data:
            return response.data[0]['prompt']
        else:
            return "No 'live_prompt' found in database."
    except Exception as e:
        return f"DB Error: {e}"

def get_knowledge_base():
    """Fetches the latest knowledge base content from Supabase."""
    try:
        response = supabase.table('prompts').select("*").eq('name', 'knowledge_base').order('created_at', desc=True).limit(1).execute()
        if response.data:
            return response.data[0]['prompt']
        else:
            return "No 'knowledge_base' found in database."
    except Exception as e:
        return f"DB Error (KB): {e}"

if __name__ == "__main__":
    print("-" * 30)
    print("CURRENT LIVE PROMPT:")
    print("-" * 30)
    print(get_current_prompt())
    print("\n" + "-" * 30)
    print("CURRENT KNOWLEDGE BASE:")
    print("-" * 30)
    print(get_knowledge_base())
    print("-" * 30)
