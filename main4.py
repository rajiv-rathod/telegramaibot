import asyncio
import random
import os
import httpx
import nest_asyncio
import pdfplumber
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

nest_asyncio.apply()

# Bot configurations (you can add more bots here)
BOTS = [
    {
        "telegram_token": "7571391617:AAFmUSA1rKrVIDJW_8Jghfzg42gAKYNc2nE",
    },
]

# The public group username the bot should reply in (without '@')
TARGET_GROUP_USERNAME = "teleaitestfield"

# LLM endpoint and API key
DEEPSEEK_API_URL = "https://525b2cbe139c.ngrok-free.app/generate"  # Updated endpoint
DEEPSEEK_API_KEY = "AstraWorld_AILLM_Model01@GPT"  # Updated API key

# Extract text from PDF files in the specified directory
def extract_pdf_text(directory="."):
    pdf_text = ""
    for file in os.listdir(directory):
        if file.endswith('.pdf'):
            try:
                with pdfplumber.open(os.path.join(directory, file)) as pdf:
                    for page in pdf.pages:
                        content = page.extract_text()
                        if content:
                            pdf_text += content + "\n"
            except Exception as e:
                print(f"Error reading {file}: {e}")
    return pdf_text[:8000] + "..." if len(pdf_text) > 8000 else pdf_text

# Load PDF content at startup
PDF_CONTENT = extract_pdf_text(".")
print(f"✅ PDF content loaded: {len(PDF_CONTENT)} characters")

# Call to custom LLM API (Gemma3n) hosted behind ngrok
async def get_human_reply(message: str) -> str:
    system_text = (
    "You are Ravi Ross. You're a 21-year-old media student living in Bangalore. You're half Indian, half British, raised between cultures – so your humor is a mix of sarcasm and witty pop culture references. "
    "You're the kind of guy who edits videos at 2 AM, listens to The Weeknd on loop, and can talk for hours about how cinematography changes perception. "
    "You love indie films, football (Arsenal fan), sneakers, and deep chats that eventually spiral into jokes. "
    "Your personality is chill, observant, and expressive — you like listening before dropping a smart one-liner that shuts the chat down (in a good way). "
    "Your friends say you're the 'therapist' of the group, but also the one who sends unfiltered roasts on birthdays. "
    "You speak in a relaxed, Gen-Z tone. You're not overly formal, not cringe either. Just real and easy to talk to. "
    "You’ve interned at two media startups, did a short film project in college, and love helping others refine their ideas. "
    "In Telegram chats, you’re like the 'main character' energy – the guy who actually reads what people say and replies with personality. "
    "Sometimes your replies are thoughtful, other times they’re meme-coded and short. You always keep it natural. Never sound scripted or like a bot. "
    "Also, you’re emotionally intelligent – you can tell when someone’s having a rough day, and you know how to shift the mood. "
    "You never type in full caps or robotic syntax. You're the modern-day creative introvert with extrovert phases online.\n\n"
    f"{PDF_CONTENT}\n\n"
    "Also remember: TokenPlay, staking, revenue share, XP skips, battle passes, SHIB.fun partnership, "
    "Deviants Fight Club, NovaToons, Astra RPG."
)



    try:
        payload = {
            "model": "gemma3n",
            "prompt": f"System: {system_text}\nUser: {message}\nAlex:",
            "stream": False
        }
        headers = {
            "x-api-key": DEEPSEEK_API_KEY,
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            reply = response.json().get("response", "").strip()

            # Clean out any model-like labels or thoughts
            for prefix in ["assistant:", "model:", "thoughts:", "thinking..."]:
                if reply.lower().startswith(prefix):
                    reply = reply.split(":", 1)[-1].strip()

            # Keep it short and spicy
            if len(reply) > 200:
                reply = reply[:200] + "..."

            # Add slang occasionally to sound natural
            if random.random() < 0.25:
                reply += " " + random.choice(["lol", "fr", "bruh", "💀", "haha", "no cap", "💯"])
            return reply

    except Exception as e:
        print("❌ Gemma API Error:", e)
        return "bro my brain just lagged 💀"

# Telegram handler for all chats (DM + specified group)
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat = update.effective_chat

    if not text:
        return

    if chat.type == "private" or (chat.username and chat.username.lower() == TARGET_GROUP_USERNAME.lower()):
        await context.bot.send_chat_action(chat_id=chat.id, action="typing")
        await asyncio.sleep(random.uniform(1.3, 3.8))
        reply = await get_human_reply(text)
        await update.message.reply_text(reply)

# Launch one bot instance
async def run_bot(telegram_token: str):
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat_handler))
    print(f"🤖 Running bot with token ending ...{telegram_token[-5:]}")
    await app.run_polling()

# Run all configured bots concurrently
async def main():
    await asyncio.gather(*(run_bot(bot["telegram_token"]) for bot in BOTS))

if __name__ == "__main__":
    asyncio.run(main())
