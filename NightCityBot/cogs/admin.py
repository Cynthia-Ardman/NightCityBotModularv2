import os
import discord
from discord.ext import commands
from typing import Optional, Union
from dotenv import load_dotenv
from NightCityBot.utils.permissions import is_fixer
from NightCityBot.utils.helpers import load_json_file, save_json_file

load_dotenv()


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_channel_id = int(os.getenv('ADMIN_CHANNEL_ID', '0'))
        self.log_channel_id = int(os.getenv('LOG_CHANNEL_ID', '0'))
        self.guild_id = int(os.getenv('GUILD_ID', '0'))

    @commands.command()
    @is_fixer()
    async def ping(self, ctx):
        """Get the bot's current latency."""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! ({latency}ms)")

    @commands.command()
    @is_fixer()
    async def post(self, ctx, destination: str, *, message: Optional[str] = None):
        """Post a message to a specified channel."""
        try:
            # Get the target channel
            channel = await commands.TextChannelConverter().convert(ctx, destination)

            if not channel:
                await ctx.send("❌ Could not find the specified channel.")
                return

            # Handle attachments
            files = [await a.to_file() for a in ctx.message.attachments]

            # Send the message
            await channel.send(content=message, files=files)
            await ctx.send("✅ Message posted successfully.")

        except commands.ChannelNotFound:
            await ctx.send("❌ Channel not found.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to post in that channel.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.command()
    @is_fixer()
    async def status(self, ctx):
        """Check the bot's status and configurations."""
        embed = discord.Embed(title="Bot Status", color=discord.Color.blue())

        # Add basic info
        embed.add_field(
            name="Basic Info",
            value=f"Latency: {round(self.bot.latency * 1000)}ms\n"
                  f"Guilds: {len(self.bot.guilds)}\n"
                  f"Commands: {len(self.bot.commands)}",
            inline=False
        )

        # Add channel configurations
        embed.add_field(
            name="Channels",
            value=f"Admin: <#{self.admin_channel_id}>\n"
                  f"Logs: <#{self.log_channel_id}>",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    @is_fixer()
    async def cleanup(self, ctx, limit: Optional[int] = 100):
        """Clean up bot messages and commands in the current channel."""

        def is_bot_or_command(message):
            return message.author == self.bot.user or \
                message.content.startswith(self.bot.command_prefix)

        try:
            deleted = await ctx.channel.purge(
                limit=limit,
                check=is_bot_or_command,
                before=ctx.message
            )
            await ctx.send(
                f"✅ Cleaned up {len(deleted)} messages.",
                delete_after=5
            )
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to delete messages.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")