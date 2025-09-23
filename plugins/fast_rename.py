from pyrogram import Client, filters

# Temporary storage for user thumbnails
user_thumbs = {}  # {user_id: file_id}

# ---------- SAVE THUMBNAIL ----------
@Client.on_message(filters.photo & filters.private)
async def save_thumbnail(client, message):
    user_id = message.from_user.id
    file_id = message.photo.file_id
    user_thumbs[user_id] = file_id
    await message.reply_text("✅ Thumbnail saved! Ab apni movie bhejo.")

# ---------- VIDEO RENAME & FAST THUMB ----------
@Client.on_message(filters.video & filters.private)
async def fast_rename_video(client, message):
    user_id = message.from_user.id
    thumb_id = user_thumbs.get(user_id)

    if thumb_id:
        await message.reply_video(
            video=message.video.file_id,
            thumb=thumb_id,
            caption=f"🎬 {message.video.file_name} renamed!"
        )
        user_thumbs.pop(user_id, None)
    else:
        await message.reply_text("⚠️ Pehle thumbnail bhejo, phir video send karo.")
