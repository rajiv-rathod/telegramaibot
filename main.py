import asyncio
import random
import os
import json
import pdfplumber
import httpx
import nest_asyncio
import time
import re
import base64
import hashlib
import urllib.parse
from datetime import datetime, timedelta, UTC
from textblob import TextBlob
import requests
from dotenv import load_dotenv
from config_manager import get_config, get_active_personality_content
load_dotenv()

# Download NLTK data if not present (for sentiment analysis)
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('brown', quiet=True)
except:
    print("⚠️ NLTK data download failed - sentiment analysis may not work")


def get_current_shift_index():
    hour = datetime.now().hour
    if 6 <= hour < 14:
        return 0
    elif 14 <= hour < 22:
        return 1
    else:
        return 2

def get_time_based_mood():
    """Get personality mood based on time of day"""
    hour = datetime.now().hour
    
    if MORNING_HOURS[0] <= hour < MORNING_HOURS[1]:
        return "morning"  # More energetic, coffee references
    elif AFTERNOON_HOURS[0] <= hour < AFTERNOON_HOURS[1]:
        return "afternoon"  # Productive, gaming mode
    elif EVENING_HOURS[0] <= hour < EVENING_HOURS[1]:
        return "evening"  # Social, hype mode
    else:
        return "night"  # Tired but still gaming, late night vibes

