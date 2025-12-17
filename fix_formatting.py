import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

# Supabase Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

def apply_formatting_rule():
    print("🎨 Fetching current prompt...")
    try:
        response = supabase.table('prompts').select("*").eq('name', 'live_prompt').order('created_at', desc=True).limit(1).execute()
        current_prompt = "You are a helpful assistant."
        if response.data:
            current_prompt = response.data[0]['prompt']
        
        print(f"Current Prompt: {current_prompt[:50]}...")
        
        formatting_instruction = """
        
        ### FORMATTING RULES ###
        - When presenting lists, pricing, packages, or features, YOU MUST use bullet points (hyphens '-').
        - Put each item on a NEW LINE.
        - Do NOT write lists in paragraph form.
        - Example:
          - Feature 1
          - Feature 2
        """
        
        if "### FORMATTING RULES ###" not in current_prompt:
            new_prompt = current_prompt + formatting_instruction
            
            data = {
                "name": "live_prompt",
                "prompt": new_prompt,
                "metadata": {"reason": "User requested bullet point formatting for clarity."}
            }
            
            supabase.table('prompts').insert(data).execute()
            print("✅ Formatting rules applied successfully!")
        else:
            print("⚠️ Formatting rules already exist.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    apply_formatting_rule()
