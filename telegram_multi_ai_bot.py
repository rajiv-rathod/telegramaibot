import asyncio
import random
from telethon import TelegramClient, events
import aiohttp

# --------- SETTINGS ----------
api_ids = [24314729]  # 🔁 Replace with your Telegram API IDs (max 10)
api_hashes = ['297c665e93500e0167b8432a9735d4f5']  # 🔁 Replace with your Telegram API hashes
phone_numbers = ['+96896267906']  # 🔁 Add up to 10 numbers
chat_id = -1002310025583  # 🔁 Replace with your target group/channel ID (use @userinfobot to get)

openrouter_api_key = "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"  # 🔁 Replace with your OpenRouter API key
openrouter_model = "nvidia/llama-3.1-nemotron-ultra-253b-v1:free"  # 
min_delay = 2  # ⏳ Min typing delay
max_delay = 5  # ⏳ Max typing delay

# Simple knowledge base
kb = {
    "hello": "Hi there! How can I help you today?",
    "how are you": "I'm doing great, thanks for asking!",
    "help": "Sure, tell me what you need help with.",
    "who made you": "I was built by Rajiv using OpenRouter AI and Telegram!",
}
# -----------------------------

clients = []

async def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "HTTP-Referer": "https://yourdomain.com/",  # Replace with your domain or just leave as is
        "Content-Type": "application/json"
    }
    body = {
        "model": openrouter_model,
        "messages": [{"role": "user", "content": prompt}],
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body) as resp:
            res = await resp.json()
            return res["choices"][0]["message"]["content"].strip()

def match_knowledge_base(text):
    for key in kb:
        if key.lower() in text.lower():
            return kb[key]
    return None

async def start_bot(index, phone):
    client = TelegramClient(f'session_{index}', api_ids[index], api_hashes[index])
    await client.start(phone=phone)
    print(f"[Client {index}] Logged in successfully.")

    @client.on(events.NewMessage(chats=chat_id))
    async def handler(event):
        if event.out: return  # Ignore own messages
        text = event.message.message
        print(f"[{index}] Incoming: {text}")

        # 1. Try to answer from knowledge base
        response = match_knowledge_base(text)

        # 2. Else use OpenRouter AI
        if not response:
            try:
                response = await ask_openrouter(text)
            except Exception as e:
                print(f"[{index}] Error getting OpenRouter response: {e}")
                response = "I'm thinking too hard... try again later!"

        # Simulate human delay
        delay = random.randint(min_delay, max_delay)
        print(f"[{index}] Typing for {delay}s...")
        await asyncio.sleep(delay)
        await event.reply(response)

    await client.run_until_disconnected()

async def main():
    tasks = []
    for i in range(min(len(phone_numbers), 10)):
        tasks.append(start_bot(i, phone_numbers[i]))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
