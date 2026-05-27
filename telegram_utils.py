import asyncio
from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

async def send_message_async(text):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )

def send_telegram_message(text):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_message_async(text))
        loop.close()

        print("✅ Message Telegram envoyé")

    except Exception as e:
        print("Erreur Telegram :", e)
