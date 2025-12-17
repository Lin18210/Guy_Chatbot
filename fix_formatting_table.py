import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

# Supabase Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

def apply_table_formatting_rule():
    print("🎨 Fetching current prompt...")
    try:
        response = supabase.table('prompts').select("*").eq('name', 'live_prompt').order('created_at', desc=True).limit(1).execute()
        current_prompt = "You are a helpful assistant."
        if response.data:
            current_prompt = response.data[0]['prompt']
        
        # This is the appointment booking instruction so far.
        
        table_instruction = """
        
        ### FORMATTING RULES ###
        - When presenting packages, pricing, or comparative lists, YOU MUST USE A MARKDOWN TABLE.
        - The table should (usually) have columns like: | Package | Price | Details |
        - Do NOT use simple bullet lists or paragraphs for pricing.
        - Make sure the table is properly formatted in Markdown.
        """
        
        # If we previously added the bullet point rule, we should replace it or append this stronger rule.
        # Ideally, we reconstruct the prompt.
        
        # Let's clean up old formatting rules
        base_prompt = current_prompt.split("### FORMATTING RULES ###")[0].strip()
        
        new_prompt = base_prompt + table_instruction
        
        data = {
            "name": "live_prompt",
            "prompt": new_prompt,
            "metadata": {"reason": "User requested table formatting for pricing."}
        }
        
        supabase.table('prompts').insert(data).execute()
        print("✅ Table formatting rules applied successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    apply_table_formatting_rule()
