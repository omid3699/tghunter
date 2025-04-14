import asyncio
import re
import uuid

from telethon import Button

from bot.config import DOWNLOAD_DIR
from bot.logger import logger

YTDL_DIR = DOWNLOAD_DIR / "youtube"
YTDL_DIR.mkdir(parents=True, exist_ok=True)

video_regex = re.compile(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+")
user_choices = {}  # For tracking who chose what


async def handle_youtube(event):
    args = event.raw_text.strip().split(maxsplit=1)
    if len(args) != 2:
        await event.reply("⚠️ Usage: `/yt <url>`", parse_mode="markdown")
        return

    url = args[1].strip()
    if not video_regex.match(url):
        await event.reply("❌ Invalid YouTube URL.", parse_mode="markdown")
        return

    choice_id = uuid.uuid4().hex[:6]
    user_choices[choice_id] = {"url": url, "chat_id": event.chat_id}

    await event.reply(
        f"🎬 What do you want to download?\n\nURL: `{url}`",
        buttons=[
            [
                Button.inline("🎵 Audio Only", f"yt_{choice_id}_audio".encode()),
                Button.inline("🎥 Video", f"yt_{choice_id}_video".encode()),
            ]
        ],
        parse_mode="markdown",
    )


async def download_youtube(url: str, format: str, event):
    folder_name = uuid.uuid4().hex[:8]
    download_path = YTDL_DIR / folder_name
    download_path.mkdir(parents=True, exist_ok=True)

    ytdl_format = "bestaudio" if format == "audio" else "bestvideo*+bestaudio/best"
    cmd = [
        "yt-dlp",
        "-f",
        ytdl_format,
        "--embed-metadata",
        "--write-thumbnail",
        "--write-info-json",
        "--merge-output-format",
        "mp4" if format == "video" else "m4a",
        "-P",
        str(download_path),
        url,
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    async for line in proc.stdout:
        decoded = line.decode().strip()
        if "Downloading" in decoded or "%" in decoded:
            await event.reply(f"⏬ {decoded}")

    await proc.wait()
    await event.reply(f"✅ Download complete! Saved in `youtube/{folder_name}`")
    logger.info(f"[youtube] Downloaded to {download_path}")
