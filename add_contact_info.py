import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

# Supabase Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

CONTACT_INFO = """
### CONTACT DETAILS ###
Business Name: Guy Heart Photography
Email: guyheartphotography11@gmail.com
Phone: +66 933490230
Line: https://lin.ee/m6EBMRf (ID: @guyheart)

### APPOINTMENT BOOKING INSTRUCTIONS ###
To book an appointment, you must collect the following 4 pieces of information from the user:
1. Name
2. Phone Number
3. Email
4. Desired Date & Time

Do NOT confirm the booking until you have ALL 4 details. Ask for missing details politely.

Once you have all 4 details, you MUST output a special JSON block to trigger the system booking.
Output ONLY the JSON block at the end of your confirmation message (or just the JSON).

FORMAT:
```json
{
  "action": "book_appointment",
  "data": {
    "name": "Customer Name",
    "phone": "Customer Phone",
    "email": "Customer Email",
    "appointment_time": "Desired Date/Time"
  }
}
```
"""

def add_contact_to_knowledge_base():
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

        # Check if contact info is already there to avoid duplicates
        if "guyheartphotography11@gmail.com" in current_kb:
            print("⚠️ Contact info already exists in Knowledge Base.")
            return

        # Append new info
        updated_kb = current_kb + "\n\n" + CONTACT_INFO
        
        # Save as new entry (Versioning)
        data = {
            "name": "knowledge_base",
            "prompt": updated_kb,
            "metadata": {"reason": "Added contact details"}
        }
        
        supabase.table('prompts').insert(data).execute()
        print("✅ Contact details added to Knowledge Base successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_contact_to_knowledge_base()
