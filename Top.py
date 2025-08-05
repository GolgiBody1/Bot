import asyncio
from pyrogram import Client, filters

# ===== CONFIG =====
API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"

# Owner ID
OWNER_ID = 6998916494

# Allowed Users
allowed_users = {OWNER_ID}

broadcasting = False
broadcast_message = ""

app = Client("autobot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# ✅ Add Authorized User
@app.on_message(filters.user(OWNER_ID) & filters.command("add", prefixes="/"))
async def add_user(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: /add user_id")
    try:
        user_id = int(message.command[1])
        allowed_users.add(user_id)
        await message.reply(f"✅ User `{user_id}` added to bot access list.")
    except:
        await message.reply("⚠️ Invalid User ID format.")

# 📢 Start Broadcasting
@app.on_message(filters.user(list(allowed_users)) & filters.command("broadcast", prefixes="/"))
async def start_broadcast(client, message):
    global broadcasting, broadcast_message
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a message.\nUsage: /broadcast Your Message")
    broadcast_message = " ".join(message.command[1:])
    broadcasting = True
    await message.reply(f"✅ Broadcasting started!\nMessage: `{broadcast_message}`")

    while broadcasting:
        async for dialog in app.get_dialogs():
            if dialog.chat.type in ["group", "supergroup"]:
                try:
                    await app.send_message(dialog.chat.id, broadcast_message)
                    await asyncio.sleep(1)
                except:
                    pass
        await asyncio.sleep(180)  # 3 minutes

# ⛔ Stop Broadcasting
@app.on_message(filters.user(list(allowed_users)) & filters.command("stop", prefixes="/"))
async def stop_broadcast(client, message):
    global broadcasting
    broadcasting = False
    await message.reply("🛑 Broadcasting stopped.")

# ✅ Ping Command
@app.on_message(filters.user(list(allowed_users)) & filters.command("ping", prefixes="/"))
async def ping_command(client, message):
    await message.reply("✅ Bot is Online!")

print("🚀 Userbot Running...")
app.run()
