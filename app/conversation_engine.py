# app/conversation_engine.py

import datetime

GREETINGS = {
    "hi": "Hello! 👋 How can I assist you today?",
    "hello": "Hello! How are you doing?",
    "hey": "Hey there! What can I help you with?",
    "yo": "Yo! Need help monitoring your servers? 😄",
    "sup": "Hey! What's up? Need any system metrics?",
    "greetings": "Greetings! What infrastructure metric would you like to check?"
}

GENERAL_RESPONSES = {
    "how are you": "I'm doing great! Ready to monitor your infrastructure 🚀",
    "how are you doing": "I'm running perfectly! Ready to assist with server monitoring.",
    "how's it going": "Everything is running smoothly on my side! How can I help?",
    "are you there": "Yes! I'm here and ready to help with your infrastructure metrics.",
    "what can you do": "I can monitor CPU, Memory, and Disk across DEV, QA, UAT, PROD, MYSAA and KK servers.",
    "who are you": "I'm your infrastructure monitoring assistant 🤖",
    "what is this": "This is an AI-powered infrastructure monitoring assistant built with FastAPI.",
    "help": "You can ask things like: 'dev cpu', 'memory qa', 'disk prod'.",

    "thanks": "You're welcome! Happy to help.",
    "thank you": "You're welcome! Let me know if you need any system metrics.",
    "cool": "Glad you think so! Need any server metrics?",
    "nice": "Happy to help! Let me know if you'd like to check CPU, Memory, or Disk usage.",
    "great": "Awesome! Let me know if you'd like to monitor any environment.",
    "ok": "Alright 👍 What would you like to check?",
    "okay": "Sure! Just tell me the server environment and metric.",
    "bye": "Goodbye! Reach out anytime you need system metrics 👋",
    "see you": "See you later! I'll keep watching the servers 😄",
    "goodbye": "Goodbye! Your infrastructure assistant signing off 👋"
}


def process_conversation(text: str):

    text = text.lower().strip()
    words = text.split()

    # Greeting detection
    for key in GREETINGS:
        if key in words:
            return GREETINGS[key]

    # General conversation detection
    for key in GENERAL_RESPONSES:
        if key in text:
            return GENERAL_RESPONSES[key]

    # Time-based greeting
    if "good" in words:

        hour = datetime.datetime.now().hour

        if hour < 12:
            return "Good morning! ☀️"
        elif hour < 17:
            return "Good afternoon! 🌤️"
        elif hour < 21:
            return "Good evening! 🌙"
        else:
            return "Good night! 😴"

    return None