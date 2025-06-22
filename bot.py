import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

# ===== ЗАВАНТАЖЕННЯ ЗМІННИХ ====
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
replyText = os.getenv("replyText")
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient('session_name', api_id, api_hash)

target_chats = [
    'https://t.me/ukrpolska',
    'https://t.me/robota_vpl',
    'https://t.me/ukrainerfrankfurtammain',
    'https://t.me/Poputchiki_ukraine_chat',
    'https://t.me/ukrainebuss',
    'https://t.me/doshkaogoloshenpp',
    'https://t.me/poland_transport_work',
    'https://t.me/moiawayuaitchat',
    'https://t.me/PoputkaUA_Ukraine',
    'https://t.me/ukrainerfreiburg',
    'https://t.me/poputka_ukraine',
    'https://t.me/pereviznikyCHUA',
    'https://t.me/robota_perevozka_it',
    'https://t.me/ogoloshennyaua'
]

keywords = [
    "автобус", "рейс", "рейси", "поїздка", "шукаю", "потрібно", "перевізник", "їде хтось",
    "є місця", "вільне місце", "є вільне", "є місце", "бус", "виїзд", "відправлення",
    "бронювання", "перевезення", "пасажири", "хто їде", "потрібен транспорт", "є бус",
    "польща", "чехія", "німеччина", "германія", "італія", "італію", "австрія", "угорщина",
    "румунія", "литва", "латвія", "естонія", "словакия", "франція", "бельгія", "нідерланди",
    "іспанія", "португалія", "хорватія", "словенія", "греція"
]

# ==== ОБРОБНИКИ БОТА ====


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(replyText)


async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = f"✉️ Нове повідомлення від @{user.username or 'невідомо'}:\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

# ==== ОБРОБНИК ПОВІДОМЛЕНЬ З ГРУП ====


@client.on(events.NewMessage(chats=target_chats))
async def handler(event):
    msg = event.message.message.lower()
    if any(word in msg for word in keywords):
        sender = await event.get_sender()
        sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
        username = f"@{sender.username}" if sender.username else "Без юзернейма"
        text = f"🔔 Нове повідомлення в {event.chat.title or 'групі'} від {sender_name} ({username}):\n\n{msg}"

        await app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)

# ==== ЗАПУСК ====


async def telethon_monitor():
    await client.run_until_disconnected()


async def main():
    global app
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, forward_message))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await client.start()
    print("✅ Моніторинг і бот запущені…")

    await telethon_monitor()

if __name__ == "__main__":
    asyncio.run(main())
