# Enhanced Human-like Telegram AI Bot 🤖✨

An improved Telegram AI bot featuring Sylvia, a chaotic gamer girl persona from Amman, Jordan. This bot has been enhanced to be as human-like as possible with open-source features.

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
- **Security Enhancement**: API keys moved to environment variables
- **Better Response Quality**: Adjusted temperature based on context
- **Improved Context Handling**: More conversation history and better prompts
- **Human-like Response Timing**: Variable delays and typing indicators

## 📁 File Structure
```
├── main.py                 # Main bot logic with enhancements
├── personality.txt         # Enhanced Sylvia persona with new behaviors
├── requirements.txt        # Updated dependencies
├── .env.example           # Environment variables template
├── accounts.json          # Telegram account configurations
└── chat_histories/        # Conversation memory storage
```

## 🛠️ Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Set Required Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_ORG_ID`: Your OpenAI organization ID

4. **Configure Telegram Accounts**:
   Edit `accounts.json` with your Telegram API credentials

5. **Run the Bot**:
   ```bash
   python main.py
   ```

## 🎯 Key Enhancements Made

### Human-like Conversation Flow
- **Dynamic Response Timing**: Simulates reading and typing time
- **Mood Adaptation**: Responds differently based on time of day
- **Emotional Intelligence**: Analyzes and responds to user sentiment
- **Contextual Awareness**: Better memory and conversation threading

### Open-Source Integrations
- **TextBlob** for sentiment analysis
- **Requests** for future API integrations
- **Enhanced logging** for better debugging
- **Modular design** for easy feature additions

### Code Quality Improvements
- **Security**: No hardcoded API keys
- **Error Handling**: Graceful fallbacks with personality
- **Documentation**: Better comments and structure
- **Modularity**: Separated concerns for maintainability

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
- `REPLY_PROBABILITY`: How often bot responds in groups (default: 0.4)
- `MIN_RESPONSE_DELAY`: Minimum delay before responding (1.0s)
- `MAX_RESPONSE_DELAY`: Maximum delay before responding (4.0s)
- `TYPING_DELAY_PER_WORD`: Typing simulation speed (0.15s/word)

### Context Management
- `CONTEXT_MSG_LIMIT`: Messages to keep in memory (15)
- `MAX_PROMPT_MSGS`: Messages sent to AI model (10)
- `MAX_RESPONSE_TOKENS`: Maximum response length (200)

## 🚀 Future Enhancements

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