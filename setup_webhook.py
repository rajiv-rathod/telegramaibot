#!/usr/bin/env python3
"""
Setup script for configuring Telegram webhook with Vercel deployment
Run this after deploying to Vercel to set up the webhook
"""

import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()

def setup_telegram_webhook():
    """Configure Telegram webhook to point to Vercel function"""
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    webhook_url = os.getenv('VERCEL_URL')  # Your Vercel deployment URL
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set")
        return False
    
    if not webhook_url:
        print("❌ Please set VERCEL_URL environment variable to your Vercel deployment URL")
        print("   Example: https://your-app.vercel.app")
        return False
    
    # Ensure webhook URL ends with the correct path
    if not webhook_url.endswith('/api/webhook'):
        webhook_url = webhook_url.rstrip('/') + '/api/webhook'
    
    print(f"🔗 Setting up webhook: {webhook_url}")
    
    # Set webhook
    webhook_response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/setWebhook",
        json={"url": webhook_url}
    )
    
    if webhook_response.status_code == 200:
        result = webhook_response.json()
        if result.get('ok'):
            print("✅ Webhook set successfully!")
            
            # Get webhook info to verify
            info_response = requests.get(
                f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
            )
            
            if info_response.status_code == 200:
                info = info_response.json()
                if info.get('ok'):
                    webhook_info = info['result']
                    print(f"📋 Webhook Info:")
                    print(f"   URL: {webhook_info.get('url', 'Not set')}")
                    print(f"   Pending updates: {webhook_info.get('pending_update_count', 0)}")
                    print(f"   Last error: {webhook_info.get('last_error_message', 'None')}")
            
            return True
        else:
            print(f"❌ Failed to set webhook: {result.get('description', 'Unknown error')}")
            return False
    else:
        print(f"❌ HTTP error {webhook_response.status_code}")
        return False

def remove_webhook():
    """Remove webhook (useful for development)"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set")
        return False
    
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print("✅ Webhook removed successfully!")
            return True
        else:
            print(f"❌ Failed to remove webhook: {result.get('description', 'Unknown error')}")
            return False
    else:
        print(f"❌ HTTP error {response.status_code}")
        return False

if __name__ == "__main__":
    print("🤖 Telegram Bot Webhook Setup for Vercel")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        remove_webhook()
    else:
        print("Setting up webhook...")
        setup_telegram_webhook()
        print("\n💡 To remove webhook later, run: python setup_webhook.py remove")
        print("💡 Make sure to set these environment variables in Vercel:")
        print("   - TELEGRAM_BOT_TOKEN")
        print("   - OPENAI_API_KEY") 
        print("   - OPENAI_ORG_ID")
        print("   - WEBHOOK_SECRET (optional, for security)")