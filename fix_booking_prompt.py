import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

# Supabase Setup
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

def apply_booking_prompt_logic():
    print("🎨 Fetching current prompt...")
    try:
        response = supabase.table('prompts').select("*").eq('name', 'live_prompt').order('created_at', desc=True).limit(1).execute()
        current_prompt = "You are a helpful assistant."
        if response.data:
            current_prompt = response.data[0]['prompt']
        
        # Remove old formatting rules to avoid duplication (careful not to remove other important stuff)
        if "### BOOKING INSTRUCTIONS ###" in current_prompt:
             base_prompt = current_prompt.split("### BOOKING INSTRUCTIONS ###")[0].strip()
        else:
             base_prompt = current_prompt.strip()
            
        booking_instruction = """
        
        ### BOOKING INSTRUCTIONS ###
        1. **OFFER APPOINTMENTS**: If a user seems interested in booking or discussing services, ASK if they would like to book an appointment (online or in-person).
        2. **DATA COLLECTION**: If they say YES, you MUST ask for the following details (one by one or together):
           - Name
           - Phone Number
           - Email Address
           - Preferred Date & Time
        3. **CONFIRMATION**: Once you have ALL 4 pieces of information, you MUST output a special JSON object to trigger the booking system in the backend.
        
        **TRIGGER FORMAT**:
        Do not say anything else in the final confirmation turn. Just output this JSON:
        ```json
        {
            "action": "book_appointment",
            "data": {
                "name": "User Name",
                "phone": "User Phone",
                "email": "User Email",
                "appointment_time": "Requested Date/Time"
            }
        }
        ```
        The system will intercept this, save the appointment, send the emails, and then tell the user "Booking Confirmed".
        """
        
        new_prompt = base_prompt + booking_instruction
        
        # Save
        data = {
            "name": "live_prompt",
            "prompt": new_prompt,
            "metadata": {"reason": "Enabled Appointment Booking Logic"}
        }
        
        supabase.table('prompts').insert(data).execute()
        print("✅ Booking Prompt Logic applied successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    apply_booking_prompt_logic()
