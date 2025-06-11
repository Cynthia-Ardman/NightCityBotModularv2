import os
from pathlib import Path
from datetime import datetime
import discord
from discord.ext import commands
from NightCityBot.utils.helpers import load_json_file, save_json_file


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.open_log_file = os.getenv('OPEN_LOG_FILE', 'data/business_open_log.json')
        self.allowed_channel_id = int(os.getenv('BUSINESS_ACTIVITY_CHANNEL_ID', '0'))

    @commands.command()
    @commands.has_permissions(send_messages=True)
    async def open_shop(self, ctx):
        """Log a business opening (Sundays only, max 4 per month)."""
        if ctx.channel.id != self.allowed_channel_id:
            await ctx.send("❌ You can only log business openings in the designated business activity channel.")
            return

        now = datetime.utcnow()
        if now.weekday() != 6:  # 6 = Sunday
            await ctx.send("❌ Business openings can only be logged on Sundays.")
            return

        data = await load_json_file(self.open_log_file, default={})
        user_id = str(ctx.author.id)
        now_str = now.isoformat()

        all_opens = data.get(user_id, [])
        this_month_opens = [
            datetime.fromisoformat(ts)
            for ts in all_opens
            if datetime.fromisoformat(ts).month == now.month and
               datetime.fromisoformat(ts).year == now.year
        ]

        # Check if already opened today
        opened_today = any(
            ts.date() == now.date()
            for ts in this_month_opens
        )

        if opened_today:
            await ctx.send("❌ You've already logged a business opening today.")
            return

        if len(this_month_opens) >= 4:
            await ctx.send("❌ You've already used all 4 business posts for this month.")
            return

        all_opens.append(now_str)
        data[user_id] = all_opens
        await save_json_file(self.open_log_file, data)

        await ctx.send(f"✅ Business opening logged! ({len(this_month_opens) + 1}/4 this month)")