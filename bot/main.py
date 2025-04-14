import asyncio

from telethon import TelegramClient, events

from bot.config import API_HASH, API_ID, AUTHORIZED_USER_ID, BOT_TOKEN, DOWNLOAD_DIR
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


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