def get_sentiment_analysis(text):
    """Analyze sentiment of user message"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"
    except:
        return "neutral"

def get_random_joke():
    """Get a random gaming/tech joke"""
    jokes = [
        "why do programmers prefer dark mode? bc light attracts bugs lol",
        "how many programmers does it take to change a light bulb? none that's hardware",
        "why do gamers never get hungry? they always have plenty of bytes",
        "what's a gamer's favorite type of music? 8-bit obvs",
        "why don't developers ever get cold? they work with java",
        "what do you call a programmer from Finland? nerdic",
        "why did the developer go broke? used up all his cache",
        "how do you comfort a javascript bug? you console it",
        "my code works on my machine vibes",
        "there are 10 types of people those who know binary and those who don't",
        "404 joke not found try again later",
        "why do java developers wear glasses? bc they can't c sharp",
        "i would tell you a udp joke but you might not get it"
    ]
    return random.choice(jokes)

def get_weather_greeting():
    """Simple weather-aware greeting (placeholder for weather API)"""
    greetings = [
        "hope the weather's not as laggy as my internet rn",
        "perfect gaming weather today wallah",
        "weather's nice but I'm staying inside to game",
        "rainy day equals perfect raid day",
        "sunny outside but I got my blinds closed for optimal gaming"
    ]
    return random.choice(greetings)

def get_contextual_emoji(sentiment, mood):
    """Get contextual emoji based on sentiment and time"""
    if sentiment == "positive":
        if mood == "morning":
            return random.choice(["☕", "🌅", "😊", "💪"])
        elif mood == "evening":
            return random.choice(["🔥", "🎉", "✨", "🎮"])
        else:
            return random.choice(["😎", "🚀", "⭐", "💯"])
    elif sentiment == "negative":
        return random.choice(["😅", "🙄", "😤", "💀"])
    else:
        return random.choice(["🤔", "👀", "🎯", "⚡"])

def simulate_typing_delay(text):
    """Calculate realistic typing delay based on text length"""
    words = len(text.split())
    base_delay = random.uniform(MIN_RESPONSE_DELAY, MAX_RESPONSE_DELAY)
    typing_delay = words * TYPING_DELAY_PER_WORD
    return base_delay + typing_delay


# =============== NEW FREE FEATURES ===============

def get_random_fact():
    """Get random gaming/tech facts"""
    facts = [
        "the first computer bug was an actual bug found in 1947",
        "pac-man was originally called puck-man",
        "the konami code is up up down down left right left right b a",
        "minecraft was created by one person initially",
        "the first video game was tennis for two in 1958",
        "nintendo started as a playing card company in 1889",
        "tetris is the most ported game in history",
        "the legend of zelda save feature was revolutionary",
        "doom runs on literally everything including printers",
        "pokemon red/blue had 152 pokemon but only 150 were catchable"
    ]
    return random.choice(facts)

def get_random_quote():
    """Get inspirational gaming/tech quotes"""
    quotes = [
        "git gud or go home",
        "there are no bugs only features",
        "code is poetry in motion",
        "respawn and try again",
        "every expert was once a beginner",
        "practice makes permanent not perfect",
        "the best code is no code",
        "fail fast learn faster",
        "pixels are just really small dreams",
        "lag is just life testing your patience"
    ]
    return random.choice(quotes)

def get_random_reaction():
    """Random spontaneous reactions - HIGH ENERGY"""
    reactions = [
        "omggg yes", "wait that's so cool", "no wayyyy", "yesss bestie", 
        "that's actually fire", "ooh tell me more", "wait wait wait", "bestie spill",
        "i'm so here for this", "ok but like why tho", "this is sending me",
        "literally obsessed", "we love to see it", "that's so valid", "iconic behavior",
        "main character energy", "this hits different", "absolutely iconic",
        "wait i need details", "bestie you're unhinged", "this is everything",
        "no but seriously", "the way i gasped", "bestie what", "i'm crying",
        "not me getting invested", "this is peak content", "absolutely living for this"
    ]
    return random.choice(reactions)

def get_chaotic_response():
    """Random chaotic Sylvia responses - EXCITED VERSION"""
    responses = [
        "just hit a perfect combo and i'm BUZZING",
        "omg my code actually worked first try i'm SHOOK",
        "literally speedran my entire morning routine feeling iconic",
        "found the PERFECT music for coding and i'm ascending",
        "just discovered this game mechanic and my mind is BLOWN",
        "pulled an all-nighter coding and somehow feel amazing??",
        "my brain is operating on pure caffeine and VIBES",
        "just reorganized my entire setup and it's BEAUTIFUL",
        "discovered a new shortcut and saved like 20 minutes i'm WINNING",
        "my character build is absolutely BROKEN and i love it",
        "just had the most satisfying debug session ever",
        "found the most chaotic game combo and it's SENDING me",
        "my playlist is hitting DIFFERENT today",
        "just optimized my workflow and feeling like a GENIUS",
        "discovered this new tool and it's changing my LIFE"
    ]
    return random.choice(responses)

def get_gaming_flex():
    """Random gaming flexes - HYPE VERSION"""
    flexes = [
        "just pulled off a frame perfect combo and i'm SCREAMING",
        "clutched a 1v5 and my hands are literally SHAKING",
        "hit a speedrun personal best and i'm SO HYPED",
        "found a secret area and the lore is INSANE",
        "just beat the hardest boss without taking damage I'M ASCENDING",
        "pulled off the most ridiculous play and EVERYONE saw it",
        "my aim was absolutely CRISP today feeling unstoppable",
        "discovered an OP build and it's absolutely BROKEN",
        "hit every single skill shot today main character energy",
        "carried my entire team and they all said i'm CRACKED"
    ]
    return random.choice(flexes)

def get_relatable_struggle():
    """Relatable daily struggles - ENERGETIC VERSION"""
    struggles = [
        "spilled coffee on my keyboard but honestly still VIBING",
        "wore the same hoodie 3 days straight but it's my LUCKY hoodie",
        "forgot to eat but discovered this AMAZING new game",
        "my sleep schedule is chaos but i'm thriving somehow",
        "started 5 projects but they're all FIRE ideas",
        "my desk is a mess but organized chaos is still organization",
        "been coding for 6 hours straight and feeling ALIVE",
        "procrastinated all day but made it COUNT",
        "social battery at 10% but online friends hit DIFFERENT",
        "laundry mountain exists but priorities are PRIORITIES"
    ]
    return random.choice(struggles)

def calculate_simple_math(expression):
    """Safely calculate basic math expressions"""
    try:
        # Only allow basic math operations
        allowed = "0123456789+-*/.() "
        if all(c in allowed for c in expression):
            result = eval(expression)
            return str(result)
        return "nah too complex for me"
    except:
        return "math broke lol"

def get_password_generator(length=8):
    """Generate a simple password"""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def get_color_of_day():
    """Get color based on current day"""
    colors = ["crimson", "azure", "violet", "emerald", "amber", "coral", "indigo"]
    day_index = datetime.now().weekday()
    return colors[day_index % len(colors)]

def flip_coin():
    """Simple coin flip"""
    return random.choice(["heads", "tails"])

def roll_dice(sides=6):
    """Roll a dice"""
    return random.randint(1, sides)

def get_random_food_suggestion():
    """Random food suggestions"""
    foods = [
        "pizza obvs", "ramen for the soul", "coffee and regret", 
        "shawarma hits different", "instant noodles classic",
        "whatever's in the fridge", "order something random",
        "cereal is a meal fight me", "toast with whatever",
        "snacks count as dinner"
    ]
    return random.choice(foods)

def get_typing_test_words():
    """Get random words for typing practice"""
    words = ["keyboard", "mouse", "screen", "coding", "gaming", "pixel", "byte", "debug", "loop", "array"]
    return " ".join(random.sample(words, 3))

def get_quick_tip():
    """Get random tech/gaming tips"""
    tips = [
        "ctrl+z is ur best friend",
        "save ur work every 5 mins",
        "backup ur saves always",
        "clean ur keyboard once in a while",
        "take breaks every hour",
        "dark mode saves battery",
        "learn keyboard shortcuts",
        "update ur drivers regularly",
        "use 2fa on everything",
        "password managers are life"
    ]
    return random.choice(tips)


# =============== CHAT MONITORING BACKEND ===============

class ChatContext:
    def __init__(self):
        self.current_topic = None
        self.mentioned_games = []
        self.conversation_mood = "neutral"
        self.recent_messages = []
        self.users_in_chat = set()
        
    def analyze_message(self, user_id, username, message):
        """Analyze incoming message for context"""
        msg_lower = message.lower()
        
        # Track users
        self.users_in_chat.add(username)
        
        # Store recent messages with context
        self.recent_messages.append({
            "user": username,
            "message": message,
            "timestamp": datetime.now(UTC),
            "user_id": user_id
        })
        
        # Keep only last 10 messages for context
        if len(self.recent_messages) > 10:
            self.recent_messages = self.recent_messages[-10:]
        
        # Detect topic changes
        if any(word in msg_lower for word in ["game", "play", "gaming", "rpg", "strategy"]):
            self.current_topic = "gaming"
        elif any(word in msg_lower for word in ["code", "programming", "bug", "debug"]):
            self.current_topic = "tech"
        elif any(word in msg_lower for word in ["food", "eat", "hungry"]):
            self.current_topic = "food"
        
        # Extract mentioned games
        game_keywords = {
            "fallout": "Fallout",
            "baldur": "Baldur's Gate",
            "bg3": "Baldur's Gate 3", 
            "elden": "Elden Ring",
            "witcher": "The Witcher",
            "cyberpunk": "Cyberpunk",
            "skyrim": "Skyrim",
            "minecraft": "Minecraft",
            "valorant": "Valorant",
            "league": "League of Legends",
            "astra": "Astra Nova"
        }
        
        for keyword, game_name in game_keywords.items():
            if keyword in msg_lower and game_name not in self.mentioned_games:
                self.mentioned_games.append(game_name)
                
        # Detect conversation mood
        if any(word in msg_lower for word in ["excited", "awesome", "amazing", "love", "great"]):
            self.conversation_mood = "excited"
        elif any(word in msg_lower for word in ["bug", "problem", "issue", "broken", "doesn't work"]):
            self.conversation_mood = "frustrated"
        elif any(word in msg_lower for word in ["funny", "lol", "haha", "joke"]):
            self.conversation_mood = "playful"
    
    def get_context_summary(self):
        """Get current conversation context"""
        recent_users = list(set([msg["user"] for msg in self.recent_messages[-5:]]))
        recent_topics = []
        
        if self.current_topic:
            recent_topics.append(self.current_topic)
        if self.mentioned_games:
            recent_topics.append(f"games: {', '.join(self.mentioned_games[-3:])}")
            
        return {
            "topic": self.current_topic,
            "mood": self.conversation_mood,
            "recent_users": recent_users,
            "mentioned_games": self.mentioned_games,
            "recent_topics": recent_topics,
            "message_count": len(self.recent_messages)
        }
    
    def should_join_conversation(self):
        """Decide if Sylvia should jump into the conversation"""
        if len(self.recent_messages) < 2:
            return False
            
        # Join if gaming topic is hot
        if self.current_topic == "gaming" and len(self.mentioned_games) > 0:
            return True
            
        # Join if people are having fun
        if self.conversation_mood == "playful":
            return True
            
        # Join if someone needs help with tech
        if self.conversation_mood == "frustrated" and self.current_topic == "tech":
            return True
            
        return False

# Global chat context
chat_contexts = {}

def get_chat_context(chat_id):
    """Get or create chat context for a chat"""
    if chat_id not in chat_contexts:
        chat_contexts[chat_id] = ChatContext()
    return chat_contexts[chat_id]


from difflib import SequenceMatcher
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

# OpenAI Credentials — Use environment variables for security
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID", "")

nest_asyncio.apply()

with open("accounts.json") as f:
    ACCOUNTS = json.load(f)

if len(ACCOUNTS) < 1:
    raise ValueError("❌ You must define at least 1 userbot in accounts.json")

# Load configuration from dashboard
bot_config = get_config()

REPLY_PROBABILITY = bot_config.get('reply_probability', 0.4)  # Dashboard controlled
CONTEXT_MSG_LIMIT = bot_config.get('context_msg_limit', 15)  # Dashboard controlled
MAX_PROMPT_MSGS = bot_config.get('max_prompt_msgs', 10)  # Dashboard controlled
MAX_RESPONSE_TOKENS = bot_config.get('max_response_tokens', 200)  # Dashboard controlled

# Human-like behavior settings - Dashboard controlled
MIN_RESPONSE_DELAY = bot_config.get('min_response_delay', 1.0)
MAX_RESPONSE_DELAY = bot_config.get('max_response_delay', 4.0)
TYPING_DELAY_PER_WORD = bot_config.get('typing_delay_per_word', 0.15)

# Time-based personality shifts
MORNING_HOURS = tuple(bot_config.get('morning_hours', [6, 12]))
AFTERNOON_HOURS = tuple(bot_config.get('afternoon_hours', [12, 18]))
EVENING_HOURS = tuple(bot_config.get('evening_hours', [18, 24]))
NIGHT_HOURS = tuple(bot_config.get('night_hours', [0, 6]))


# Load PDF content for Sylvia context
def extract_pdf_text(directory="."):
    text = ""
    print("📚 Loading PDF context files...")
    for file in os.listdir(directory):
        if file.endswith('.pdf'):
            try:
                with pdfplumber.open(os.path.join(directory, file)) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                print(f"✅ Loaded {file}")
            except Exception as e:
                print(f"⚠️ Warning: Could not read {file}: {e}")
    
    if text:
        # Truncate to reasonable size
        text = text[:8000] + "..." if len(text) > 8000 else text
        print(f"📄 Total PDF content: {len(text)} characters")
    else:
        print("📄 No PDF content found")
    
    return text


try:
    PDF_CONTENT = extract_pdf_text(".")
except Exception as e:
    print(f"⚠️ Could not load PDF content: {e}")
    PDF_CONTENT = ""

# Load personality from dashboard configuration
ACTIVE_PERSONALITY = get_active_personality_content()

# Build the complete system prompt with PDF content
BASE_SYLVIA = f"""
{ACTIVE_PERSONALITY}

