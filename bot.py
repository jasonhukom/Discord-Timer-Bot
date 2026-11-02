import logging
import os

import discord
from discord.ext import commands, tasks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("timer-bot")

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
INTERVAL_HOURS = float(os.getenv("INTERVAL_HOURS", "3"))
MESSAGE = os.getenv(
    "TIMER_MESSAGE",
    "Hello! This is your scheduled community reminder.",
)

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Set it in your .env file.")
if CHANNEL_ID <= 0:
    raise RuntimeError("CHANNEL_ID must be a valid Discord channel ID.")
if INTERVAL_HOURS <= 0:
    raise RuntimeError("INTERVAL_HOURS must be greater than zero.")


class TimerBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        self.send_timer.change_interval(hours=INTERVAL_HOURS)
        self.send_timer.start()

    async def on_ready(self) -> None:
        logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)

    @tasks.loop(hours=3)
    async def send_timer(self) -> None:
        try:
            channel = self.get_channel(CHANNEL_ID)
            if channel is None:
                channel = await self.fetch_channel(CHANNEL_ID)

            if not hasattr(channel, "send"):
                logger.error("Configured channel does not support messages.")
                return

            await channel.send(MESSAGE)
            logger.info("Sent scheduled message to channel %s", CHANNEL_ID)
        except discord.Forbidden:
            logger.exception(
                "Discord denied access. Check View Channel and Send Messages permissions."
            )
        except discord.NotFound:
            logger.exception("Channel %s was not found.", CHANNEL_ID)
        except discord.HTTPException:
            logger.exception("Discord API error while sending the reminder.")

    @send_timer.before_loop
    async def before_send_timer(self) -> None:
        await self.wait_until_ready()


if __name__ == "__main__":
    TimerBot().run(TOKEN, log_handler=None)
