import asyncio
import shutil
import uuid
from urllib.parse import urlparse

from bot.config import DOWNLOAD_DIR
from bot.logger import logger

WEBSITES_DIR = DOWNLOAD_DIR / "websites"
WEBSITES_DIR.mkdir(parents=True, exist_ok=True)


async def handle_clone(event):
    args = event.raw_text.strip().split(maxsplit=1)
    if len(args) != 2:
        await event.reply("⚠️ Usage: `/clone <url>`", parse_mode="markdown")
        return

    url = args[1].strip()
    try:
        domain = urlparse(url).netloc or uuid.uuid4().hex[:6]
        folder = WEBSITES_DIR / domain
        if folder.exists():
            folder = folder.with_name(f"{folder.name}_{uuid.uuid4().hex[:4]}")
        folder.mkdir(parents=True)

        await event.reply(
            f"🌐 Cloning `{url}` into `{folder.name}`...\nThis might take a while.",
            parse_mode="markdown",
        )

        cmd = ["httrack", url, "-O", str(folder), "--quiet"]

        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )

        async for line in proc.stdout:
            decoded = line.decode().strip()
            if decoded:
                await event.reply(f"🔄 {decoded[:100]}")  # Shorten long logs

        await proc.wait()

        zip_path = shutil.make_archive(str(folder), "zip", folder)
        await event.reply(
            f"✅ Website cloned!\n📁 `{folder.name}`\n📦 Sending archive...",
            parse_mode="markdown",
        )
        await event.reply(file=zip_path)

        logger.info(f"[clone] Cloned site to {folder} and zipped.")
    except Exception as e:
        await event.reply(f"❌ Error cloning site:\n`{str(e)}`", parse_mode="markdown")
        logger.error(f"[clone] {e}")
