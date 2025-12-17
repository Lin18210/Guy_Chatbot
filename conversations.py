# conversations.py

# Extracted from Customer_support_data.csv (Shopzilla context)

sample_data = [
    {
        # TRAINING GOAL: Clean, spaced-out pricing list
        "client_sequence": "What are your 2024 rates?",
        "chat_history": [],
        "real_consultant_reply": """Here is my 2024 pricing! 📸

        **Engagement / Pre-Wedding**
        • Bangkok (2-3 hrs): 25,000 THB
        • Destination (Thailand): 35,000–50,000 THB

        **Wedding Coverage**
        • Half-Day (6 hrs): 60,000 THB
        • Full-Day (10 hrs): 90,000 THB

        **Popular Add-ons**
        • Second Photographer: +20,000 THB
        • Drone Footage: +10,000 THB

        Let me know your date and I can send a formal quote! ✨"""
    },
    {
        "client_sequence": "I am very disappointed with Shopzilla. The issue was not resolved. The customer care executive was polite enough though he was not able to resolve the issue. But I am appalled at the utter lack of responsibility and accountability of Shopzilla in providing tracking services.",
        "chat_history": [],
        "real_consultant_reply": "We are truly sorry to hear about your frustration. We understand how important it is to track your order accurately. We value your feedback on our accountability and are currently investigating the tracking delay with our logistics partner. Please share your Order ID so we can personally oversee this."
    },
    {
        "client_sequence": "You have played around with this order. Without taking customers concern, how can you plan the resolution/pick-up of the products? Don't you have brain to check with the customers availability? Order placed on 8 July and 19 July damaged product delivered. I'm still awaiting for the resolution and refund.",
        "chat_history": [],
        "real_consultant_reply": "We sincerely apologize for the delay and the damaged product you received. This is certainly not the experience we want for you. We have escalated your pickup request to our logistics team to ensure it happens within 24 hours. Your refund will be processed immediately upon pickup."
    },
    {
        "client_sequence": "Even in the guarantee period you have to contact the supplier to reduce the duration of resolve the issue.",
        "chat_history": [],
        "real_consultant_reply": "We understand your concern regarding the warranty process. While we facilitate the connection with suppliers for authorized service, we are happy to step in and expedite this for you. Let us contact the supplier on your behalf to speed up the resolution."
    },
    {
        "client_sequence": "I selected for English language preference but it's goes into Hindi channel. But customer service executive doesn't understand English properly",
        "chat_history": [],
        "real_consultant_reply": "We apologize for the language mismatch. We have updated your profile preferences to ensure you are connected with our English-speaking support team for all future interactions. How can we assist you today?"
    },
]