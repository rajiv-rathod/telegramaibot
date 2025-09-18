#!/bin/bash

# DigitalOcean VPS Setup Script for Telegram Userbot
# Run this script on your fresh Ubuntu 22.04 DigitalOcean droplet

set -e

echo "🚀 Setting up Telegram Userbot on DigitalOcean..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Update system
echo -e "${YELLOW}📦 Updating system packages...${NC}"
apt update && apt upgrade -y

# Install required packages
echo -e "${YELLOW}🔧 Installing Python and dependencies...${NC}"
apt install -y python3 python3-pip python3-venv git curl htop nano ufw

# Create bot user
echo -e "${YELLOW}👤 Creating telegram_bot user...${NC}"
if ! id "telegram_bot" &>/dev/null; then
    adduser --disabled-password --gecos "" telegram_bot
    usermod -aG sudo telegram_bot
    echo -e "${GREEN}✅ User telegram_bot created${NC}"
else
    echo -e "${GREEN}✅ User telegram_bot already exists${NC}"
fi

# Switch to bot user for app setup
echo -e "${YELLOW}📁 Setting up application...${NC}"
sudo -u telegram_bot bash << 'EOF'
cd /home/telegram_bot

# Clone repository if not exists
if [ ! -d "telegramaibot" ]; then
    echo "📥 Cloning repository..."
    git clone https://github.com/rajiv-rathod/telegramaibot.git
else
    echo "📁 Repository already exists, pulling latest changes..."
    cd telegramaibot && git pull origin main && cd ..
fi

cd telegramaibot

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Application setup complete!"
EOF

# Create systemd service file
echo -e "${YELLOW}⚙️ Creating systemd service...${NC}"
cat > /etc/systemd/system/telegram-bot.service << 'EOF'
[Unit]
Description=Telegram Userbot - Sylvia
After=network.target

[Service]
Type=simple
User=telegram_bot
WorkingDirectory=/home/telegram_bot/telegramaibot
Environment=PATH=/home/telegram_bot/telegramaibot/venv/bin
Environment=PYTHONPATH=/home/telegram_bot/telegramaibot
ExecStart=/home/telegram_bot/telegramaibot/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Set up firewall
echo -e "${YELLOW}🔥 Configuring firewall...${NC}"
ufw --force enable
ufw allow ssh
ufw allow 80
ufw allow 443

# Enable but don't start service yet (need environment variables)
systemctl daemon-reload
systemctl enable telegram-bot

echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Set your environment variables:"
echo "   export OPENAI_API_KEY='your_openai_api_key'"
echo "   export OPENAI_ORG_ID='your_openai_org_id'"
echo ""
echo "2. Or create /home/telegram_bot/telegramaibot/.env file:"
echo "   sudo -u telegram_bot nano /home/telegram_bot/telegramaibot/.env"
echo "   Add:"
echo "   OPENAI_API_KEY=your_openai_api_key"
echo "   OPENAI_ORG_ID=your_openai_org_id"
echo ""
echo "3. Start the bot:"
echo "   systemctl start telegram-bot"
echo ""
echo "4. Check status:"
echo "   systemctl status telegram-bot"
echo ""
echo "5. View logs:"
echo "   journalctl -u telegram-bot -f"
echo ""
echo -e "${GREEN}🤖 Your Telegram userbot is ready to run!${NC}"