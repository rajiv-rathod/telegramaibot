# DigitalOcean VPS Deployment Guide for Telegram Userbot

## 🚀 DigitalOcean Setup

### 1. Create DigitalOcean Droplet
```bash
# Recommended specs:
- OS: Ubuntu 22.04 LTS
- Plan: Basic ($6/month - 1GB RAM, 1 vCPU)
- Region: Choose closest to you
- SSH Key: Add your SSH key
```

### 2. Connect to Your Droplet
```bash
ssh root@your_droplet_ip
```

### 3. Initial Server Setup
```bash
# Update system
apt update && apt upgrade -y

# Install Python 3.11+
apt install python3 python3-pip python3-venv git curl -y

# Create app user
adduser telegram_bot
usermod -aG sudo telegram_bot
su - telegram_bot
```

### 4. Deploy Your Bot
```bash
# Clone your repository
git clone https://github.com/rajiv-rathod/telegramaibot.git
cd telegramaibot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your_openai_api_key"
export OPENAI_ORG_ID="your_openai_org_id"
```

### 5. Create Systemd Service (Auto-restart)
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Add this content:
```ini
[Unit]
Description=Telegram Userbot
After=network.target

[Service]
Type=simple
User=telegram_bot
WorkingDirectory=/home/telegram_bot/telegramaibot
Environment=PATH=/home/telegram_bot/telegramaibot/venv/bin
Environment=OPENAI_API_KEY=your_openai_api_key
Environment=OPENAI_ORG_ID=your_openai_org_id
ExecStart=/home/telegram_bot/telegramaibot/venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 6. Start and Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f
```

### 7. Firewall Setup (Optional)
```bash
# Enable UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### 8. Update Bot Code
```bash
# To update your bot later:
cd /home/telegram_bot/telegramaibot
git pull origin main
sudo systemctl restart telegram-bot
```

## 🔧 Management Commands

```bash
# Stop bot
sudo systemctl stop telegram-bot

# Start bot
sudo systemctl start telegram-bot

# Restart bot
sudo systemctl restart telegram-bot

# View logs
sudo journalctl -u telegram-bot -f

# Check status
sudo systemctl status telegram-bot
```

## 🛠 Troubleshooting

### Check if bot is running:
```bash
ps aux | grep python
sudo systemctl status telegram-bot
```

### View recent logs:
```bash
sudo journalctl -u telegram-bot --since "1 hour ago"
```

### Debug mode (run manually):
```bash
su - telegram_bot
cd telegramaibot
source venv/bin/activate
export OPENAI_API_KEY="your_key"
export OPENAI_ORG_ID="your_org"
python main.py
```

## 💰 Cost Estimate
- **DigitalOcean Droplet**: $6/month (Basic plan)
- **OpenAI API**: Pay per usage
- **Total**: ~$6-10/month depending on usage

## 🔐 Security Notes
- Change default SSH port
- Use SSH keys instead of passwords
- Keep system updated: `sudo apt update && sudo apt upgrade`
- Monitor resource usage: `htop`

Your userbot will run 24/7 on DigitalOcean with automatic restarts!