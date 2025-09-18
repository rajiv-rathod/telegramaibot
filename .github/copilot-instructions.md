# Telegram AI Bot - AI Coding Instructions

This is a human-like Telegram AI bot featuring **Sylvia**, a chaotic gamer girl persona. The bot uses Telegram webhooks with OpenAI's GPT-4 API deployed on **Vercel** as serverless functions.

## Architecture Overview

### Core Components
- **`main.py`**: Original 1,693-line file containing bot logic (used as library)
- **`api/webhook.py`**: Vercel serverless function handling Telegram webhooks
- **Character System**: Sylvia's personality defined in extensive prompts with 1000+ catchphrases, roasts, and contextual responses
- **Webhook Architecture**: Serverless deployment responding to Telegram updates
- **Chat Context Monitoring**: Tracks conversation topics, mood, mentioned games, and user interactions per chat
- **Human-like Behaviors**: Sentiment analysis, time-based personality shifts, typing delays, and contextual emoji usage

### Data Flow
```
Telegram Webhook → Vercel Function → Sentiment Analysis → Chat Context Update → 
OpenAI API (with full context) → Human-like Post-processing → Response → Telegram API
```

## Key Patterns & Conventions

### Serverless Architecture Pattern
- **Webhook Handler**: `api/webhook.py` processes incoming Telegram updates
- **Stateless Functions**: Each request is independent, chat history persisted externally
- **Import Strategy**: Core bot logic imported from `main.py` as reusable components
- **Error Handling**: Graceful fallbacks with personality-appropriate responses

### Personality Architecture
- **Base Prompt**: 500+ line character definition in `BASE_SYLVIA` with location responses, food preferences, gaming origin story
- **Dynamic Responses**: 2000+ pre-written emotional responses (hype, salty, tired, excited, playful, supportive)
- **Catchphrases**: Massive collection organized by emotion type and context
- **Multi-language**: Natural Arabic/English mixing ("yalla", "wallah", "habibi", "aywa")

### Chat State Management
- **Per-chat Persistence**: JSON files in `chat_histories/` storing conversation history
- **Context Tracking**: `ChatContext` class monitors topics, games mentioned, mood, recent users
- **Memory Limits**: 15 messages in memory, 10 sent to AI model
- **Smart Engagement**: Dynamic reply probability based on gaming keywords, webhook context

### Human-like Response System
```python
# Time-based personality shifts
MORNING_HOURS = (6, 12)   # More coffee references, energetic
AFTERNOON_HOURS = (12, 18) # Productive gaming mode  
EVENING_HOURS = (18, 24)  # Social hype mode
NIGHT_HOURS = (0, 6)      # Tired but still gaming
```

### Response Processing Pipeline
1. **Webhook Validation** → security check and message extraction
2. **Sentiment Analysis** (TextBlob) → adjust temperature and emoji selection
3. **Context Integration** → recent conversation, mentioned games, mood tracking
4. **OpenAI API Call** → with dynamic temperature (1.1-1.4) based on mood/sentiment
5. **Post-processing** → `make_more_human()` adds slang, energy, contextual emojis
6. **Telegram Response** → send back via Telegram Bot API

## Critical Developer Workflows

### Vercel Deployment Setup
```bash
# Deploy to Vercel
vercel

# Set environment variables in Vercel dashboard:
# - OPENAI_API_KEY
# - OPENAI_ORG_ID  
# - TELEGRAM_BOT_TOKEN
# - WEBHOOK_SECRET (optional)

# Configure webhook after deployment
python setup_webhook.py
```

### Development Testing
- **Demo Script**: `python demo.py` showcases human-like features
- **Webhook Testing**: Use ngrok or similar for local webhook development
- **Debug Mode**: Console logs show response times, sentiment analysis, context tracking

### Deployment Patterns
- **Vercel Serverless**: Configured via `vercel.json` with Python runtime
- **Webhook Setup**: `setup_webhook.py` configures Telegram webhook URL
- **Environment Variables**: Stored in Vercel dashboard, accessed via `os.getenv()`
- **Auto-scaling**: Vercel handles traffic scaling automatically

## Unique Integration Points

### Webhook Architecture
- **Single Endpoint**: `/api/webhook` handles all Telegram updates
- **Security**: Optional webhook secret validation
- **Response Flow**: Process update → generate reply → send via Telegram API
- **Error Handling**: Fallback responses maintain personality even on failures

### OpenAI API Integration
- **Dynamic Context Building**: Assembles system prompt with recent conversation, time mood, sentiment analysis
- **Smart Token Management**: Truncates history intelligently, prevents context overflow
- **Temperature Tuning**: 1.3 base, +0.1 for evening hype, -0.2 for night mode, +0.1 for positive sentiment
- **Error Handling**: Fallback to personality-appropriate responses if API fails

### PDF Context Loading
- Uses `pdfplumber` to extract text from PDFs in project root for additional character context
- Truncates to 8000 characters, gracefully handles missing files
- Integrates into system prompt for enhanced personality depth

## Development Anti-Patterns to Avoid

- **Don't Remove Core Logic**: Keep `main.py` as importable library - personality coherence depends on it
- **Don't Remove Catchphrases**: The extensive pre-written responses are core to authenticity
- **Don't Simplify Context**: Rich conversation tracking is essential for human-like behavior
- **Don't Reduce Response Variety**: Multiple response paths prevent repetitive bot behavior
- **Don't Remove Time-based Logic**: Personality shifts by time of day are crucial for realism

## Vercel-Specific Considerations

### File Structure
```
api/
├── webhook.py              # Vercel serverless function
main.py                     # Core bot logic (imported)
vercel.json                 # Deployment configuration
requirements_vercel.txt     # Lighter dependencies for serverless
```

### Environment Variables
```bash
# Required in Vercel dashboard
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...
TELEGRAM_BOT_TOKEN=123456:ABC...
WEBHOOK_SECRET=optional_secret
```

### Webhook Management
```bash
# Set webhook URL to Vercel deployment
python setup_webhook.py

# Remove webhook (for development)
python setup_webhook.py remove
```

## Quick Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run demo (no Telegram required)
python demo.py

# Deploy to Vercel
vercel

# Configure webhook
TELEGRAM_BOT_TOKEN=your_token VERCEL_URL=https://your-app.vercel.app python setup_webhook.py
```

## Common Extension Points
- **New Features**: Add to special response patterns in `webhook.py` or core `get_human_reply()` function
- **Personality Tweaks**: Modify `BASE_SYLVIA` prompt or response collections in `main.py`
- **Webhook Security**: Enhance validation in `webhook.py`
- **External Storage**: Replace JSON file persistence with database integration
- **Context Enhancement**: Extend `ChatContext` class with new tracking capabilities