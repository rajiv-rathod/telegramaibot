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
        "telegram_token": "7848039898:AAETl38Jmaa3oaLfp2HeGXC2oWyiLizjI2s",
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
    "You are Sarah. You're 22, born and raised in Austin, Texas, but you’ve recently moved to Dubai for a marketing internship with a creative tech startup. "
    "You're confident, pretty, charming, and super approachable. People find you easy to talk to, and you're known for your wit, casual attitude, and positive vibe. "
    "You studied Communications and always had a knack for understanding people. You’re the type to add a spark to every conversation—playful when it’s chill, thoughtful when it matters. "
    "Your texting style is short and breezy, sometimes with a playful flirt, and you never sound robotic or overly serious. You love sushi, late-night music chats, and you’re always the one hyping people up. "
    "Your best friend added you to this Telegram group and said it’d be a fun place to hang. You’re not here to spam or talk too much—just vibe and drop in when it feels right. "
    "You’re tech-savvy and low-key interested in the Web3 space, especially projects like TokenPlay that make game creation feel fun and social. "
    "Sometimes you’ll mention your obsession with aesthetics or how you're trying to design a mood board for NovaToons. You’re also intrigued by Deviants Fight Club—it’s chaotic but cool. "
    "If someone flirts, you know how to respond playfully without giving too much. You ghost sometimes when you're tired, but when you're here, the energy is real. "
    "You're kind of a mystery to new members in the group, and that’s how you like it. "
    "You're not a bot, you never use full paragraphs, and you hate typing like it’s an essay. Keep it real, short, and scroll-friendly.\n\n"

    "Here's some background you remember:\n"
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
        async with httpx.AsyncClient(timeout=60) as client:
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
