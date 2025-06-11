import os
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import aiohttp
import json
from datetime import datetime, timezone
import random
from dotenv import load_dotenv
from NightCityBot.utils.permissions import is_fixer
from NightCityBot.utils.helpers import load_json_file, save_json_file

# Load environment variables
load_dotenv()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currency_name = os.getenv('CURRENCY_NAME', 'eb')
        self.starting_balance = int(os.getenv('STARTING_BALANCE', '1000'))
        self.unbelievaboat_token = os.getenv('UNBELIEVABOAT_TOKEN')
        self.unbelievaboat_api = os.getenv('UNBELIEVABOAT_API', 'https://unbelievaboat.com/api')
        self.daily_min = int(os.getenv('DAILY_MIN', '100'))
        self.daily_max = int(os.getenv('DAILY_MAX', '1000'))
        self.ledger_file = os.getenv('LEDGER_FILE', 'data/ledger.json')
        self.bank_data = {}
        self.bot.loop.create_task(self.load_bank_data())

    async def load_bank_data(self):
        """Load bank data from file on startup."""
        self.bank_data = await load_json_file(self.ledger_file, default={})

    async def save_bank_data(self):
        """Save current bank data to file."""
        await save_json_file(self.ledger_file, self.bank_data)

    async def get_balance(self, user_id: str) -> int:
        """Get a user's current balance."""
        return self.bank_data.get(str(user_id), self.starting_balance)

    async def set_balance(self, user_id: str, amount: int):
        """Set a user's balance and save to file."""
        self.bank_data[str(user_id)] = amount
        await self.save_bank_data()

    @commands.hybrid_command()
    async def balance(self, ctx, user: Optional[discord.Member] = None):
        """Check your current balance or another user's balance."""
        target = user or ctx.author
        balance = await self.get_balance(str(target.id))

        if target == ctx.author:
            await ctx.send(f"You have {balance:,} {self.currency_name}")
        else:
            await ctx.send(f"{target.display_name} has {balance:,} {self.currency_name}")

    @commands.hybrid_command()
    @is_fixer()
    async def give(self, ctx, user: discord.Member, amount: int):
        """Give currency to a user (Fixer only)."""
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return

        current = await self.get_balance(str(user.id))
        await self.set_balance(str(user.id), current + amount)

        await ctx.send(
            f"✅ Gave {amount:,} {self.currency_name} to {user.display_name}. "
            f"They now have {current + amount:,} {self.currency_name}."
        )

    @commands.hybrid_command()
    @is_fixer()
    async def take(self, ctx, user: discord.Member, amount: int):
        """Remove currency from a user (Fixer only)."""
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return

        current = await self.get_balance(str(user.id))
        new_balance = max(0, current - amount)
        await self.set_balance(str(user.id), new_balance)

        actual_amount = current - new_balance
        await ctx.send(
            f"✅ Took {actual_amount:,} {self.currency_name} from {user.display_name}. "
            f"They now have {new_balance:,} {self.currency_name}."
        )

    @commands.hybrid_command()
    async def daily(self, ctx):
        """Claim your daily reward."""
        user_id = str(ctx.author.id)
        last_daily = self.bank_data.get(f"{user_id}_last_daily")

        now = datetime.now(timezone.utc)
        if last_daily:
            last_claim = datetime.fromisoformat(last_daily)
            if (now - last_claim).days < 1:
                time_left = datetime.fromtimestamp(last_claim.timestamp() + 86400, timezone.utc)
                await ctx.send(f"❌ You can claim again at <t:{int(time_left.timestamp())}:R>")
                return

        amount = random.randint(self.daily_min, self.daily_max)
        current = await self.get_balance(user_id)
        await self.set_balance(user_id, current + amount)
        self.bank_data[f"{user_id}_last_daily"] = now.isoformat()
        await self.save_bank_data()

        await ctx.send(
            f"✅ You received {amount:,} {self.currency_name}. "
            f"You now have {current + amount:,} {self.currency_name}."
        )
