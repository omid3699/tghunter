from pathlib import Path

from bot.config import AUTHORIZED_USER_ID, DOWNLOAD_DIR
from bot.logger import logger


async def handle_media(event):
    if event.sender_id != AUTHORIZED_USER_ID:
        return

    msg = event.message
    media = msg.media

    if not media:
        return

    file_name = await msg.download_media(file=DOWNLOAD_DIR)
    if file_name:
        file_path = Path(file_name).resolve()
        logger.success(f"📥 Downloaded: {file_path.name}")
        await event.reply(f"✅ Downloaded: `{file_path.name}`", parse_mode="markdown")
    else:
        logger.error("Failed to download media.")
        await event.reply("❌ Failed to download file.")
