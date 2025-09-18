# 🚀 Vercel Deployment Guide

This guide walks you through deploying Sylvia's Telegram AI bot to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Telegram Bot Token**: Get one from [@BotFather](https://t.me/botfather)
3. **OpenAI API Access**: Get API key from [OpenAI](https://platform.openai.com)

## 🛠️ Step-by-Step Deployment

### Step 1: Prepare Your Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command and follow instructions
3. Save your bot token (format: `123456789:ABCdef...`)
4. Note your bot's username

### Step 2: Deploy to Vercel

#### Option A: Using Vercel Dashboard
1. Fork this repository to your GitHub account
2. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Import your forked repository
5. Vercel will auto-detect the configuration from `vercel.json`

#### Option B: Using Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# - Link to existing project? No
# - What's your project's name? (enter name)
# - In which directory is your code located? ./
```

### Step 3: Configure Environment Variables

In your Vercel dashboard, go to **Settings > Environment Variables** and add:

| Variable | Value | Description |
|----------|-------|-------------|
| `OPENAI_API_KEY` | `sk-...` | Your OpenAI API key |
| `OPENAI_ORG_ID` | `org-...` | Your OpenAI organization ID |
| `TELEGRAM_BOT_TOKEN` | `123456:ABC...` | Bot token from BotFather |
| `WEBHOOK_SECRET` | `your_secret` | (Optional) Security secret |

**Important**: Set these for all environments (Production, Preview, Development).

### Step 4: Set Up Webhook

After deployment, you'll get a URL like `https://your-app.vercel.app`. Now configure the Telegram webhook:

```bash
# Clone your deployed repository locally
git clone https://github.com/yourusername/your-repo-name
cd your-repo-name

# Install dependencies
pip install -r requirements.txt

# Set environment variables for the setup script
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export VERCEL_URL="https://your-app.vercel.app"

# Run webhook setup
python setup_webhook.py
```

### Step 5: Test Your Bot

1. **Health Check**: Visit `https://your-app.vercel.app/api/webhook` 
   - Should show: `{"status": "Sylvia bot is alive and ready! 🎮"}`

2. **Test Bot**: Send a message to your bot on Telegram
   - Start with: `/start` or `hey Sylvia`
   - Try gaming keywords: `what games do you play?`

## 🔧 Development Workflow

### Local Testing
```bash
# Run local development server
python dev_server.py

# In another terminal, use ngrok to expose it
ngrok http 8000

# Update webhook to point to ngrok URL
export VERCEL_URL="https://abc123.ngrok.io"
python setup_webhook.py
```

### Updating Deployment
```bash
# Make changes to your code
git add .
git commit -m "Update bot features"
git push

# Vercel will automatically redeploy
# No need to reconfigure webhook
```

## 🐛 Troubleshooting

### Bot Not Responding
1. Check Vercel function logs in dashboard
2. Verify environment variables are set
3. Test webhook URL manually:
   ```bash
   curl https://your-app.vercel.app/api/webhook
   ```

### Webhook Issues
```bash
# Check current webhook status
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo"

# Remove webhook if needed
python setup_webhook.py remove

# Set webhook again
python setup_webhook.py
```

### Environment Variables
- Make sure all required variables are set in Vercel dashboard
- Check they're set for all environments (Production, Preview, Development)
- Variables take effect after next deployment

## 📊 Monitoring

- **Vercel Dashboard**: Monitor function invocations, errors, and performance
- **Bot Logs**: Check Vercel function logs for debugging info
- **Telegram**: Bot will respond with fallback messages if errors occur

## 🔒 Security

- **Webhook Secret**: Add `WEBHOOK_SECRET` environment variable for additional security
- **Environment Variables**: Never commit API keys to repository
- **HTTPS Only**: Vercel provides HTTPS by default (required for Telegram webhooks)

## 🚀 Performance

- **Cold Starts**: First request may be slower (Vercel warming up)
- **Concurrent Requests**: Vercel automatically scales serverless functions
- **Response Time**: Typical response under 2 seconds including OpenAI API call

## 📈 Scaling

- **Automatic**: Vercel handles all scaling automatically
- **Limits**: Check your Vercel plan limits for function invocations
- **Monitoring**: Use Vercel analytics to track usage

---

Need help? Check the [main README](README.md) or open an issue! 🤖✨