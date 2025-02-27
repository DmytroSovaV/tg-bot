from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv
import os

load_dotenv()  # Завантажує змінні з .env


TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
replyText = os.getenv("replyText")


async def forward_message(update: Update, context):
    user = update.message.from_user
    message_text = f"Ваш chat_id: {update.message.chat_id}"
    await update.message.reply_text(message_text)


async def start(update: Update, context):
    await update.message.reply_text(replyText)

async def forward_message(update: Update, context):
    user = update.message.from_user
    message_text = f"✉ Нове повідомлення від @{user.username}:\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message_text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    print("Бот запущений!")
    app.run_polling()

if __name__ == "__main__":
    main()
