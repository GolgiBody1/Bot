import re
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired

# ================== CONFIG ==================
API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"

app = Client("escrow_userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# ✅ Admin or Owner check
async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ["administrator", "creator"]:
            return True
        if getattr(member, "can_manage_chat", False):
            return True
    except ChatAdminRequired:
        return False
    except:
        pass
    return False

# ✅ Common function for both commands
async def process_deal(client, message, action_text, released_text):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("❌ Only admins can use this command.", quote=True)

    if not message.reply_to_message:
        return await message.reply("❌ Please reply to a DEAL INFO message.", quote=True)

    deal_text = message.reply_to_message.text

    buyer = re.search(r"Buyer\s*:\s*(\S+)", deal_text, re.IGNORECASE)
    buyer = buyer.group(1) if buyer else "N/A"

    seller = re.search(r"Seller\s*:\s*(\S+)", deal_text, re.IGNORECASE)
    seller = seller.group(1) if seller else "N/A"

    amount = re.search(r"Deal Amount\s*:\s*(\d+)", deal_text, re.IGNORECASE)
    amount = float(amount.group(1)) if amount else 0.0

    release_amount = round(amount * 0.98, 2)
    escrower = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

    await client.send_message(
        chat_id=message.chat.id,
        text=(
            f"{action_text}\n"
            f"────────────────\n"
            f"👤 Buyer  : {buyer}\n"
            f"👤 Seller : {seller}\n"
            f"💰 Amount : ₹{amount}\n"
            f"💸 {released_text}: ₹{release_amount}\n\n"
            f"🛡️ By - {escrower}"
        ),
        reply_to_message_id=message.reply_to_message.id
    )

    # ✅ Delete only the admin/owner's command message
    try:
        await client.delete_messages(chat_id=message.chat.id, message_ids=message.id)
    except:
        pass

# ✅ Commands
@app.on_message(filters.command(["add", "Add"], prefixes="/"))
async def add_deal(client, message):
    await process_deal(client, message, "✅ Amount Received!", "Release")

@app.on_message(filters.command(["complete", "Complete"], prefixes="/"))
async def complete_deal(client, message):
    await process_deal(client, message, "✅ Payment Released!", "Released")

print("🚀 Userbot Running...")
app.run()
