import json
import os
from http.server import BaseHTTPRequestHandler
import asyncio
import sys
import requests
import random
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import core functions from main.py (we'll need to extract these)
try:
    from main import (
        get_human_reply,
        BASE_SYLVIA,
        add_message_to_history,
        get_chat_context,
        get_sentiment_analysis,
        get_time_based_mood,
        REPLY_PROBABILITY
    )
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback minimal implementation
    BASE_SYLVIA = "You are Sylvia, a chaotic gamer girl from Amman, Jordan. Keep responses short and energetic."
    REPLY_PROBABILITY = 0.4

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Verify webhook secret for security
            webhook_secret = os.getenv('WEBHOOK_SECRET', '')
            if webhook_secret:
                provided_secret = self.headers.get('X-Webhook-Secret', '')
                if provided_secret != webhook_secret:
                    self.send_response(401)
                    self.end_headers()
                    return

            # Get the content length and read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Parse the JSON data from Telegram webhook
            update = json.loads(post_data.decode('utf-8'))
            
            # Process the update
            response = asyncio.run(self.process_telegram_update(update))
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Error processing webhook: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_GET(self):
        # Health check endpoint
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "Sylvia bot is alive and ready! 🎮",
            "timestamp": datetime.now().isoformat(),
            "mood": get_time_based_mood() if 'get_time_based_mood' in globals() else "energetic"
        }
        self.wfile.write(json.dumps(response).encode())

    async def process_telegram_update(self, update):
        """Process incoming Telegram update and send response"""
        try:
            # Extract message data
            if 'message' not in update:
                return {"status": "no_message"}
                
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            username = message['from'].get('username', message['from'].get('first_name', 'User'))
            text = message.get('text', '')
            
            if not text:
                return {"status": "no_text"}
            
            print(f"💬 Processing message from {username} in chat {chat_id}: {text}")
            
            # Determine if bot should reply
            should_reply = self.should_bot_reply(text, chat_id, message)
            
            if not should_reply:
                return {"status": "no_reply"}
            
            # Generate response using the bot logic
            try:
                reply = await get_human_reply(text, BASE_SYLVIA, str(chat_id), user_id, username)
            except:
                # Fallback response if main bot logic fails
                reply = self.get_fallback_response(text)
            
            if reply:
                # Send response back to Telegram
                success = self.send_telegram_message(chat_id, reply)
                
                return {
                    "status": "replied" if success else "send_failed",
                    "reply": reply,
                    "chat_id": chat_id
                }
            
            return {"status": "no_reply_generated"}
            
        except Exception as e:
            print(f"Error in process_telegram_update: {e}")
            return {"error": str(e)}
    
    def should_bot_reply(self, text, chat_id, message):
        """Determine if the bot should reply to this message"""
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        if not bot_token:
            return False
            
        # Always reply in DMs
        if message['chat']['type'] == 'private':
            return True
        
        # In groups, reply if:
        text_lower = text.lower()
        
        # Check for bot mention
        if f"@{self.get_bot_username()}" in text_lower:
            return True
        
        # Check for gaming/tech keywords that Sylvia would be interested in
        gaming_keywords = [
            "game", "gaming", "play", "raid", "boss", "level", "patch", "update",
            "tech", "code", "dev", "bug", "programming", "rpg", "strategy",
            "sylvia", "syl"
        ]
        
        if any(keyword in text_lower for keyword in gaming_keywords):
            return random.random() < (REPLY_PROBABILITY + 0.2)  # Higher chance for gaming topics
        
        # Random engagement
        return random.random() < REPLY_PROBABILITY
    
    def get_bot_username(self):
        """Get bot username - cache this for efficiency"""
        # You'd typically cache this value
        return "sylvia_bot"  # Replace with actual bot username
    
    def send_telegram_message(self, chat_id, text):
        """Send message to Telegram"""
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            print("No Telegram bot token configured")
            return False
            
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def get_fallback_response(self, text):
        """Fallback responses if main bot logic fails"""
        fallback_responses = [
            "yalla, I'm having a brain glitch rn 🤖",
            "oops, my caffeine levels are too low for this",
            "bestie, I'm lagging harder than my internet",
            "error 404: witty response not found 😅",
            "brb, rebooting my chaos engine",
            "plot twist: I forgot how to English for a sec",
            "my brain.exe stopped working, gimme a sec",
            "technical difficulties, but I'm still here for you bestie!"
        ]
        return random.choice(fallback_responses)