from pyrogram import Client, filters
import aiohttp
import io

@Client.on_message(filters.command("leech") & filters.private)
async def leech(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a file URL. Example:\n/leech https://example.com/file.zip")
        return

    url = message.command[1]
    await message.reply_text("Downloading file... ⏳")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await message.reply_text("Failed to download file.")
                return
            data = await resp.read()

    file_like = io.BytesIO(data)
    file_like.name = url.split("/")[-1]  # Extract file name from URL

    await message.reply_document(file_like, caption="Here is your file! ✅")
