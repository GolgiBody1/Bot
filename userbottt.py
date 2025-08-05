import re, random, json, asyncio
from pyrogram import Client, filters

# ==== CONFIG ====
API_ID = 26014459
API_HASH = "34b8791089c72367a5088f96d925f989"
STRING_SESSION = "BQGM8vsAJVppG5SfjCvycz5l9o_UIsYpj3bvjYYF7qxZijHTM8_7mx8HlI2NVksjHXC3o31_QhFdq3VQGp510kRTE8CP0lYNSxQoM7A00-Wa56JNH1R2cNWTDuUGTYXqbif1B4z96_vPRJvPysL-R-6YMO7BDrI39Poyxv-IieogpMorJKUiQEgn1DjbeQTQNkpbJNwa2l-sbXumBfw5zwMCCZo4-iW_cNULOJLR_hw9-cRC64tMvegiJUUxmpweOThIJdz4ElEl7_qWV1HJSuTkPHyO_RaAIem-GwqQEi5RUlfpKXkCcOZYkPzZpMyrymLzcD0c-cGjPY7lqvFatJnNxF__VwAAAAGx20OoAA"
LOG_CHANNEL_ID = -1002330347621
DATA_FILE = "data.json"

# ==== DATA LOAD/SAVE ====
try:
    data = json.load(open(DATA_FILE))
except FileNotFoundError:
    data = {"groups": {}, "global": {"total_deals": 0, "total_volume": 0, "total_fee": 0.0, "escrowers": {}}}

save = lambda: json.dump(data, open(DATA_FILE, "w"))

def init(gid): data["groups"].setdefault(gid, {"deals": {}, "total_deals":0,"total_volume":0,"total_fee":0,"escrowers":{}})

async def autodel(m, t=15): await asyncio.sleep(t); 
try: await m.delete()
except: pass

app = Client("escrow_userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# ==== COMMANDS ====
@app.on_message(filters.command(["start","stats","gstats","add","complete"], ["/","!"]))
async def all_cmds(c, m):
    gid = str(m.chat.id)
    cmd = m.command[0]
    init(gid)

    if cmd == "start":
        msg = "✨ **Escrow Userbot**\n\n`/add` Add deal (reply)\n`/complete` Complete deal\n`/stats` Group stats\n`/gstats` Global stats"
        r = await m.reply(msg)

    elif cmd == "stats":
        g = data["groups"][gid]; 
        stats = "\n".join([f"{k}=₹{v}" for k,v in g["escrowers"].items()]) or "No deals yet"
        r = await m.reply(f"📊 **Group Stats**\n\n{stats}\n\nDeals: {g['total_deals']}\nVolume: ₹{g['total_volume']}\nFee: ₹{g['total_fee']}")

    elif cmd == "gstats":
        g = data["global"]
        stats = "\n".join([f"{k}=₹{v}" for k,v in g["escrowers"].items()]) or "No deals yet"
        r = await m.reply(f"🌍 **Global Stats**\n\n{stats}\n\nDeals: {g['total_deals']}\nVolume: ₹{g['total_volume']}\nFee: ₹{g['total_fee']}")

    elif cmd == "add":
        if not m.reply_to_message: return await m.reply("❌ Reply to DEAL INFO!")
        txt = m.reply_to_message.text or ""
        buyer = re.search(r"BUYER\s*:\s*(@\w+)",txt,re.I)
        seller = re.search(r"SELLER\s*:\s*(@\w+)",txt,re.I)
        amt = re.search(r"DEAL AMOUNT\s*:\s*₹?\s*([\d.]+)",txt,re.I)
        if not amt: return await m.reply("❌ Amount not found!")
        amt=float(amt.group(1)); r_id=str(m.reply_to_message.id); g=data["groups"][gid]
        if r_id not in g["deals"]:
            tid=f"TID{random.randint(100000,999999)}"; fee=round(amt*0.02,2); rel=amt-fee
            g["deals"][r_id]={"trade_id":tid,"release":rel,"done":False}
        else: tid=g["deals"][r_id]["trade_id"]; rel=g["deals"][r_id]["release"]; fee=amt-rel
        esc=m.from_user.username and f"@{m.from_user.username}" or m.from_user.first_name
        g["total_deals"]+=1; g["total_volume"]+=amt; g["total_fee"]+=fee
        data["global"]["total_deals"]+=1; data["global"]["total_volume"]+=amt; data["global"]["total_fee"]+=fee
        g["escrowers"][esc]=g["escrowers"].get(esc,0)+amt
        data["global"]["escrowers"][esc]=data["global"]["escrowers"].get(esc,0)+amt
        save()
        msg=f"✅ **Amount Received**\n──────────────\n👤Buyer: {buyer and buyer.group(1)}\n👤Seller: {seller and seller.group(1)}\n💰Amt: ₹{amt}\n💸Release: ₹{rel}\n⚖️Fee: ₹{fee}\n🆔TradeID: #{tid}\n🛡️Escrowed by {esc}"
        r=await m.reply_to_message.reply_text(msg)

    elif cmd == "complete":
        if not m.reply_to_message: return await m.reply("❌ Reply to DEAL INFO!")
        r_id=str(m.reply_to_message.id); g=data["groups"][gid]; deal=g["deals"].get(r_id)
        if not deal: return await m.reply("❌ Deal not added!")
        if deal["done"]: return await m.reply("❌ Already completed!")
        deal["done"]=True; save()
        txt=m.reply_to_message.text or ""
        buyer=re.search(r"BUYER\s*:\s*(@\w+)",txt,re.I); seller=re.search(r"SELLER\s*:\s*(@\w+)",txt,re.I)
        esc=m.from_user.username and f"@{m.from_user.username}" or m.from_user.first_name
        msg=f"✅ **Deal Completed**\n──────────────\n👤Buyer: {buyer and buyer.group(1)}\n👤Seller: {seller and seller.group(1)}\n💸Released: ₹{deal['release']}\n🆔TradeID: #{deal['trade_id']}\n🛡️Escrowed by {esc}"
        r=await m.reply_to_message.reply_text(msg)
        await c.send_message(LOG_CHANNEL_ID,f"📜 **Deal Completed(Log)**\n{msg}\nGroup: {m.chat.title} ({gid})")

    # Auto delete reply and command
    asyncio.create_task(autodel(r))
    await m.delete()

print("✅ Ultra-Fast Escrow Userbot Started...")
app.run()