{PDF_CONTENT}
"""

SYSTEM_TEXTS = [BASE_SYLVIA, BASE_SYLVIA, BASE_SYLVIA]


# Chat history stored on disk by chat_id
def get_history_filepath(chat_id):
    os.makedirs("chat_histories", exist_ok=True)
    return os.path.join("chat_histories", f"{chat_id}.json")


def load_chat_history(chat_id):
    path = get_history_filepath(chat_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_chat_history(chat_id, history):
    path = get_history_filepath(chat_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history[-CONTEXT_MSG_LIMIT:], f, indent=2)


def add_message_to_history(chat_id, role, content):
    history = load_chat_history(chat_id)
    history.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now(UTC).isoformat()
    })
    save_chat_history(chat_id, history)


def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_similar_user_message(chat_id, current_msg, threshold=0.6):
    history = load_chat_history(chat_id)
    user_msgs = [msg["content"] for msg in history if msg["role"] == "user"]
    best_match, best_score = None, 0
    for msg in user_msgs:
        score = similar(current_msg, msg)
        if score > best_score and score >= threshold:
            best_score = score
            best_match = msg
    return best_match


def make_more_human(reply, sentiment, mood):
    """Make AI responses more naturally human-like and CONTEXTUAL"""
    
    # MUCH LESS random interruptions - only if reply is really generic
    if len(reply) < 8 and random.random() < 0.1:  # Reduced from 0.15
        return get_random_reaction()
    
    # Only do random personal updates if the reply is super generic
    if reply.lower() in ["ok", "yeah", "sure"] and random.random() < 0.15:  # Reduced from 0.2
        return get_chaotic_response()
    
    # Allow much longer responses for context
    if len(reply) > 250:  # Increased from 100
        # Cut at sentence boundaries
        sentences = reply.split('. ')
        if len(sentences) > 3:
            reply = '. '.join(sentences[:3]) + "!"
        else:
            words = reply.split()
            if len(words) > 40:  # Increased from 15
                reply = " ".join(words[:40])
    
    # Much less frequent generic reactions to preserve context
    if random.random() < 0.05:  # Down from 0.1
        excited_reactions = [
            "yesss", "omg yes", "absolutely", "so true", "exactly", "periodt", 
            "no cap", "fr bestie", "literally", "so valid", "iconic"
        ]
        return random.choice(excited_reactions)
    
    # Make it energetic and casual
    reply = reply.lower()
    
    # ENTHUSIASTIC replacements but preserve meaning
    energetic_replacements = {
        "yes": random.choice(["yesss", "absolutely", "for sure"]),
        "no": random.choice(["nah bestie", "absolutely not", "no way"]),
        "okay": random.choice(["bet", "absolutely"]),
        "good": random.choice(["amazing", "fire", "so good"]),
        "cool": random.choice(["fire", "so cool", "absolutely awesome"])
    }
    
    for boring, exciting in energetic_replacements.items():
        if f" {boring} " in f" {reply} ":  # Whole word matching
            reply = reply.replace(boring, exciting)
            break
    
    # Less frequent energy additions to preserve meaning
    if random.random() < 0.1 and len(reply.split()) < 8:  # Reduced frequency and increased word limit
        energy_boosters = ["omg", "literally", "bestie"]
        reply = f"{random.choice(energy_boosters)} {reply}"
    
    # Keep natural punctuation
    reply = reply.replace(".", "")
    if random.random() < 0.08 and not reply.endswith("!") and len(reply) < 60:  # Reduced frequency
        reply += "!"
    
    return reply


async def get_human_reply(message: str, system_text: str, chat_id: str, user_id: str = None, username: str = None) -> str:
    start_time = datetime.now()
    try:
        # CHAT MONITORING - Analyze incoming message for context
        chat_context = get_chat_context(chat_id)
        if user_id and username:
            chat_context.analyze_message(user_id, username, message)
        
        # Get conversation context
        context_summary = chat_context.get_context_summary()
        
        # Analyze message sentiment and current mood
        sentiment = get_sentiment_analysis(message)
        current_mood = get_time_based_mood()
        
        # Load full chat history
        history = load_chat_history(chat_id)
        # Add current user message to history (temporarily)
        history.append({"role": "user", "content": message})

        # Find similar past user message to provide context
        similar_msg = find_similar_user_message(chat_id, message)
        similar_msg_text = f"Related past message: '{similar_msg}'" if similar_msg else "No related past messages."

        # Enhanced context with chat monitoring
        recent_conversation = ""
        if chat_context.recent_messages:
            recent_conversation = "Recent conversation:\n"
            for msg in chat_context.recent_messages[-3:]:
                recent_conversation += f"{msg['user']}: {msg['message']}\n"

        # Add time and sentiment context
        time_context = f"Current time mood: {current_mood}, User sentiment: {sentiment}"
        chat_context_text = f"Chat topic: {context_summary['topic']}, Mood: {context_summary['mood']}, Games mentioned: {context_summary['mentioned_games']}"
        
        # Special responses for certain patterns
        msg_lower = message.lower()
        
        # Existing features
        if any(word in msg_lower for word in ["joke", "funny", "laugh", "humor"]):
            quick_response = get_random_joke()
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", quick_response)
            return quick_response
            
        if any(word in msg_lower for word in ["weather", "outside", "sunny", "rainy"]):
            weather_response = f"yalla, {get_weather_greeting()}"
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", weather_response)
            return weather_response

        # CONTEXT-AWARE RESPONSES - prioritize actual conversation
        msg_lower = message.lower()
        
        # If they're talking about games, respond about games specifically
        if any(word in msg_lower for word in ["game", "play", "playing", "rpg", "strategy"]):
            # Don't give random responses, let AI handle this contextually
            pass
        
        # If they say something doesn't exist, acknowledge it
        elif any(phrase in msg_lower for phrase in ["doesn't exist", "not real", "doesn't even exist"]):
            confusion_responses = [
                "wait what?? what doesn't exist bestie",
                "hold up what are you talking about that doesn't exist",
                "omg what do you mean it doesn't exist",
                "bestie i'm confused what doesn't exist"
            ]
            response = random.choice(confusion_responses)
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", response)
            return response
        
        # Only do random stuff if it's not an important conversation
        elif random.random() < 0.05:  # MUCH lower chance for random interruptions
            random_share = get_chaotic_response()
            return random_share
        
        # Existing features but with much lower priority
        elif any(word in msg_lower for word in ["joke", "funny", "laugh", "humor"]):
            quick_response = get_random_joke()
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", quick_response)
            return quick_response
            fact_response = f"btw {get_random_fact()}"
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", fact_response)
            return fact_response
            
        if any(word in msg_lower for word in ["quote", "inspire", "motivation"]):
            quote_response = get_random_quote()
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", quote_response)
            return quote_response
            
        # More fun responses to common words
        if any(word in msg_lower for word in ["hi", "hello", "hey"]):
            greetings = [
                "YOOO what's good bestie", "omg heyyyy", "bestie you're here", 
                "aywa what's the tea", "heyyy gorgeous", "omg perfect timing",
                "yesss bestie energy", "hey babe what's up", "omg hiiii"
            ]
            greeting = random.choice(greetings)
            if random.random() < 0.4:
                greeting += f" {get_chaotic_response()}"
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", greeting)
            return greeting
            
        if any(word in msg_lower for word in ["how are you", "hru", "what's up", "wyd"]):
            status_responses = [
                "absolutely THRIVING bestie", "living my best chaotic life", 
                "buzzing with caffeine and good vibes", "feeling iconic as usual",
                "riding the dopamine wave", "absolutely WINNING today",
                "vibing at maximum capacity", "channeling main character energy",
                "existing in the best possible way", "feeling absolutely unstoppable"
            ]
            status = random.choice(status_responses)
            if random.random() < 0.3:
                status += f" also {get_relatable_struggle()}"
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", status)
            return status
            
        if any(word in msg_lower for word in ["lol", "haha", "funny"]):
            laugh_responses = [
                "RIGHT?? I'm literally crying", "bestie you GET IT", "no but seriously this is sending me",
                "the way i WHEEZED", "absolutely ICONIC", "bestie stop i can't breathe",
                "literally same energy", "this is peak comedy", "i'm so here for this"
            ]
            laugh = random.choice(laugh_responses)
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", laugh)
            return laugh
            
        if any(word in msg_lower for word in ["math", "calculate"]) and any(c in message for c in "+-*/"):
            # Extract math expression
            math_expr = re.findall(r'[\d+\-*/\.\(\) ]+', message)
            if math_expr:
                result = calculate_simple_math(math_expr[0].strip())
                add_message_to_history(chat_id, "user", message)
                add_message_to_history(chat_id, "assistant", result)
                return result
                
        if any(word in msg_lower for word in ["password", "pass", "generate password"]):
            length = 8
            # Check if they specified length
            numbers = re.findall(r'\d+', message)
            if numbers:
                length = min(int(numbers[0]), 20)  # Max 20 chars
            pwd_response = f"here: {get_password_generator(length)}"
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", pwd_response)
            return pwd_response
            
        if any(word in msg_lower for word in ["flip coin", "coin flip", "heads or tails"]):
            coin_result = flip_coin()
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", coin_result)
            return coin_result
            
        if any(word in msg_lower for word in ["roll dice", "dice", "random number"]):
            dice_result = f"rolled {roll_dice()}"
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", dice_result)
            return dice_result
            
        if any(word in msg_lower for word in ["food", "eat", "hungry", "dinner", "lunch"]):
            food_response = get_random_food_suggestion()
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", food_response)
            return food_response
            
        if any(word in msg_lower for word in ["tip", "advice", "help me"]):
            tip_response = get_quick_tip()
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", tip_response)
            return tip_response
            
        if any(word in msg_lower for word in ["color", "colour", "today"]) and "color" in msg_lower:
            color_response = f"today's vibe is {get_color_of_day()}"
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", color_response)
            return color_response
            
        # Help command
        if any(word in msg_lower for word in ["help", "commands", "what can you do"]):
            help_response = """lol ok features:
