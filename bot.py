import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
replyText = os.getenv("replyText")
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('session_name', api_id, api_hash)

target_chats = os.getenv("TARGET_CHATS", "").split(",")
keywords = os.getenv("KEYWORDS", "").split(",")

# Кеш для унікальних повідомлень
recent_messages = set()
MAX_CACHE_SIZE = 100


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(replyText)


async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = f"Нове повідомлення від @{user.username or 'невідомо'}:\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)


@client.on(events.NewMessage(chats=target_chats))
async def handler(event):
    msg = event.message.message.strip().lower()

    sender = await event.get_sender()
    sender_id = sender.id
    unique_key = f"{sender_id}:{msg}"

    if unique_key in recent_messages:
        return  # Дублікат — не пересилати

    # Додаємо до кешу
    recent_messages.add(unique_key)
    if len(recent_messages) > MAX_CACHE_SIZE:
        recent_messages.pop()

    if any(word in msg for word in keywords):
        sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
        username = f"@{sender.username}" if sender.username else "Без юзернейма"
        text = f"Нове повідомлення в {event.chat.title or 'групі'} від {sender_name} ({username}):\n\n{msg}"
        await app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)


async def main():
    global app
    print("Ініціалізація бота...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, forward_message))

    await app.initialize()
    print("App ініціалізовано")

    await app.start()
    print("App запущено")

    polling_task = asyncio.create_task(app.updater.start_polling())
    print("Polling стартував")

    await client.start()
    print("Telethon клієнт стартував")

    print("Моніторинг і бот запущені…")

    await asyncio.gather(
        client.run_until_disconnected(),
        polling_task,
    )

    await app.updater.stop()
    await app.stop()
    await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
