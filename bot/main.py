from telethon import TelegramClient, events

from bot.commands.aria2_handler import download_with_aria2
from bot.commands.clone_handler import handle_clone
from bot.commands.git_handler import handle_git
from bot.commands.pip_handler import handle_pip
from bot.commands.youtube_handler import download_youtube, handle_youtube, user_choices
from bot.config import API_HASH, API_ID, AUTHORIZED_USER_ID, BOT_TOKEN, DOWNLOAD_DIR
from bot.handlers.media import handle_media
from bot.logger import logger

# Ensure download dir exists
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Setup session

client = TelegramClient("tghunter", API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    if event.sender_id != AUTHORIZED_USER_ID:
        await event.respond("❌ Access denied.")
        logger.warning(f"Unauthorized access attempt by {event.sender_id}")
        return
    await event.respond("👋 Hello! TGHunter is ready.")
    logger.info("Authorized user started bot.")


@client.on(events.NewMessage())
async def all_messages(event):
    if event.sender_id != AUTHORIZED_USER_ID:
        return
    logger.debug(f"Received message: {event.raw_text}")


async def main():
    logger.info("Starting TGHunter bot...")
    await client.run_until_disconnected()


@client.on(events.NewMessage(incoming=True, forwards=True))
async def forwarded_handler(event):
    await handle_media(event)


@client.on(events.NewMessage(pattern=r"^/git"))
async def git_command(event):
    if event.sender_id != AUTHORIZED_USER_ID:
        return
    await handle_git(event)


@client.on(events.NewMessage(pattern=r"^/pip"))
async def pip_command(event):
    if event.sender_id != AUTHORIZED_USER_ID:
        return
    await handle_pip(event)


@client.on(events.NewMessage(pattern=r"^/yt"))
async def yt_command(event):
    if event.sender_id != AUTHORIZED_USER_ID:
        return
    await handle_youtube(event)


@client.on(events.CallbackQuery())
async def callback_handler(event):
    data = event.data.decode()

    if not data.startswith("yt_"):
        return

    _, choice_id, mode = data.split("_")

    choice = user_choices.get(choice_id)

    if not choice:
        await event.answer("❌ Session expired", alert=True)
        return

    await event.edit(f"⏳ Downloading as {mode.upper()}...")
    await download_youtube(choice["url"], mode, event)
    del user_choices[choice_id]


@client.on(events.NewMessage(pattern=r"^/clone"))
async def clone_command(event):
    if event.sender_id != AUTHORIZED_USER_ID:
        return
    await handle_clone(event)


@client.on(events.NewMessage(pattern="/download"))
async def download_file(event):
    """Handle file downloads from direct URLs."""
    try:
        url = event.text.split(" ", 1)[1].strip()  # Extract URL from the message
    except IndexError:
        await event.reply("Please provide a valid URL.")
        return

    await event.reply(f"Starting download from {url}...")

    # Start the download using Aria2
    download_successful = await download_with_aria2(url)

    if download_successful:
        await event.reply(f"Download of {url} completed successfully!")
    else:
        await event.reply(f"Download of {url} failed.")


if __name__ == "__main__":
    try:
        logger.info("tghunter starting....")
        client.run_until_disconnected()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
