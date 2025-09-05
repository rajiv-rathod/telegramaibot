#!/bin/bash

# Railway startup script
echo "🚀 Starting Telegram AI Bot on Railway..."

# Create necessary directories
mkdir -p chat_histories
mkdir -p sessions

# Download NLTK data if needed
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True)"

# Start the bot
echo "🤖 Launching bot..."
python main.py
