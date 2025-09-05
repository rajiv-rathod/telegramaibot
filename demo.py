#!/usr/bin/env python3
"""
Demo script showing the enhanced human-like features of the Telegram AI bot
This demonstrates the improvements made to make Sylvia more human-like
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import (
    get_time_based_mood, 
    get_sentiment_analysis, 
    get_random_joke, 
    get_weather_greeting,
    get_contextual_emoji,
    simulate_typing_delay
)

def demo_human_features():
    print("🤖 Enhanced Human-like Telegram AI Bot Demo")
    print("=" * 50)
    
    # Time-based personality
    print("\n⏰ Time-based Personality:")
    current_mood = get_time_based_mood()
    print(f"Current mood: {current_mood}")
    
    # Sentiment analysis
    print("\n💭 Sentiment Analysis:")
    test_messages = [
        "I love gaming so much!",
        "This is really frustrating...",
        "Hey, how are you doing?",
        "OMG this patch is AMAZING!! 🔥"
    ]
    
    for msg in test_messages:
        sentiment = get_sentiment_analysis(msg)
        emoji = get_contextual_emoji(sentiment, current_mood)
        delay = simulate_typing_delay(msg)
        print(f"'{msg}' → Sentiment: {sentiment} {emoji} (Response delay: {delay:.1f}s)")
    
    # Open-source features
    print("\n🎮 Open-source Features:")
    print(f"Random joke: {get_random_joke()}")
    print(f"Weather greeting: {get_weather_greeting()}")
    
    # Human-like timing
    print("\n⚡ Human-like Response Timing:")
    timing_tests = [
        "Hi!",
        "What's your favorite game?",
        "Can you help me with this really complex programming problem that involves multiple steps?"
    ]
    
    for msg in timing_tests:
        delay = simulate_typing_delay(msg)
        print(f"'{msg[:30]}...' → {delay:.2f}s delay")
    
    print("\n✨ Key Improvements Made:")
    print("- ❌ Removed Solace integration (as requested)")
    print("- 🧠 Added sentiment analysis for emotional responses")
    print("- ⏰ Time-based personality shifts")
    print("- 🎯 Contextual emoji selection")
    print("- ⚡ Human-like typing delays")
    print("- 🎮 Gaming/tech topic detection")
    print("- 🔒 Secure environment variable configuration")
    print("- 😄 Open-source joke/weather features")
    print("- 🤖 Enhanced error handling with personality")
    print("- 📚 Better conversation memory and context")

if __name__ == "__main__":
    demo_human_features()