import discord
from discord.ext import commands
from flask import Flask
from dotenv import load_dotenv
from threading import Thread
import os

# Import cogs
from NightCityBot.cogs.dm_handling import DMHandler
from NightCityBot.cogs.economy import Economy
from NightCityBot.cogs.rp_manager import RPManager
from NightCityBot.cogs.roll_system import RollSystem
from NightCityBot.cogs.admin import Admin
from NightCityBot.cogs.test_suite import TestSuite
from NightCityBot.cogs.trauma_team import TraumaTeam
from NightCityBot.cogs.help import Help
from NightCityBot.cogs.shop import Shop
from NightCityBot.cogs.error_handler import ErrorHandler

# Import config
from NightCityBot.utils.config import config


class NightCityBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        intents.dm_messages = True

        super().__init__(
            command_prefix=config.prefix,
            help_command=None,
            intents=intents
        )

        self.config = config

    async def setup_hook(self):
        """Initialize bot and load cogs."""
        # Load core systems first
        await self.add_cog(ErrorHandler(self))
        await self.add_cog(Admin(self))

        # Load feature cogs
        await self.add_cog(DMHandler(self))
        await self.add_cog(Economy(self))
        await self.add_cog(RPManager(self))
        await self.add_cog(RollSystem(self))
        await self.add_cog(TraumaTeam(self))
        await self.add_cog(Shop(self))
        await self.add_cog(Help(self))

        # Load test suite last
        if os.getenv('ENVIRONMENT') == 'development':
            await self.add_cog(TestSuite(self))

    async def on_ready(self):
        """Called when the bot is ready."""
        print(f"✅ {self.user.name} is running!")
        print(f"Bot latency: {round(self.latency * 1000)}ms")
        print(f"Connected to {len(self.guilds)} guilds")


# Flask keep-alive server
app = Flask('')


@app.route('/')
def home():
    return "Bot is alive Version 1.2!"


def run_flask():
    app.run(host='0.0.0.0', port=5000)


def keep_alive():
    t = Thread(target=run_flask, daemon=True)  # Add daemon=True
    t.start()


def main():
    bot = NightCityBot()
    keep_alive()
    try:
        bot.run(config.token)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")


if __name__ == "__main__":
    main()