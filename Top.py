import re
import random
import json
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus

# ================== CONFIG ==================
API_ID = 26014459  # अपना डालें
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH"
DATA_FILE = "data.json"
LOG_CHANNEL_ID = -1002330347621  # लॉग चैनल ID

app = Client("escrow_userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# ================== LOAD / SAVE DATA ==================
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"groups": {}, "global": {"total_deals": 0, "total_volume": 0, "total_fee": 0.0, "escrowers": {}}}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# ================== HELPERS ==================
async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
    except:
        return False

def init_group(chat_id: str):
    if chat_id not in data["groups"]:
        data["groups"][chat_id] = {
            "deals": {},
            "total_deals": 0,
            "total_volume": 0,
            "total_fee": 0.0,
            "escrowers": {}
        }

def update_escrower_stats(group_id: str, escrower: str, amount: float, fee: float):
    g = data["groups"][group_id]
    g["total_deals"] += 1
    g["total_volume"] += amount
    g["total_fee"] += fee
    g["escrowers"][escrower] = g["escrowers"].get(escrower, 0) + amount

    data["global"]["total_deals"] += 1
    data["global"]["total_volume"] += amount
    data["global"]["total_fee"] += fee
    data["global"]["escrowers"][escrower] = data["global"]["escrowers"].get(escrower, 0) + amount

    save_data()

# ================== /add Command ==================
@app.on_message(filters.command("add") & filters.group)
async def add_deal(client, message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return

    await message.delete()

    if not message.reply_to_message or not message.reply_to_message.text:
        await message.reply("❌ Please reply to the DEAL INFO form message!")
        return

    original_text = message.reply_to_message.text
    chat_id = str(message.chat.id)
    reply_id = str(message.reply_to_message.id)
    init_group(chat_id)

    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    amount_match = re.search(r"DEAL AMOUNT\s*:\s*₹?\s*([\d.]+)", original_text, re.IGNORECASE)

    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"

    if not amount_match:
        await message.reply("❌ Amount not found in the form!")
        return

    amount = float(amount_match.group(1))
    group_data = data["groups"][chat_id]
    if reply_id not in group_data["deals"]:
        trade_id = f"TID{random.randint(100000, 999999)}"
        fee = round(amount * 0.02, 2)
        release_amount = round(amount - fee, 2)
        group_data["deals"][reply_id] = {
            "trade_id": trade_id,
            "release_amount": release_amount,
            "completed": False
        }
    else:
        trade_id = group_data["deals"][reply_id]["trade_id"]
        release_amount = group_data["deals"][reply_id]["release_amount"]
        fee = round(amount - release_amount, 2)

    escrower = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    update_escrower_stats(chat_id, escrower, amount, fee)

    msg = (
        "✅ <b>Amount Received!</b>\n"
        "────────────────\n"
        f"👤 <b>Buyer</b>  : {buyer}\n"
        f"👤 <b>Seller</b> : {seller}\n"
        f"💰 <b>Amount</b> : ₹{amount}\n"
        f"💸 <b>Release</b>: ₹{release_amount}\n"
        f"⚖️ <b>Fee</b>    : ₹{fee}\n"
        f"🆔 <b>Trade ID</b>: #{trade_id}\n"
        "────────────────\n"
        f"🛡️ <b>Escrowed by</b> {escrower}"
    )

    await message.chat.send_message(msg, reply_to_message_id=message.reply_to_message.id, parse_mode="HTML")
    save_data()

# ================== /complete Command ==================
@app.on_message(filters.command("complete") & filters.group)
async def complete_deal(client, message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return

    await message.delete()

    if not message.reply_to_message or not message.reply_to_message.text:
        await message.reply("❌ Please reply to the DEAL INFO form message!")
        return

    chat_id = str(message.chat.id)
    reply_id = str(message.reply_to_message.id)
    init_group(chat_id)

    group_data = data["groups"][chat_id]
    deal_info = group_data["deals"].get(reply_id)

    if not deal_info:
        await message.reply("❌ This deal was never added with /add!")
        return

    if deal_info["completed"]:
        await message.reply("❌ This deal is already completed!")
        return

    deal_info["completed"] = True
    save_data()

    original_text = message.reply_to_message.text
    buyer_match = re.search(r"BUYER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    seller_match = re.search(r"SELLER\s*:\s*(@\w+)", original_text, re.IGNORECASE)
    buyer = buyer_match.group(1) if buyer_match else "Unknown"
    seller = seller_match.group(1) if seller_match else "Unknown"

    trade_id = deal_info["trade_id"]
    release_amount = deal_info["release_amount"]
    escrower = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

    msg = (
        "✅ <b>Deal Completed!</b>\n"
        "────────────────\n"
        f"👤 <b>Buyer</b>   : {buyer}\n"
        f"👤 <b>Seller</b>  : {seller}\n"
        f"💸 <b>Released</b>: ₹{release_amount}\n"
        f"🆔 <b>Trade ID</b>: #{trade_id}\n"
        "────────────────\n"
        f"🛡️ <b>Escrowed by</b> {escrower}"
    )
    await message.chat.send_message(msg, reply_to_message_id=message.reply_to_message.id, parse_mode="HTML")

    log_msg = (
        "📜 <b>Deal Completed (Log)</b>\n"
        "────────────────\n"
        f"👤 <b>Buyer</b>   : {buyer}\n"
        f"👤 <b>Seller</b>  : {seller}\n"
        f"💸 <b>Released</b>: ₹{release_amount}\n"
        f"🆔 <b>Trade ID</b>: #{trade_id}\n"
        f"🛡️ <b>Escrowed by</b> {escrower}\n\n"
        f"📌 <b>Group</b>: {message.chat.title} ({message.chat.id})"
    )
    await app.send_message(LOG_CHANNEL_ID, log_msg, parse_mode="HTML")

# ================== /stats Command ==================
@app.on_message(filters.command("stats") & filters.group)
async def group_stats(client, message):
    chat_id = str(message.chat.id)
    init_group(chat_id)
    g = data["groups"][chat_id]

    escrowers_text = "\n".join([f"{name} = ₹{amt}" for name, amt in g["escrowers"].items()]) or "No deals yet"

    msg = (
        f"📊 Escrow Bot Stats\n\n"
        f"{escrowers_text}\n\n"
        f"🔹 Total Deals: {g['total_deals']}\n"
        f"💰 Total Volume: ₹{g['total_volume']}\n"
        f"💸 Total Fee Collected: ₹{g['total_fee']}\n"
    )
    await message.reply(msg)

# ================== /gstats Command ==================
@app.on_message(filters.command("gstats") & filters.group)
async def global_stats(client, message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return

    g = data["global"]
    escrowers_text = "\n".join([f"{name} = ₹{amt}" for name, amt in g["escrowers"].items()]) or "No deals yet"

    msg = (
        f"🌍 Global Escrow Stats\n\n"
        f"{escrowers_text}\n\n"
        f"🔹 Total Deals: {g['total_deals']}\n"
        f"💰 Total Volume: ₹{g['total_volume']}\n"
        f"💸 Total Fee Collected: ₹{g['total_fee']}\n"
    )
    await message.reply(msg)

# ================== Start Userbot ==================
print("✅ Userbot Started")
app.run()
