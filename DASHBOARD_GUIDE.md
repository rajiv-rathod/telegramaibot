# Telegram AI Bot Dashboard Documentation

## 🎯 Overview

The Telegram AI Bot Dashboard provides complete web-based control over your bot's functionality, personalities, and configuration. No coding required!

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- All dependencies installed (`pip install -r requirements.txt`)
- Telegram API credentials configured

### Quick Start
```bash
# Start both dashboard and bot
python start_bot.py

# Or start just the dashboard
python dashboard.py
```

Dashboard will be available at: **http://localhost:5000**

## 📋 Dashboard Features

### 1. 📊 Overview Dashboard
- **Real-time Status**: Bot online/offline status
- **Statistics**: Active sessions, messages today, uptime
- **Current Personality**: See which personality is active
- **Quick Actions**: Fast access to common tasks

### 2. 🎭 Personality Management

#### Default Personalities Included:
- **Sylvia (Default)**: Chaotic gamer girl from Amman - sarcastic, caring, roast queen
- **Professional Assistant**: Formal, helpful business assistant
- **Casual Friend**: Relaxed, friendly, supportive companion  
- **Tech Expert**: Knowledgeable programmer and tech enthusiast
- **Gaming Buddy**: Enthusiastic gamer friend

#### Custom Personalities:
- Create unlimited custom personalities
- Rich text editor for personality prompts
- Support for multi-paragraph personality descriptions
- Real-time personality switching without bot restart

#### How to Create Custom Personality:
1. Go to Personality section
2. Click "Add Custom Personality" 
3. Enter name and description
4. Write full personality prompt in the editor
5. Save and select to activate

### 3. 📄 PDF Management

#### Features:
- Upload PDF documents for bot context
- Support for multiple PDFs per bot instance
- Different PDFs for different companies/use cases
- Automatic text extraction and integration
- File size and modification tracking

#### Supported Use Cases:
- Company-specific knowledge bases
- Product documentation
- Training materials
- FAQ documents
- Any PDF content for bot context

### 4. ⚙️ Configuration Control

#### Response Behavior:
- **Reply Probability**: How often bot responds (0.0 - 1.0)
- **Context Message Limit**: How many messages to remember
- **Max Response Tokens**: Maximum response length

#### Timing Settings:
- **Response Delays**: Min/max delays before responding
- **Typing Simulation**: Delay per word to simulate human typing
- **Human-like Behavior**: Natural conversation flow

#### Advanced Options:
- **Debug Mode**: Enhanced logging and error reporting
- **Time-based Personality**: Mood shifts throughout the day

### 5. 👥 Bot Accounts Management

#### Features:
- Manage multiple Telegram bot accounts
- Add/remove bot instances dynamically
- Configure API credentials per account
- Support for company-specific bot instances

#### Multi-Company Setup:
1. Add separate accounts for each company
2. Upload company-specific PDFs
3. Create company-specific personalities
4. Run multiple bot instances simultaneously

### 6. 🐛 Debug & Monitoring

#### Debug Features:
- **Real-time Logs**: Live bot activity monitoring
- **Error Tracking**: Catch and debug issues quickly
- **Performance Metrics**: Response times and usage stats
- **Configuration History**: Track changes over time

#### Troubleshooting:
- Clear logs to reset debug output
- Enable debug mode for detailed information
- Monitor bot status in real-time

## 🏢 Multi-Company Deployment

### Setup for Multiple Companies:

1. **Create Company-Specific Configurations**:
   - Upload company PDFs to PDF Management
   - Create company-specific personalities
   - Configure separate Telegram accounts

2. **Personality Examples for Different Companies**:
   ```
   Company A: Professional, formal, product-focused
   Company B: Casual, friendly, support-focused  
   Company C: Technical, expert, developer-focused
   ```

3. **PDF Organization**:
   ```
   company_a_manual.pdf
   company_b_faq.pdf
   company_c_docs.pdf
   ```

4. **Account Management**:
   - Account 1: Company A bot
   - Account 2: Company B bot  
   - Account 3: Company C bot

## 🎨 Customization

### Logo Integration
- Place your logo file in `dashboard/static/images/`
- Update the navbar brand section in the HTML template
- Animated logo effects already included in CSS

### Styling Customization
- Edit `dashboard/static/css/dashboard.css` for custom styles
- Responsive design works on all devices
- Bootstrap 5 framework for easy customization

### Adding New Features
- Dashboard is modular and extensible
- Add new routes in `dashboard.py`
- Create new template sections as needed
- All API endpoints are documented in the code

## 🔧 Technical Details

### File Structure:
```
├── dashboard.py              # Main dashboard application
├── config_manager.py         # Configuration management
├── dashboard/
│   ├── templates/
│   │   └── dashboard.html    # Main dashboard UI
│   └── static/
│       ├── css/
│       │   └── dashboard.css # Dashboard styles
│       └── js/
│           └── dashboard.js  # Dashboard functionality
├── personalities.json        # Personality presets storage
├── bot_config.json          # Bot configuration storage
└── pdf_storage/             # Uploaded PDFs directory
```

### Configuration Files:
- `bot_config.json`: Bot behavior parameters
- `personalities.json`: Personality presets and custom personalities
- `accounts.json`: Telegram account configurations

### API Endpoints:
- `GET/POST /api/config`: Bot configuration
- `GET/POST /api/personalities`: Personality management  
- `GET /api/pdfs`: PDF file listing
- `POST /api/upload_pdf`: PDF file upload
- `POST /api/delete_pdf`: PDF file deletion
- `GET/POST /api/accounts`: Account management
- `GET /api/bot/status`: Bot status monitoring
- `POST /api/bot/start|stop`: Bot control
- `GET /api/logs`: Debug logs

## 🛡️ Security Notes

- Dashboard designed for local/private network use
- No authentication required (suitable for personal/internal use)
- API keys stored in environment variables
- File uploads restricted to PDF files only
- No external dependencies for core functionality

## 🚀 Future Enhancements

Ready for expansion:
- User authentication system
- Role-based access control
- Cloud deployment support
- Advanced analytics dashboard
- Webhook integrations
- API rate limiting
- Multi-language support

## 💡 Tips & Best Practices

1. **Start with Dashboard**: Configure everything through the web interface
2. **Test Personalities**: Use the editor to test personality changes
3. **PDF Organization**: Keep PDFs organized by company/purpose
4. **Regular Backups**: Save your personality configurations
5. **Monitor Logs**: Use debug section to troubleshoot issues
6. **Performance Tuning**: Adjust timing settings based on usage

## ❓ Troubleshooting

### Common Issues:

**Dashboard won't start**:
- Check if port 5000 is available
- Ensure all dependencies are installed
- Verify Python version is 3.8+

**Bot won't connect**:
- Check Telegram API credentials in accounts.json
- Verify .env file has OpenAI API key
- Check network connectivity

**Personalities not working**:
- Verify personality content is properly formatted
- Check that personality is selected in dashboard
- Restart bot after personality changes

**PDF upload fails**:
- Ensure file is valid PDF
- Check file size (recommended < 10MB)
- Verify write permissions to pdf_storage directory

## 🤝 Support

For issues or feature requests:
1. Check the debug logs in the dashboard
2. Review this documentation
3. Check the repository issues page
4. Create detailed issue reports with logs

---

Made with 💖 for the Telegram bot community!