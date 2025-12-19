
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    with open("current_prompt_dump_utf8.txt", "w", encoding="utf-8") as f:
        f.write("Error: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not found in environment.")
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
    output = []
    output.append("-" * 30)
    output.append("CURRENT LIVE PROMPT:")
    output.append("-" * 30)
    output.append(get_current_prompt())
    output.append("\n" + "-" * 30)
    output.append("CURRENT KNOWLEDGE BASE:")
    output.append("-" * 30)
    output.append(get_knowledge_base())
    output.append("-" * 30)
    
    with open("current_prompt_dump_utf8.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))
