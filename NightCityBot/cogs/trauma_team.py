import os
import discord
from discord.ext import commands
from typing import Optional, List
from dotenv import load_dotenv
from NightCityBot.utils.permissions import is_fixer
from NightCityBot.services.trauma_team import TraumaTeam as TraumaTeamService

load_dotenv()


class TraumaTeam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = TraumaTeamService()

    @commands.command()
    @is_fixer()
    async def collect_trauma(self, ctx, user: discord.Member):
        """Manually collect Trauma Team subscription"""
        log = [f"💊 Manual Trauma Team Subscription Processing for <@{user.id}>"]

        # Get trauma forum channel
        trauma_channel = self.bot.get_channel(self.service.trauma_forum_channel_id)
        if not isinstance(trauma_channel, discord.ForumChannel):
            await ctx.send("❌ Trauma Team forum channel not found.")
            return

        # Process payment
        await self.service.process_trauma_team_payment(user, trauma_channel, log=log)

        # Send log to context
        await ctx.send("\n".join(log))

    async def process_trauma_payment(self, member: discord.Member, *, log: Optional[List[str]] = None) -> None:
        """Process Trauma Team subscription payment (used by other cogs)."""
        trauma_channel = self.bot.get_channel(self.service.trauma_forum_channel_id)
        if isinstance(trauma_channel, discord.ForumChannel):
            await self.service.process_trauma_team_payment(member, trauma_channel, log=log)