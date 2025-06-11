import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Import cogs
from NightCityBot.cogs.dm_handling import DMHandler
from NightCityBot.cogs.economy import Economy
from NightCityBot.cogs.rp_manager import RPManager
from NightCityBot.cogs.roll_system import RollSystem
from NightCityBot.cogs.admin import Admin
from NightCityBot.cogs.test_suite import TestSuite
from NightCityBot.cogs.trauma_team import TraumaTeam

# Load environment variables
load_dotenv()

class NightCityBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        intents.dm_messages = True

        super().__init__(
            command_prefix=os.getenv('BOT_PREFIX', '!'),
            help_command=None,
            intents=intents
        )

    async def setup_hook(self):
        # Load all cogs
        await self.add_cog(DMHandler(self))
        await self.add_cog(Economy(self))
        await self.add_cog(RPManager(self))
        await self.add_cog(RollSystem(self))
        await self.add_cog(Admin(self))
        await self.add_cog(TestSuite(self))
        await self.add_cog(TraumaTeam(self))

    async def on_ready(self):
        print(f"✅ {self.user.name} is running!")

# Flask keep-alive server
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive Version 1.2!"

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

def main():
    bot = NightCityBot()
    keep_alive()
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main()