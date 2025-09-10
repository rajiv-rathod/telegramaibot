#!/usr/bin/env python3
"""
Dashboard Demo Script
Demonstrates the key features of the Telegram AI Bot Dashboard
"""

import json
import os
from config_manager import get_config, save_config, get_active_personality_content

def demo_dashboard_features():
    print("🎯 Telegram AI Bot Dashboard Demo")
    print("=" * 50)
    
    # Show current configuration
    print("\n📊 Current Bot Configuration:")
    config = get_config()
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Show active personality
    print("\n🎭 Active Personality Content Preview:")
    personality = get_active_personality_content()
    print(f"  Length: {len(personality)} characters")
    print(f"  Preview: {personality[:200]}...")
    
    # Show available personalities
    print("\n🎨 Available Personalities:")
    if os.path.exists('personalities.json'):
        with open('personalities.json', 'r') as f:
            personalities = json.load(f)
            for pid, personality in personalities.items():
                print(f"  - {personality['name']}: {personality['description']}")
    
    # Show PDF files
    print("\n📄 Available PDF Files:")
    pdf_count = 0
    for file in os.listdir('.'):
        if file.endswith('.pdf'):
            size = os.path.getsize(file) / 1024 / 1024  # MB
            print(f"  - {file} ({size:.1f} MB)")
            pdf_count += 1
    
    if os.path.exists('pdf_storage'):
        for file in os.listdir('pdf_storage'):
            if file.endswith('.pdf'):
                path = os.path.join('pdf_storage', file)
                size = os.path.getsize(path) / 1024 / 1024  # MB
                print(f"  - {file} ({size:.1f} MB) [uploaded]")
                pdf_count += 1
    
    print(f"  Total PDFs: {pdf_count}")
    
    # Show bot accounts
    print("\n👥 Bot Accounts:")
    if os.path.exists('accounts.json'):
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)
            for i, account in enumerate(accounts, 1):
                phone = account.get('phone', 'Unknown')
                print(f"  Account {i}: {phone}")
    
    print("\n🚀 Dashboard Features Available:")
    print("  ✅ Real-time bot configuration")
    print("  ✅ Multiple personality presets")
    print("  ✅ Custom personality creation")
    print("  ✅ PDF document management")
    print("  ✅ Multi-bot account support")
    print("  ✅ Debug logging and monitoring")
    print("  ✅ No-code configuration changes")
    
    print("\n🌐 Access Dashboard at: http://localhost:5000")
    print("📋 Full documentation: DASHBOARD_GUIDE.md")
    
    print("\n💡 Quick Start:")
    print("  1. Run: python start_bot.py")
    print("  2. Choose mode (dashboard + bot recommended)")
    print("  3. Open browser to http://localhost:5000")
    print("  4. Configure personalities, PDFs, and settings")
    print("  5. Start bot and enjoy!")

if __name__ == "__main__":
    demo_dashboard_features()