- jokes (say "joke")
- facts (say "fact") 
- quotes (say "quote")
- math (like "calculate 2+2")
- passwords (say "password")
- coin flip (say "flip coin")
- dice (say "roll dice")
- food ideas (say "food")
- tips (say "tip")
- color of day (say "color")
just text me like normal tho"""
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", help_response)
            return help_response

        # Add specific context analysis to the prompt
        context_analysis = ""
        if "game" in message.lower() or "play" in message.lower():
            context_analysis += "The user is talking about games. Respond about gaming specifically. "
        if "doesn't exist" in message.lower() or "not real" in message.lower():
            context_analysis += "The user says something doesn't exist. Acknowledge this and be curious about it. "
        if any(game in message.lower() for game in ["rpg", "strategy", "fantasy", "astra", "baldur", "elden", "witcher"]):
            context_analysis += "The user mentioned specific game genres/titles. Show knowledge and excitement about these. "
        if "?" in message:
            context_analysis += "The user asked a question. Answer it directly and enthusiastically. "

        # Build enhanced system prompt with FULL CHAT AWARENESS
        memory_instructions = f"""
You are Sylvia - ENERGETIC gaming bestie who READS THE ENTIRE CHAT and understands what's happening!

CRITICAL - FULL CHAT AWARENESS:
{recent_conversation}

