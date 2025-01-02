import os
from pyrogram import filters
from BrandrdXMusic import app
import requests


def upload_file(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload", "json": "true"}
    files = {"fileToUpload": open(file_path, "rb")}
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        return True, response.text.strip()
    else:
        return False, f"Error: {response.status_code} - {response.text}"


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Please reply to a media file to upload it to Telegraph."
        )

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    if file_size > 200 * 1024 * 1024:
        return await message.reply_text("Please provide a media file under 200MB.")

    try:
        text = await message.reply("Processing...")

        async def progress(current, total):
            try:
                await text.edit_text(f"📥 Downloading... {current * 100 / total:.1f}%")
            except Exception:
                pass

        try:
            local_path = await media.download(progress=progress)
            await text.edit_text("📤 Uploading to Telegraph...")

            success, upload_path = upload_file(local_path)

            if success:
                await text.edit_text(f"🌐 Uploaded successfully: {upload_path}")
            else:
                await text.edit_text(
                    f"An error occurred while uploading your file:\n{upload_path}"
                )

            try:
                os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            await text.edit_text(f"❌ File upload failed\n\n<i>Reason: {e}</i>")
            try:
                os.remove(local_path)
            except Exception:
                pass
            return
    except Exception:
        pass


__HELP__ = """
**Telegraph Upload Bot Commands**

Use these commands to upload media to Telegraph:

- `/tgm`: Upload replied media to Telegraph.
- `/tgt`: Same as `/tgm`.
- `/telegraph`: Same as `/tgm`.
- `/tl`: Same as `/tgm`.

**Example:**
- Reply to a photo or video with `/tgm` to upload it.

**Note:**
You must reply to a media file for the upload to work.
"""

__MODULE__ = "Telegraph"

