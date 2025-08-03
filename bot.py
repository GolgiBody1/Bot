import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Your bot token
BOT_TOKEN = "7258037258:AAH9MbkHm46q0IipPBmVxW9Qz_MlIa0IszY"

# Optional: Admin user IDs (only they can use /admin commands)
ADMINS = [123456789]  # <- apna Telegram ID yaha daalna


# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! ✅ Bot is working in both DM and Groups.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📌 Available Commands:\n"
        "/start - Bot start kare\n"
        "/help - Ye help message\n"
        "/admin - Sirf admin use kar sakta hai\n"
    )
    await update.message.reply_text(help_text)


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ADMINS:
        await update.message.reply_text("🔑 Admin command executed!")
    else:
        await update.message.reply_text("❌ You are not allowed to use this command.")


# --- Auto reply to any text ---
async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hello" in text:
        await update.message.reply_text("Hi there! 👋")
    elif "ping" in text:
        await update.message.reply_text("Pong! 🏓")
    else:
        await update.message.reply_text("I am an advanced bot 🤖")


# --- Main function ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("admin", admin_command))

    # Auto reply in groups & DMs
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))

    print("🤖 Advanced Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
