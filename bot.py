from pyrogram import Client, filters

# --- Your credentials added here ---
API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
BOT_TOKEN = "8479001314:AAEtthyPfZiuu3YHdVJYI-T_uIediUNytoM"
# ----------------------------------

app = Client("escrow_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Welcome to Escrow Bot!\n\n"
        "Type /deal and I will create a private escrow group for you with a join link."
    )

@app.on_message(filters.command("deal"))
async def create_deal(client, message):
    chat_title = "Escrow Deal Group"

    # 1️⃣ Create a private supergroup
    group = await client.create_supergroup(chat_title, "Auto-created private escrow group")

    # 2️⃣ Generate invite link
    invite = await client.create_chat_invite_link(group.id, name="Escrow Deal Link")

    # 3️⃣ Send link to user
    await message.reply(
        f"✅ A new escrow group has been created!\n\n"
        f"🔗 Join here: {invite.invite_link}\n\n"
        f"⚠️ Share this link with the other party to join."
    )

app.run()
