import discord
from discord.ext import commands
from NightCityBot.utils.helpers import log_audit

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Global error handler for all commands."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Unknown command.")
            await log_audit(ctx.author, f"❌ Unknown command: {ctx.message.content}")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ Permission denied.")
            await log_audit(ctx.author, f"❌ Permission denied: {ctx.message.content}")
        else:
            await ctx.send(f"⚠️ Error: {str(error)}")
            await log_audit(ctx.author, f"⚠️ Error: {ctx.message.content} → {str(error)}")