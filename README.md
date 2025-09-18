# Enhanced Human-like Telegram AI Bot 🤖✨

An improved Telegram AI bot featuring Sylvia, a chaotic gamer girl persona from Amman, Jordan. This bot has been enhanced to be as human-like as possible and is now deployable on **Vercel** as a serverless webhook.

## 🚀 New Human-like Features

### 🧠 Advanced Behavior
- **Sentiment Analysis**: Responds differently based on user's emotional tone
- **Time-based Personality**: More energetic in evenings, sleepy at night
- **Contextual Emoji**: Adds appropriate emojis based on sentiment and time
- **Typing Simulation**: Realistic delays that simulate human typing speed
- **Enhanced Memory**: Better context awareness and conversation continuity

### 🆓 Open-Source Features Added
- **Sentiment Analysis** using TextBlob
- **Random Gaming Jokes** for entertainment
- **Weather-aware Responses** (placeholder for weather API integration)
- **Time-based Greetings** and mood adjustments
- **Enhanced Error Handling** with personality-appropriate fallbacks

### 🔧 Technical Improvements
- **Vercel Serverless Deployment**: Webhook-based architecture for Vercel
- **Security Enhancement**: API keys moved to environment variables
- **Better Response Quality**: Adjusted temperature based on context
- **Improved Context Handling**: More conversation history and better prompts
- **Human-like Response Timing**: Variable delays and typing indicators

## 📁 File Structure
```
├── api/
│   └── webhook.py          # Vercel serverless function for Telegram webhook
├── main.py                 # Original bot logic (reusable components)
├── personality.txt         # Enhanced Sylvia persona with new behaviors
├── requirements.txt        # Original dependencies
├── requirements_vercel.txt # Vercel-specific lighter dependencies
├── .env.vercel.example     # Environment variables template for Vercel
├── setup_webhook.py        # Script to configure Telegram webhook
├── vercel.json             # Vercel deployment configuration
└── chat_histories/         # Conversation memory storage
```

## 🛠️ Vercel Deployment Setup

### 1. **Create a Telegram Bot**
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command and follow instructions
3. Save the bot token for environment variables

### 2. **Deploy to Vercel**
1. Fork/clone this repository
2. Import to Vercel or use Vercel CLI:
   ```bash
   npm i -g vercel
   vercel
   ```

### 3. **Configure Environment Variables**
In your Vercel dashboard, go to Settings > Environment Variables and add:
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_ORG_ID`: Your OpenAI organization ID
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from BotFather
- `WEBHOOK_SECRET`: (Optional) Secret for webhook security

### 4. **Set Up Webhook**
After deployment, run the webhook setup script:
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables locally for the setup script
export TELEGRAM_BOT_TOKEN="your_bot_token"
export VERCEL_URL="https://your-app.vercel.app"

# Run webhook setup
python setup_webhook.py
```

## 🎯 Key Architecture Changes for Vercel

### Webhook-Based vs Long-Running Process
- **Original**: Long-running userbot with persistent connections
- **Vercel**: Serverless function responding to Telegram webhooks
- **Benefits**: Auto-scaling, zero maintenance, cost-effective

### Response Flow
```
Telegram → Webhook → Vercel Function → OpenAI API → Response → Telegram
```

### Chat State Management
- Conversation history still persists (you may want to add external storage)
- Context tracking maintains Sylvia's personality continuity
- Same human-like behaviors and response processing

## 🎮 Sylvia's Personality Features

Sylvia is a 25-year-old chaotic gamer from Amman with:
- **Cultural Background**: Half-Palestinian, half-Lebanese
- **Gaming Expertise**: Junior game designer at Astra Nova
- **Language**: Natural mix of Arabic and English slang
- **Personality**: Sarcastic but caring, hype queen, roast master
- **Interests**: Gaming, pixel art, shawarma, late-night raids

### New Behavioral Patterns
- **Time Awareness**: Different energy levels throughout the day
- **Gaming Focus**: More engaged with gaming/tech topics
- **Emotional Range**: Responds appropriately to user's mood
- **Conversation Memory**: References past interactions naturally

## 🔧 Configuration Options

### Response Behavior
- **Reply Probability**: How often bot responds in groups (configurable in webhook.py)
- **Gaming Keywords**: Higher engagement with gaming/tech topics
- **Direct Messages**: Always responds in private chats
- **Mentions**: Always responds when bot is mentioned

### Context Management
- `CONTEXT_MSG_LIMIT`: Messages to keep in memory (15)
- `MAX_PROMPT_MSGS`: Messages sent to AI model (10)
- `MAX_RESPONSE_TOKENS`: Maximum response length (200)

## 🚀 Development

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run demo (showcases human-like features)
python demo.py

# For webhook testing, you'll need to use ngrok or similar
# to expose your local server to Telegram
```

### Webhook Management
```bash
# Set up webhook
python setup_webhook.py

# Remove webhook (for development)
python setup_webhook.py remove
```

## 🛡️ Security Notes

- API keys are environment variables only
- Optional webhook secret for additional security
- No sensitive data in source code
- Graceful error handling prevents information leaks

## 🔄 Migration from Railway

This project was migrated from Railway to Vercel with these changes:
- ❌ Removed Railway-specific files (`railway.toml`, `start.sh`, `Dockerfile`)
- ✅ Added Vercel serverless function architecture
- ✅ Created webhook-based Telegram integration
- ✅ Maintained all personality and AI features
- ✅ Added deployment automation scripts

---

Made with 💖 and lots of ☕ for the gaming community!
Now running serverless on Vercel! 🚀
- `REPLY_PROBABILITY`: How often bot responds in groups (default: 0.4)
- `MIN_RESPONSE_DELAY`: Minimum delay before responding (1.0s)
- `MAX_RESPONSE_DELAY`: Maximum delay before responding (4.0s)
- `TYPING_DELAY_PER_WORD`: Typing simulation speed (0.15s/word)

### Context Management
- `CONTEXT_MSG_LIMIT`: Messages to keep in memory (15)
- `MAX_PROMPT_MSGS`: Messages sent to AI model (10)
- `MAX_RESPONSE_TOKENS`: Maximum response length (200)

## 🚀 Future Enhancements

- [ ] External database integration for chat histories (Redis/PostgreSQL)
- [ ] Weather API integration for real weather responses
- [ ] Gaming news integration
- [ ] Voice message support
- [ ] Custom emoji reactions
- [ ] Group activity tracking
- [ ] Enhanced conversation threading

## 🛡️ Security Notes

- API keys are now environment variables only
- No sensitive data in source code
- Graceful error handling prevents information leaks
- Optional debug mode for development

---

Made with 💖 and lots of ☕ for the gaming community!
```