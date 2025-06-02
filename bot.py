from utils.time_formatter import get_progress_bar
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
import random
import os

from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, SESSION_NAME

START_IMAGES = [
    "https://telegra.ph/file/4f93f678a111974b13e44.jpg",
    "https://telegra.ph/file/1b2b3c4d5e6f7g8h9i0j1.jpg"
]

PING_IMAGES = [
    "https://telegra.ph/file/63620a01a0ef3e34d99cf.jpg",
    "https://telegra.ph/file/badcafeabc123def456gh.jpg"
]

bot = Client("LoveRjXMusic", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
vc = PyTgCalls(user)

admins = [OWNER_ID]

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_photo(
        photo=random.choice(START_IMAGES),
        caption = """🎧 **LoveRJ on Streaming!**
🎵 Enjoy the music!
"""
caption = "Powered by LoveRjXMusic"
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Play", callback_data="play")],
            [InlineKeyboardButton("⏸ Pause", callback_data="pause"),
             InlineKeyboardButton("▶️ Resume", callback_data="resume")],
            [InlineKeyboardButton("⏭ Skip", callback_data="skip"),
             InlineKeyboardButton("🔄 Restart", callback_data="restart")],
            [InlineKeyboardButton("❌ Close", callback_data="close")]
        ])
    )

@bot.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply_photo(
        photo=random.choice(PING_IMAGES),
        caption="🏓 **Pong! Bot is alive.**"
    )

@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast it.")
    for dialog in await client.get_dialogs():
        try:
            await client.send_message(dialog.chat.id, message.reply_to_message.text)
        except:
            pass
    await message.reply("✅ Broadcast completed.")

@bot.on_callback_query()
async def callbacks(_, query):
    user_id = query.from_user.id
    if user_id not in admins:
        return await query.answer("Only admins can control the music.", show_alert=True)

    chat_id = query.message.chat.id

    if query.data == "pause":
        await vc.pause_stream(chat_id)
        await query.answer("⏸ Paused")
    elif query.data == "resume":
        await vc.resume_stream(chat_id)
        await query.answer("▶️ Resumed")
    elif query.data == "skip":
        await vc.leave_group_call(chat_id)
        await query.answer("⏭ Skipped")
    elif query.data == "restart":
        await vc.leave_group_call(chat_id)
        await vc.join_group_call(chat_id, InputStream(HighQualityAudio()))
        await query.answer("🔄 Restarted")
    elif query.data == "play":
        await vc.join_group_call(chat_id, InputStream(HighQualityAudio()))
        # Simulate song metadata
        title = "Test Song Title"
        duration = "03:45"
        thumb = "https://telegra.ph/file/9f2443e4d0b8efb7b70e9.jpg"  # Album art
        await query.message.reply_photo(
            photo=thumb,
            caption=f"🎵 **Now Playing:** `{title}`
"
                    f"⏱ **Duration:** `{duration}`
"
                    f"🙋‍♂️ **Requested by:** [{query.from_user.first_name}](tg://user?id={user_id})
"
                    f"💠 Powered by @LoveRjXMusic",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                 InlineKeyboardButton("▶️ Resume", callback_data="resume")],
                [InlineKeyboardButton("⏭ Skip", callback_data="skip"),
                 InlineKeyboardButton("🔄 Restart", callback_data="restart")],
                [InlineKeyboardButton("❌ Close", callback_data="close")]
            ])
        )
        await query.answer("▶️ Playing")

bot.start()
user.start()
vc.start()
print("LoveRjXMusic is running...")
idle()
# Example values (replace with real-time values)
current = 47
total = 225
progress = get_progress_bar(current, total)

caption = f"""
🎧 Title: Ram Siya Ram
📊 {progress}
🎙️ Played by: @username
"""
