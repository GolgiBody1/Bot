from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7258037258:AAHV21cupMdlDHETCsR_2sWxWVLEaJIp72Y"  # Tumhara token

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! ✅ Bot is working.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commands:\n/start - Start bot\n/help - Help message")

# --- DM Reply Only ---
async def dm_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":  # Sirf DM
        await update.message.reply_text("Thanks for messaging me! 🤖")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # DM reply only
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dm_reply))

    print("🤖 Simple Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
