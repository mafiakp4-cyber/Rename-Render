import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess

# Queue for processing videos
video_queue = asyncio.Queue()
user_thumbs = {}  # {user_id: file_id}

# ---------- SAVE THUMBNAIL ----------
@Client.on_message(filters.photo & filters.private)
async def save_thumbnail(client, message: Message):
    user_id = message.from_user.id
    file_id = message.photo.file_id
    user_thumbs[user_id] = file_id
    await message.reply_text("✅ Thumbnail saved! Ab apni movie bhejo.")

# ---------- ADD VIDEO TO QUEUE ----------
@Client.on_message(filters.video & filters.private)
async def enqueue_video(client, message: Message):
    await video_queue.put(message)
    await message.reply_text("🎬 Video queued for fast rename...")

# ---------- WORKER PROCESS ----------
async def video_worker(client: Client):
    while True:
        message = await video_queue.get()
        user_id = message.from_user.id
        thumb_id = user_thumbs.get(user_id)

        # Optional: remux video without re-encoding for speed
        video_path = f"temp_{user_id}.mp4"
        await message.download(file_name=video_path)
        remuxed_path = f"remux_{user_id}.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-c", "copy", remuxed_path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Send video with saved thumbnail
        await client.send_video(
            chat_id=message.chat.id,
            video=remuxed_path,
            thumb=thumb_id,
            caption=f"🎬 {message.video.file_name} renamed!"
        )

        # Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(remuxed_path):
            os.remove(remuxed_path)
        user_thumbs.pop(user_id, None)
        video_queue.task_done()
