import asyncio
import logging
import os

import discord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord-timer-action")

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
MESSAGE = os.getenv(
    "TIMER_MESSAGE",
    "Hello! This is your scheduled community reminder.",
)


async def main() -> None:
    if not TOKEN:
        raise RuntimeError("GitHub Actions secret DISCORD_TOKEN is not configured.")
    if CHANNEL_ID <= 0:
        raise RuntimeError("GitHub Actions secret CHANNEL_ID is missing or invalid.")

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready() -> None:
        try:
            channel = client.get_channel(CHANNEL_ID)
            if channel is None:
                channel = await client.fetch_channel(CHANNEL_ID)

            if not hasattr(channel, "send"):
                raise RuntimeError("The configured channel cannot receive messages.")

            await channel.send(MESSAGE)
            logger.info("Reminder sent to channel %s.", CHANNEL_ID)
        finally:
            await client.close()

    await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
