# conversations.py

# Training data for Guy Heart Photography
# STYLE: Simple, Direct. FAST BOOKING (Ask all at once).

sample_data = [
    {
        "client_sequence": "Hi, what services do you offer?",
        "chat_history": [],
        "real_consultant_reply": """Hello. We offer:
1. Wedding Photography (Full & Half Day)
2. Pre-Wedding / Engagement Shoots
3. Cinematic Storytelling

Please let me know which service you are interested in."""
    },
    {
        "client_sequence": "I want to book the Full Day wedding package.",
        "chat_history": [],
        # NEW BEHAVIOR: Ask for everything at once
        "real_consultant_reply": """To proceed with the booking, please provide the following details:
1. Name
2. Phone Number
3. Email Address
4. Desired Date & Time"""
    },
    {
        # Scenario where user gives partial info, AI asks for the REST all at once
        "client_sequence": "I want to book for Dec 12th. My name is John.",
        "chat_history": [],
        "real_consultant_reply": """Thank you, John. To complete the booking for Dec 12th, I still need:
- Phone Number
- Email Address

Please provide these details."""
    },
    {
        "client_sequence": "How much is a pre-wedding shoot?",
        "chat_history": [],
        "real_consultant_reply": """Our Pre-Wedding Session starts from 25,000 THB.
This includes:
- 2 Hours of coverage
- 1 Photographer
- 3 Outfits/Locations
- 100 Retouched Images

Would you like to book this service?"""
    },
    {
        "client_sequence": "I'm really nervous about posing.",
        "chat_history": [],
        "real_consultant_reply": """That is normal. Our photographer will guide you to ensure you look natural. You do not need experience."""
    }
]