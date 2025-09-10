#!/usr/bin/env python3
"""
Startup script for Telegram AI Bot with Dashboard
Runs both the dashboard web interface and the bot
"""

import os
import sys
import threading
import time
import subprocess
import signal
from config_manager import initialize_config_files, get_config

def run_dashboard():
    """Run the dashboard web interface"""
    print("🌐 Starting Dashboard Web Interface...")
    os.system("python dashboard.py")

def run_bot():
    """Run the main telegram bot"""
    print("🤖 Starting Telegram Bot...")
    # Wait a bit for dashboard to start
    time.sleep(2)
    os.system("python main.py")

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask', 'flask_cors', 'telethon', 'httpx', 'pdfplumber', 
        'textblob', 'requests', 'python-dotenv', 'nltk'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    return True

def check_config_files():
    """Check if required configuration files exist"""
    required_files = ['.env', 'accounts.json']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ Missing configuration files: {', '.join(missing_files)}")
        print("Creating example files...")
        
        if '.env' in missing_files:
            print("Please copy .env.example to .env and configure your API keys")
        
        if 'accounts.json' in missing_files:
            if os.path.exists('accounts.json.example'):
                print("Please copy accounts.json.example to accounts.json and configure your Telegram accounts")
            else:
                # Create a basic accounts.json template
                import json
                template = [
                    {
                        "api_id": "YOUR_API_ID",
                        "api_hash": "YOUR_API_HASH", 
                        "phone": "YOUR_PHONE_NUMBER"
                    }
                ]
                with open('accounts.json', 'w') as f:
                    json.dump(template, f, indent=2)
                print("Created accounts.json template - please configure your Telegram accounts")
        
        return False
    
    return True

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\n🛑 Shutting down...")
    sys.exit(0)

def main():
    """Main startup function"""
    print("🚀 Telegram AI Bot with Dashboard Startup")
    print("=" * 50)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Initialize configuration files
    print("📝 Initializing configuration files...")
    initialize_config_files()
    
    # Check required config files
    if not check_config_files():
        print("\n⚠️ Please configure the required files and run again.")
        return 1
    
    print("✅ All dependencies and configurations OK!")
    print("\n🎯 Starting services...")
    print("📊 Dashboard: http://localhost:5000")
    print("🤖 Bot: Will start automatically")
    print("\nPress Ctrl+C to stop all services\n")
    
    # Get user choice
    mode = input("Choose mode:\n1. Dashboard only\n2. Bot only\n3. Both (default)\nEnter choice (1/2/3): ").strip()
    
    if mode == '1':
        # Dashboard only
        run_dashboard()
    elif mode == '2':
        # Bot only
        run_bot()
    else:
        # Both (default)
        try:
            # Start dashboard in a separate thread
            dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
            dashboard_thread.start()
            
            # Start bot in main thread
            run_bot()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            return 0
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)