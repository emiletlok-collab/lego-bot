import asyncio
from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(text):
    async def send():
        await bot.send_message(
            chat_id=CHAT_ID,
            text=text
        )

    try:
        asyncio.run(send())
        print("✅ Message Telegram envoyé")
    except Exception as e:
        print("Erreur Telegram :", e)
