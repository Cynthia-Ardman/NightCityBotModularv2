import traceback
import discord
from discord.ext import commands
from typing import Optional
from NightCityBot.utils.config import config


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handle all command errors."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Unknown command.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("❌ Permission denied.")
        else:
            # Log the full error
            error_trace = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            print(f"Error in {ctx.command}:\n{error_trace}")

            # Send a user-friendly message
            await ctx.send(f"⚠️ An error occurred: {str(error)}")

            # Log to admin channel if available
            admin_channel = self.bot.get_channel(config.channels['admin'])
            if admin_channel:
                embed = discord.Embed(
                    title="❌ Command Error",
                    description=f"Error in command: `{ctx.command}`",
                    color=discord.Color.red()
                )
                embed.add_field(name="User", value=f"{ctx.author} ({ctx.author.id})")
                embed.add_field(name="Channel", value=f"{ctx.channel} ({ctx.channel.id})")
                embed.add_field(name="Error", value=f"```py\n{str(error)}```", inline=False)

                await admin_channel.send(embed=embed)