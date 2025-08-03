import os
import logging
import json
import random
from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from datetime import datetime

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("7258037258:AAHV21cupMdlDHETCsR_2sWxWVLEaJIp72Y")  # Railway/Heroku me set karo
DATA_FILE = "stats.json"  # persistent storage

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --------------- HELPER FUNCS ---------------
def load_stats():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"messages": 0, "groups": {}, "users": {}}

def save_stats(stats):
    with open(DATA_FILE, "w") as f:
        json.dump(stats, f)

stats = load_stats()

async def update_stats(update: Update):
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)

    stats["messages"] += 1
    stats["users"][user_id] = stats["users"].get(user_id, 0) + 1
    stats["groups"][chat_id] = stats["groups"].get(chat_id, 0) + 1
    save_stats(stats)

# ---------------- BASIC COMMANDS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I am your multi-feature bot.\nType /help to see commands.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = """
📌 **Commands List**:

**Basic**
/start - Start bot
/help - Show help
/ping - Check response
/about - About bot

**Admin**
/ban @user - Ban user
/unban @user - Unban user
/kick @user - Kick user
/mute @user - Mute user
/unmute @user - Unmute user
/promote @user - Promote user
/demote @user - Demote user
/purge - Delete recent messages
/lock links - Lock links
/unlock links - Unlock links

**Fun & Utility**
/id - Your Telegram ID
/userinfo @user - User info
/stats - Bot stats
/gstats - Group stats
/quote - Random quote
/gif - Random gif
/meme - Random meme

**Custom**
/deal - Create private deal group
"""
    await update.message.reply_text(commands, disable_web_page_preview=True)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = datetime.now()
    msg = await update.message.reply_text("🏓 Pinging...")
    end = datetime.now()
    latency = (end - start).microseconds // 1000
    await msg.edit_text(f"🏓 Pong! `{latency} ms`")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Multi-feature Telegram bot by Afzal.\nPersistent stats & admin tools included!")

# ---------------- ADMIN COMMANDS ----------------
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user's message to ban them.")
        return
    user = update.message.reply_to_message.from_user
    await update.message.chat.ban_member(user.id)
    await update.message.reply_text(f"🚫 Banned {user.mention_html()}", parse_mode="HTML")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /unban <user_id>")
        return
    user_id = int(context.args[0])
    await update.message.chat.unban_member(user_id)
    await update.message.reply_text(f"✅ Unbanned {user_id}")

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to kick someone.")
        return
    user = update.message.reply_to_message.from_user
    await update.message.chat.ban_member(user.id)
    await update.message.chat.unban_member(user.id)
    await update.message.reply_text(f"👢 Kicked {user.mention_html()}", parse_mode="HTML")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to mute someone.")
        return
    user = update.message.reply_to_message.from_user
    await update.message.chat.restrict_member(user.id, ChatPermissions(can_send_messages=False))
    await update.message.reply_text(f"🔇 Muted {user.mention_html()}", parse_mode="HTML")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to unmute someone.")
        return
    user = update.message.reply_to_message.from_user
    await update.message.chat.restrict_member(user.id, ChatPermissions(can_send_messages=True))
    await update.message.reply_text(f"🔊 Unmuted {user.mention_html()}", parse_mode="HTML")

async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages = []
    async for msg in update.message.chat.get_history(limit=50):
        messages.append(msg.message_id)
    await context.bot.delete_messages(update.message.chat_id, messages)
    await update.message.reply_text("🗑 Purged last 50 messages")

# ---------------- FUN & UTILITY ----------------
async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: `{update.effective_user.id}`")

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_msgs = stats.get("messages", 0)
    total_users = len(stats.get("users", {}))
    total_groups = len(stats.get("groups", {}))
    await update.message.reply_text(f"📊 **Bot Stats**\nUsers: {total_users}\nGroups: {total_groups}\nMessages: {total_msgs}")

async def gstats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gid = str(update.effective_chat.id)
    msg_count = stats["groups"].get(gid, 0)
    await update.message.reply_text(f"📈 Group Stats\nMessages: {msg_count}")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = [
        "Life is what happens when you're busy making other plans.",
        "Do what you can, with what you have, where you are.",
        "Happiness depends upon ourselves."
    ]
    await update.message.reply_text(random.choice(quotes))

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memes = ["😂 Meme 1", "🤣 Meme 2", "😎 Meme 3"]
    await update.message.reply_text(random.choice(memes))

async def gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gifs = ["https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif"]
    await update.message.reply_animation(random.choice(gifs))

# ---------------- CUSTOM /deal ----------------
async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_title = f"Deal_{user.first_name}_{random.randint(1000,9999)}"
    new_group = await context.bot.create_chat(chat_title, [user.id])
    await update.message.reply_text(f"✅ Private deal group created: {chat_title}")

# ---------------- MESSAGE TRACKER ----------------
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update_stats(update)

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("about", about))

    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("purge", purge))

    app.add_handler(CommandHandler("id", my_id))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("gstats", gstats))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("gif", gif))
    app.add_handler(CommandHandler("meme", meme))
    app.add_handler(CommandHandler("deal", deal))

    app.add_handler(MessageHandler(filters.ALL, track))  # track messages for stats

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