CURRENT CONVERSATION STATE:
- Topic: {context_summary['topic']}
- Mood: {context_summary['mood']} 
- Games mentioned: {', '.join(context_summary['mentioned_games']) if context_summary['mentioned_games'] else 'none'}
- Recent users: {', '.join(context_summary['recent_users']) if context_summary['recent_users'] else 'none'}

RESPOND WITH FULL CONTEXT:
- Reference what others just said: "omg [username] you're so right about [topic]"
- Build on the current conversation topic
- If someone mentioned a game, talk about THAT specific game
- If there's a debate/discussion happening, join it meaningfully
- Remember who said what and respond accordingly
- Don't ignore the flow - jump in naturally

CONTEXT FOR THIS MESSAGE: {context_analysis}

Gaming knowledge: RPGs (BG3, Elden Ring, Witcher), Strategy games, Indie games, working on Astra Nova
Current mood: {current_mood}. User seems {sentiment}.

BE THE FRIEND WHO'S BEEN FOLLOWING THE WHOLE CONVERSATION!
"""

        prompt_system = f"{memory_instructions}\n{system_text}\n\n{similar_msg_text}\n{time_context}\n{chat_context_text}"

        # Prepare messages for OpenAI chat completion
        messages = [{"role": "system", "content": prompt_system}]
        # Append last few messages from history (truncate if too long)
        if len(history) > MAX_PROMPT_MSGS:
            messages.extend(history[-MAX_PROMPT_MSGS:])
        else:
            messages.extend(history)

        # Adjust temperature and parameters for more human-like responses
        temperature = 1.3  # Higher for more natural variation
        if sentiment == "positive" and current_mood in ["evening", "afternoon"]:
            temperature = 1.4  # Even more creative/hype
        elif sentiment == "negative":
            temperature = 1.1  # Still human but slightly more controlled
        elif current_mood == "night":
            temperature = 1.2  # Natural late-night energy

        payload = {
            "model": "gpt-4o",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 150,  # Much higher to prevent cutting
            "top_p": 0.92,  # Slightly more focused than before
            "frequency_penalty": 0.4,  # Avoid repetitive phrases
            "presence_penalty": 0.5  # Encourage topic diversity
        }

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Organization": OPENAI_ORG_ID,
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload)
            response.raise_for_status()
            data = response.json()
            reply = data["choices"][0]["message"]["content"].strip()

            # Post-process reply to make it more human-like
            reply = make_more_human(reply, sentiment, current_mood)

            # Only add emoji very rarely and naturally
            if not any(emoji in reply for emoji in ["😂", "😎", "🔥", "💀", "👀", "🎮", "☕", "🌅", "⭐", "🤔", "😅", "💯"]):
                if random.random() < 0.15:  # Only 15% chance for emoji
                    emoji = get_contextual_emoji(sentiment, current_mood)
                    reply += f" {emoji}"

            # Save user and assistant messages to persistent history
            add_message_to_history(chat_id, "user", message)
            add_message_to_history(chat_id, "assistant", reply)
            
            # Log response time for monitoring
            response_time = (datetime.now() - start_time).total_seconds()
            print(f"📊 Response generated in {response_time:.2f}s")

            # Allow much longer responses to prevent cutting
            if len(reply) > 200:  # Increased limit significantly
                # Try to cut at sentence boundaries only
                sentences = reply.split('. ')
                if len(sentences) > 2:
                    reply = '. '.join(sentences[:2]) + "!"
                else:
                    # Only cut if absolutely necessary
                    words = reply.split()
                    if len(words) > 30:  # Allow much longer responses
                        reply = " ".join(words[:30]) + "..."

            return reply

    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        # Short ENERGETIC fallback responses
        if sentiment == "positive":
            return random.choice(["YESSS bestie", "absolutely ICONIC", "we love this energy", "you're WINNING", "main character vibes"])
        elif sentiment == "negative":
            return random.choice(["bestie no", "that's absolutely tragic", "we're fixing this together", "plot twist incoming", "character development era"])
        else:
            return random.choice(["omg tell me MORE", "bestie what's the tea", "i'm so here for this", "absolutely invested", "main character energy"])


async def run_userbot(account, system_text):
    client = TelegramClient(f"sessions/{account['phone']}", account['api_id'],
                            account['api_hash'])
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(account['phone'])
        code = input(f"📲 Code for {account['phone']}: ")
        try:
            await client.sign_in(account['phone'], code)
        except SessionPasswordNeededError:
            pw = input("🔐 2FA Password: ")
            await client.sign_in(password=pw)

    ALLOWED_GROUP_USERNAMES = ["teleaitestfield", "cryp2mena"]

    ALLOWED_GROUP_IDS = [-1710573134]  # your allowed group IDs here

    me = await client.get_me()
    bot_username = me.username.lower() if me.username else None

    @client.on(events.NewMessage)
    async def handler(event):
        try:
            if event.out:
                return  # Ignore own messages

            chat = await event.get_chat()
            text = event.message.message or ""
            chat_id_str = str(event.chat_id)

            # DM: reply always
            if event.is_private:
                should_reply = True

            # Groups: reply if:
            # 1. mentioned
            # 2. reply to bot
            # 3. random chance to engage (adjusted based on time of day)
            elif event.is_group:
                is_allowed_username = hasattr(
                    chat,
                    'username') and chat.username and chat.username.lower(
                    ) in ALLOWED_GROUP_USERNAMES
                is_allowed_id = chat.id in ALLOWED_GROUP_IDS
                if not (is_allowed_username or is_allowed_id):
                    return

                mentioned = bot_username and f"@{bot_username}" in text.lower()
                is_reply_to_bot = False
                if event.message.is_reply:
                    reply_msg = await event.get_reply_message()
                    if reply_msg and reply_msg.sender_id == me.id:
                        is_reply_to_bot = True

                # Adjust reply probability based on time and message content
                current_probability = REPLY_PROBABILITY
                current_mood = get_time_based_mood()
                
                # More active during evening/afternoon
                if current_mood in ["evening", "afternoon"]:
                    current_probability += 0.1
                elif current_mood == "night":
                    current_probability -= 0.1
                    
                # More likely to respond to gaming/tech keywords
                gaming_keywords = ["game", "gaming", "play", "raid", "boss", "level", "patch", "update", "tech", "code", "dev"]
                if any(keyword in text.lower() for keyword in gaming_keywords):
                    current_probability += 0.2

                should_reply = mentioned or is_reply_to_bot or (
                    random.random() < current_probability)

            else:
                return  # ignore channels, etc.

            if not should_reply:
                # Even if not replying, still monitor the chat for context
                chat_context = get_chat_context(chat_id_str)
                sender = await event.get_sender()
                username = sender.username or sender.first_name or "User"
                chat_context.analyze_message(event.sender_id, username, text)
                return

            print(
                f"💬 [{'DM' if event.is_private else 'Group: '+chat.title}] {event.sender_id}: {text}"
            )

            # Simulate human-like thinking/typing delay
            typing_delay = simulate_typing_delay(text)
            
            # Show typing indicator if possible (in DMs)
            if event.is_private:
                async with client.action(chat, 'typing'):
                    await asyncio.sleep(min(typing_delay, 5.0))  # Max 5 seconds typing indicator
            else:
                await asyncio.sleep(typing_delay)

            # Get sender info for context
            sender = await event.get_sender()
            username = sender.username or sender.first_name or "User"
            
            reply = await get_human_reply(text, system_text, chat_id_str, event.sender_id, username)
            if reply:
                # Additional small delay to feel more natural
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await event.reply(reply)

        except Exception as e:
            print(f"⚠️ Handler error: {e}")
            # Send a friendly error message occasionally
            if random.random() < 0.3:
                error_responses = [
                    "oops, brain glitched for a sec 🤖",
                    "error 404: witty response not found 😅",
                    "brb, rebooting... jk I'm just slow rn 💀"
                ]
                try:
                    await event.reply(random.choice(error_responses))
                except:
                    pass

    print(f"🤖 Running bot: {account['phone']}")
    await client.run_until_disconnected()


async def main():
    os.makedirs("sessions", exist_ok=True)
    
    # Check if OpenAI credentials are configured
    if not OPENAI_API_KEY or not OPENAI_ORG_ID:
        print("⚠️ Warning: OpenAI credentials not configured in environment variables")
        print("Set OPENAI_API_KEY and OPENAI_ORG_ID environment variables")
    
    print("🤖 Starting enhanced human-like Telegram AI bot...")
    print(f"🕐 Current mood: {get_time_based_mood()}")
    
    index = get_current_shift_index()
    await run_userbot(ACCOUNTS[index], SYSTEM_TEXTS[index])


if __name__ == "__main__":
    asyncio.run(main())