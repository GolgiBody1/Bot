import asyncio
from pyrogram import Client, filters

# ===== CONFIG =====
API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"

BROADCAST_MESSAGE = """
🎩 Cheap Nft Gifts On Sale 🎁

Price Starting Just 600₹ 💰
Good Model / Cool Background
Check Out On @GiftysView 🍰

Dm - @Swieniy For Deal 🏖️
Escrow Accepted ⚡
"""

app = Client("autobot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

@app.on_message(filters.me & filters.command("ping", prefixes="/"))
async def ping_command(client, message):
    await message.reply("✅ Bot is Online!")

async def auto_broadcast():
    await app.start()
    print("🚀 Userbot Started... Broadcasting every 3 minutes!")

    while True:
        count = 0
        async for dialog in app.get_dialogs():
            if dialog.chat.type in ["group", "supergroup", "private"]:
                try:
                    await app.send_message(dialog.chat.id, BROADCAST_MESSAGE)
                    print(f"✅ Sent to: {dialog.chat.title or dialog.chat.first_name}")
                    count += 1
                    await asyncio.sleep(3)  # safe delay
                except Exception as e:
                    print(f"❌ Error sending to {dialog.chat.title or dialog.chat.first_name}: {e}")

        print(f"🔄 Broadcast cycle complete. Messages sent: {count}")
        await asyncio.sleep(180)  # 3 minutes delay for next cycle

app.run(auto_broadcast())
