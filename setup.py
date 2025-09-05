#!/usr/bin/env python3
"""
Setup script for the Enhanced Telegram AI Bot
Downloads necessary NLTK data for sentiment analysis
"""

import nltk
import os

def setup_nltk():
    """Download required NLTK data"""
    print("🔄 Setting up NLTK data for sentiment analysis...")
    
    try:
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True) 
        nltk.download('vader_lexicon', quiet=True)
        print("✅ NLTK data setup complete!")
        return True
    except Exception as e:
        print(f"❌ Error setting up NLTK: {e}")
        return False

def verify_dependencies():
    """Verify all dependencies are available"""
    print("🔍 Verifying dependencies...")
    
    try:
        import telethon
        import httpx
        import textblob
        import requests
        print("✅ All dependencies verified!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = ['sessions', 'chat_histories']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created!")

def main():
    print("🚀 Enhanced Telegram AI Bot Setup")
    print("=" * 40)
    
    success = True
    success &= verify_dependencies()
    success &= setup_nltk()
    create_directories()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("📋 Next steps:")
        print("1. Copy .env.example to .env and add your API keys")
        print("2. Copy accounts.json.example to accounts.json and add your Telegram credentials")
        print("3. Run: python main.py")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()