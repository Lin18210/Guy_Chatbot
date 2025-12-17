import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

# Supabase Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

def apply_strict_formatting_rule():
    print("🎨 Fetching current prompt...")
    try:
        response = supabase.table('prompts').select("*").eq('name', 'live_prompt').order('created_at', desc=True).limit(1).execute()
        current_prompt = "You are a helpful assistant."
        if response.data:
            current_prompt = response.data[0]['prompt']
        
        # I strip out old formatting rules to start fresh
        if "### FORMATTING RULES ###" in current_prompt:
            base_prompt = current_prompt.split("### FORMATTING RULES ###")[0].strip()
        else:
            base_prompt = current_prompt.strip()
            
        strict_instruction = """
        
        ### FORMATTING RULES ###
        1. **PRICING & PACKAGES MUST BE TABLES**: Whenever you list packages, options, or pricing, you MUST use a Markdown Table.
        2. **STRICT MARKDOWN SYNTAX**: 
           - You MUST put a newline `\\n` before to the table.
           - You MUST put a newline `\\n` after every row.
           - You MUST use `|` to separate columns.
           - You MUST use `|---|` for the separator line.
        
        Example JSON Output structure (internal thought process):
        Start with: `Here are the packages:`
        Then newline.
        Then:
        | Package | Price | Details |
        | :--- | :--- | :--- |
        | Name | 500 | Info |
        | Name 2 | 1000 | Info 2 |
        
        Do NOT write it as a paragraph. Do NOT use simple lists.
        """
        
        new_prompt = base_prompt + strict_instruction
        
        data = {
            "name": "live_prompt",
            "prompt": new_prompt,
            "metadata": {"reason": "User requested STRICT table formatting."}
        }
        
        supabase.table('prompts').insert(data).execute()
        print("✅ Strict Table formatting rules applied successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    apply_strict_formatting_rule()
