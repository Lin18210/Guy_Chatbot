import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from supabase import create_client, Client
from openai import OpenAI
from flask_mail import Mail, Message
from dotenv import load_dotenv

# 1. Configuration
load_dotenv(override=True)
app = Flask(__name__)

# MAIL Config
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)

# Supabase Setup (Using Service Role Key to bypass RLS)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

# DeepSeek / OpenRouter Setup
client_deepseek = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("Deepseek_API_KEY"),
)
MODEL_DEEPSEEK = "tngtech/deepseek-r1t2-chimera:free"

print(f"--- CONFIG ---")
print(f"DeepSeek Key Loaded: {bool(os.environ.get('Deepseek_API_KEY'))}")
print(f"Model: {MODEL_DEEPSEEK}")
print(f"--------------")


# 2. Helper Functions

def get_current_prompt():
    """Fetches the latest active prompt from Supabase."""
    try:
        response = supabase.table('prompts').select("*").eq('name', 'live_prompt').order('created_at', desc=True).limit(1).execute()
        if response.data:
            return response.data[0]['prompt']
    except Exception as e:
        print(f"DB Error: {e}")
    return "You are a helpful assistant." # Fallback

def get_knowledge_base():
    """Fetches the latest knowledge base content from Supabase."""
    try:
        response = supabase.table('prompts').select("*").eq('name', 'knowledge_base').order('created_at', desc=True).limit(1).execute()
        if response.data:
            return response.data[0]['prompt']
    except Exception as e:
        print(f"DB Error (KB): {e}")
    return ""

def update_system_prompt(new_prompt_text, reasoning):
    """Saves the new improved prompt to Supabase."""
    data = {
        "name": "live_prompt",
        "prompt": new_prompt_text,
        "metadata": {"reason": reasoning}
    }
    supabase.table('prompts').insert(data).execute()

def send_booking_email(booking_data):
    """Sends confirmation email to client and notification to business."""
    try:
        # 1. Email to Business
        msg_admin = Message('New Appointment Request', 
                      sender=app.config['MAIL_USERNAME'], 
                      recipients=['linnt3100@gmail.com']) 
        msg_admin.body = f"""
        New Appointment Request:
        Name: {booking_data.get('name')}
        Phone: {booking_data.get('phone')}
        Email: {booking_data.get('email')}
        Requested Time: {booking_data.get('appointment_time')}
        """
        mail.send(msg_admin)
        
        # 2. Email to Client
        if booking_data.get('email'):
            msg_client = Message('Appointment Confirmation - Guy Heart Photography',
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[booking_data.get('email')])
            msg_client.body = f"""
            Dear {booking_data.get('name')},
            
            Thank you for booking with Guy Heart Photography.
            We have received your request for an appointment on {booking_data.get('appointment_time')}.
            
            We will review your request and contact you shortly to confirm the details.
            
            Best regards,
            Guy Heart Photography Team
            """
            mail.send(msg_client)
            
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# --- DEEPSEEK LOGIC ---

def generate_with_deepseek(system_instruction, history, user_message):
    """
    Uses DeepSeek via OpenRouter to generate content.
    """
    try:
        # Convert history to OpenAI format
        messages = [{"role": "system", "content": system_instruction}]
        
        for h in history:
            # Map roles: consultant -> assistant, client -> user
            role = "assistant" if h.get("role") in ["consultant", "model"] else "user"
            messages.append({"role": role, "content": h.get("message", "")})
            
        messages.append({"role": "user", "content": user_message})

        completion = client_deepseek.chat.completions.create(
            model=MODEL_DEEPSEEK,
            messages=messages,
        )
        return completion.choices[0].message.content, "DeepSeek"

    except Exception as e:
        logging.error(f"DeepSeek failed: {e}")
        raise e

# 3. Routes

@app.route('/')
def client_chat():
    """Customer facing chat interface."""
    return render_template('client_chat.html')

@app.route('/admin')
def admin_dashboard():
    """Internal dashboard for monitoring and improvement."""
    return render_template('dashboard.html')

@app.route('/api/logs')
def get_logs_api():
    """Fetches data for the dashboard."""
    logs = supabase.table('ai_logs').select("*").order('created_at', desc=True).limit(20).execute()
    prompt = get_current_prompt()
    return jsonify({"logs": logs.data, "current_prompt": prompt})

@app.route('/generate-reply', methods=['POST'])
def generate_reply():
    """Generates a reply using DeepSeek."""
    data = request.json
    client_seq = data.get('clientSequence')
    history = data.get('chatHistory', [])
    
    current_prompt = get_current_prompt()
    knowledge_base = get_knowledge_base()
    full_system_instruction = f"{current_prompt}\n\n### KNOWLEDGE BASE ###\n{knowledge_base}"
    
    try:
        ai_reply, provider = generate_with_deepseek(full_system_instruction, history, client_seq)
        
        # Check for booking action (simple JSON detection)
        if "action" in ai_reply and "book_appointment" in ai_reply:
            try:
                # Attempt to extract JSON if wrapped in markdown
                clean_json = ai_reply
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()
                
                action_data = json.loads(clean_json)
                if action_data.get('action') == 'book_appointment':
                     details = action_data.get('data')
                     supabase.table('appointments').insert(details).execute()
                     send_booking_email(details)
                     return jsonify({"aiReply": f"Confirmed! Appointment booked for {details.get('appointment_time')}."})
            except Exception as e:
                print(f"Booking Error: {e}")

        return jsonify({"aiReply": ai_reply, "provider": provider})
        
    except Exception as e:
        return jsonify({"error": f"DeepSeek generation failed: {str(e)}"}), 500

@app.route('/improve-ai', methods=['POST'])
def improve_ai():
    """The Core Learning Loop."""
    data = request.json
    client_seq = data.get('clientSequence')
    history = data.get('chatHistory', [])
    ground_truth = data.get('consultantReply')
    
    current_prompt = get_current_prompt()
    
    # A. PREDICT
    try:
        prediction, _ = generate_with_deepseek(current_prompt, history, client_seq)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
    # B. OPTIMIZE (Editor)
    editor_prompt = f"""
    1. CURRENT SYSTEM PROMPT: "{current_prompt}"
    2. CLIENT INPUT: "{client_seq}"
    3. AI PREDICTED REPLY: "{prediction}"
    4. IDEAL HUMAN REPLY: "{ground_truth}"

    TASK: 
    Compare the AI prediction to the Ideal Human Reply.
    Rewrite the SYSTEM PROMPT (the persona/behavior part only) to make the AI match the human's tone, length, and logic.
    Do NOT include the Knowledge Base data in the new prompt.
    
    Return JSON: {{ "reasoning": "...", "new_prompt": "..." }}
    """
    
    try:
        result_text, provider = generate_with_deepseek("You are an AI Optimization Engine. Return only valid JSON.", [], editor_prompt)
        
        # Cleanup potential markdown around JSON
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()

        result = json.loads(result_text)
        
        new_prompt = result.get('new_prompt')
        reasoning = result.get('reasoning')
        
        supabase.table('ai_logs').insert({
            "client_sequence": json.dumps(client_seq),
            "predicted_reply": prediction,
            "consultant_reply": ground_truth,
            "editor_result": result,
            "provider": provider 
        }).execute()
        
        update_system_prompt(new_prompt, reasoning)
        
        return jsonify({"status": "success", "new_prompt": new_prompt, "provider": provider})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000, debug=True)