import re
from pyrogram import Client, filters

# ================== CONFIG ==================
API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"

app = Client("escrow_userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)


# ---------------- /add Command ----------------
@app.on_message(filters.command(["add", "Add"], prefixes="/") & filters.me)
async def add_deal(client, message):
    try:
        if not message.reply_to_message:
            return await message.reply("❌ Please reply to a DEAL INFO message.", quote=True)
        
        form_msg = message.reply_to_message
        deal_text = form_msg.text

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
                f"✅ Amount Received!\n"
                f"────────────────\n"
                f"👤 Buyer  : {buyer}\n"
                f"👤 Seller : {seller}\n"
                f"💰 Amount : ₹{amount}\n"
                f"💸 Release: ₹{release_amount}\n\n"
                f"🛡️ Escrowed by - {escrower}"
            ),
            reply_to_message_id=form_msg.id
        )

    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")


# ---------------- /complete Command ----------------
@app.on_message(filters.command(["complete", "Complete"], prefixes="/") & filters.me)
async def complete_deal(client, message):
    try:
        if not message.reply_to_message:
            return await message.reply("❌ Please reply to a DEAL INFO message.", quote=True)
        
        form_msg = message.reply_to_message
        deal_text = form_msg.text

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
                f"✅ Payment Released!\n"
                f"────────────────\n"
                f"👤 Buyer  : {buyer}\n"
                f"👤 Seller : {seller}\n"
                f"💰 Amount : ₹{amount}\n"
                f"💸 Released: ₹{release_amount}\n\n"
                f"🛡️ Released by - {escrower}"
            ),
            reply_to_message_id=form_msg.id
        )

    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")


print("🚀 Userbot Running...")
app.run()
