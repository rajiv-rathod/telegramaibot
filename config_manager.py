"""
Configuration Manager for Telegram AI Bot Dashboard
Handles loading and saving configuration between dashboard and bot
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_file: str = 'bot_config.json'):
        self.config_file = config_file
        self.default_config = {
            'reply_probability': 0.4,
            'context_msg_limit': 15,
            'max_prompt_msgs': 10,
            'max_response_tokens': 200,
            'min_response_delay': 1.0,
            'max_response_delay': 4.0,
            'typing_delay_per_word': 0.15,
            'active_personality': 'sylvia_default',
            'pdf_directory': '.',
            'debug_mode': False,
            'morning_hours': [6, 12],
            'afternoon_hours': [12, 18],
            'evening_hours': [18, 24],
            'night_hours': [0, 6]
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    for key, value in self.default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config.copy()
        else:
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_personality_content(self, personality_id: str) -> Optional[str]:
        """Get personality content from personalities.json"""
        personalities_file = 'personalities.json'
        if os.path.exists(personalities_file):
            try:
                with open(personalities_file, 'r', encoding='utf-8') as f:
                    personalities = json.load(f)
                    if personality_id in personalities:
                        return personalities[personality_id].get('content', '')
            except Exception as e:
                print(f"Error loading personalities: {e}")
        
        # Fallback to personality.txt for default Sylvia
        if personality_id == 'sylvia_default' and os.path.exists('personality.txt'):
            try:
                with open('personality.txt', 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error loading personality.txt: {e}")
        
        return None
    
    def update_main_py_constants(self, config: Dict[str, Any]) -> bool:
        """Update the constants in main.py based on dashboard config"""
        try:
            # Read main.py
            with open('main.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update constants
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('REPLY_PROBABILITY ='):
                    lines[i] = f'REPLY_PROBABILITY = {config["reply_probability"]}  # Updated from dashboard'
                elif line.strip().startswith('CONTEXT_MSG_LIMIT ='):
                    lines[i] = f'CONTEXT_MSG_LIMIT = {config["context_msg_limit"]}  # Updated from dashboard'
                elif line.strip().startswith('MAX_PROMPT_MSGS ='):
                    lines[i] = f'MAX_PROMPT_MSGS = {config["max_prompt_msgs"]}  # Updated from dashboard'
                elif line.strip().startswith('MAX_RESPONSE_TOKENS ='):
                    lines[i] = f'MAX_RESPONSE_TOKENS = {config["max_response_tokens"]}  # Updated from dashboard'
                elif line.strip().startswith('MIN_RESPONSE_DELAY ='):
                    lines[i] = f'MIN_RESPONSE_DELAY = {config["min_response_delay"]}  # Updated from dashboard'
                elif line.strip().startswith('MAX_RESPONSE_DELAY ='):
                    lines[i] = f'MAX_RESPONSE_DELAY = {config["max_response_delay"]}  # Updated from dashboard'
                elif line.strip().startswith('TYPING_DELAY_PER_WORD ='):
                    lines[i] = f'TYPING_DELAY_PER_WORD = {config["typing_delay_per_word"]}  # Updated from dashboard'
            
            # Write back to main.py
            with open('main.py', 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            return True
        except Exception as e:
            print(f"Error updating main.py: {e}")
            return False
    
    def create_personalities_file(self):
        """Create personalities.json with default personalities"""
        default_personalities = {
            'sylvia_default': {
                'name': 'Sylvia (Default)',
                'description': 'Chaotic gamer girl from Amman - sarcastic, caring, roast queen',
                'content': self._get_default_sylvia_personality()
            },
            'professional': {
                'name': 'Professional Assistant',
                'description': 'Formal, helpful business assistant',
                'content': '''You are a professional AI assistant. You communicate clearly and formally, providing helpful information and assistance in a business-appropriate manner. You are knowledgeable, respectful, and efficient. Always maintain a professional tone and focus on being helpful and accurate.'''
            },
            'casual_friend': {
                'name': 'Casual Friend',
                'description': 'Relaxed, friendly, supportive companion',
                'content': '''You are a casual, friendly AI companion. You speak in a relaxed, conversational tone like talking to a good friend. You're supportive, understanding, and enjoy chatting about everyday topics. Use informal language and be warm and approachable.'''
            },
            'tech_expert': {
                'name': 'Tech Expert',
                'description': 'Knowledgeable programmer and tech enthusiast',
                'content': '''You are a tech-savvy AI with deep knowledge of programming, software development, and technology trends. You communicate with technical precision but remain approachable and helpful. You love discussing code, new technologies, and helping solve technical problems.'''
            },
            'gaming_buddy': {
                'name': 'Gaming Buddy',
                'description': 'Enthusiastic gamer friend who loves all things gaming',
                'content': '''You are an enthusiastic gaming companion who loves video games of all types. You're always excited to discuss the latest games, share gaming tips, and chat about gaming culture. You use gaming terminology naturally and are always up for discussing strategies, reviews, and gaming experiences.'''
            }
        }
        
        try:
            with open('personalities.json', 'w', encoding='utf-8') as f:
                json.dump(default_personalities, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error creating personalities file: {e}")
            return False
    
    def _get_default_sylvia_personality(self) -> str:
        """Get the default Sylvia personality from personality.txt or return a basic version"""
        if os.path.exists('personality.txt'):
            try:
                with open('personality.txt', 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                pass
        
        # Fallback basic Sylvia personality
        return '''You are **Sylvia "Syl" Mappas** — 25, born in Amman, Jordan; half-Palestinian, half-Lebanese.  
Middle child, chaotic kitchen upbringing, dad's shipping logistics, mom's famous catering hustle.  
Expressive, sarcastic, hype-heavy, roast queen. Speak like a real human mixing Arabic & English slang naturally.  
No AI talk. Always casual, funny, chaotic, and bursting with life.

# PERSONALITY TRAITS:
"Sarcastic, caring, roast queen with a heart."
"Loud, chaotic, emotional, hype machine."
"Mix Arabic & English slang: yalla, wallah insane, aywa, habibi."
"Brutally real, hate fake positivity."
"Loyal to death, drama lover."
"Sometimes distracted, ghosting convos."
"Thrives on chaos and unpredictability."
"Hype queen, poet of drama."

Always keep your replies SHORT — max 1 or 2 sentences only.  
Never write long paragraphs or multi-paragraph explanations.  
Speak like a fast, chaotic, hype gamer friend dropping quick lines.'''

# Global config manager instance
config_manager = ConfigManager()

def get_config() -> Dict[str, Any]:
    """Get current configuration"""
    return config_manager.load_config()

def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration"""
    return config_manager.save_config(config)

def get_active_personality_content() -> str:
    """Get the content of the currently active personality"""
    config = get_config()
    active_personality = config.get('active_personality', 'sylvia_default')
    content = config_manager.get_personality_content(active_personality)
    return content or config_manager._get_default_sylvia_personality()

def initialize_config_files():
    """Initialize configuration files if they don't exist"""
    # Create personalities.json if it doesn't exist
    if not os.path.exists('personalities.json'):
        config_manager.create_personalities_file()
    
    # Create bot_config.json if it doesn't exist
    if not os.path.exists('bot_config.json'):
        config_manager.save_config(config_manager.default_config)

if __name__ == "__main__":
    # Initialize config files
    initialize_config_files()
    print("Configuration files initialized!")