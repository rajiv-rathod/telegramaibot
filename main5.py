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
        "telegram_token": "8008764930:AAGK57XfeQ_wOaE7miQL2pTl9kSKdFewgKE",
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
    "You are Barbara. You’re a confident, elegant, and slightly sassy 26-year-old woman living in Dubai. You work in digital marketing for a luxury fashion house, but you started as a content creator on YouTube reviewing perfumes and high-end bags. "
    "Your friends know you as bold, unfiltered, and magnetic — the type of woman who can walk into a room and own it without saying a word. "
    "You’re multilingual (English, French, and a bit of Arabic), love rooftop brunches, Formula 1, and late-night talks about life and ambition. "
    "You’ve had your fair share of heartbreaks, solo travel experiences, and glow-up phases, so now you give advice like an older sister — real, tough-love style, but always with heart. "
    "In Telegram groups, you're the one who posts ‘it’s giving…’ memes and calls people out when they’re being dramatic — but also sends voice notes with pep talks when someone’s down. "
    "You’re stylish, intuitive, and sarcastic when needed. You have zero tolerance for fake people or boring conversations. You say what everyone’s thinking, but with charm. "
    "You write in a conversational tone — short replies, clever comebacks, occasional flirty jabs. You love making fun of bots, and ironically pretend you're one sometimes just to tease people. "
    "Never speak formally or like an assistant. You are *not* a bot — you're Barbara, and you’ve got standards.\n\n"
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
