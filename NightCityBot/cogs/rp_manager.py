import os
import discord
from discord.ext import commands
from typing import Optional, Dict, Union
from dotenv import load_dotenv
from NightCityBot.utils.permissions import is_fixer
from NightCityBot.utils.helpers import load_json_file, save_json_file

load_dotenv()


class RPManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rp_data_file = os.getenv('RP_DATA_FILE', 'data/rp_data.json')
        self.rp_channel_id = int(os.getenv('RP_CHANNEL_ID', '0'))
        self.active_sessions: Dict[str, dict] = {}
        self.bot.loop.create_task(self.load_rp_data())

    async def load_rp_data(self):
        """Load RP session data from file on startup."""
        self.active_sessions = await load_json_file(self.rp_data_file, default={})

    async def save_rp_data(self):
        """Save current RP session data to file."""
        await save_json_file(self.rp_data_file, self.active_sessions)

    @commands.group(invoke_without_command=True)
    async def rp(self, ctx):
        """RP management commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Available commands: `start`, `end`, `join`, `leave`, `list`")

    @rp.command()
    async def start(
            self,
            ctx,
            name: str,
            category: Optional[discord.CategoryChannel] = None,
            *players: discord.Member
    ):
        """Start a new RP session."""
        if name in self.active_sessions:
            await ctx.send("❌ An RP session with that name already exists.")
            return

        # Create new session
        session = {
            "name": name,
            "dm": ctx.author.id,
            "players": [p.id for p in players] if players else [],
            "category_id": category.id if category else None,
            "channels": []
        }

        self.active_sessions[name] = session
        await self.save_rp_data()

        players_mention = " ".join(p.mention for p in players) if players else "No players yet"
        await ctx.send(
            f"✅ Started RP session '{name}'\n"
            f"**DM:** {ctx.author.mention}\n"
            f"**Players:** {players_mention}"
        )

    @rp.command()
    async def end(self, ctx, name: str):
        """End an RP session."""
        if name not in self.active_sessions:
            await ctx.send("❌ No RP session with that name exists.")
            return

        session = self.active_sessions[name]
        if ctx.author.id != session["dm"] and not await is_fixer().predicate(ctx):
            await ctx.send("❌ Only the session DM or a Fixer can end the session.")
            return

        del self.active_sessions[name]
        await self.save_rp_data()
        await ctx.send(f"✅ Ended RP session '{name}'")

    @rp.command()
    async def join(self, ctx, name: str):
        """Join an RP session."""
        if name not in self.active_sessions:
            await ctx.send("❌ No RP session with that name exists.")
            return

        session = self.active_sessions[name]
        if ctx.author.id in session["players"]:
            await ctx.send("❌ You're already in this session.")
            return

        session["players"].append(ctx.author.id)
        await self.save_rp_data()
        await ctx.send(f"✅ {ctx.author.mention} joined RP session '{name}'")

    @rp.command()
    async def leave(self, ctx, name: str):
        """Leave an RP session."""
        if name not in self.active_sessions:
            await ctx.send("❌ No RP session with that name exists.")
            return

        session = self.active_sessions[name]
        if ctx.author.id not in session["players"]:
            await ctx.send("❌ You're not in this session.")
            return

        session["players"].remove(ctx.author.id)
        await self.save_rp_data()
        await ctx.send(f"✅ {ctx.author.mention} left RP session '{name}'")

    @rp.command(name="list")
    async def list_sessions(self, ctx):
        """List all active RP sessions."""
        if not self.active_sessions:
            await ctx.send("No active RP sessions.")
            return

        for name, session in self.active_sessions.items():
            dm = ctx.guild.get_member(session["dm"])
            players = [ctx.guild.get_member(pid) for pid in session["players"]]
            players = [p for p in players if p]  # Filter out None values

            players_text = "\n".join(f"- {p.display_name}" for p in players) or "No players"

            await ctx.send(
                f"**{name}**\n"
                f"DM: {dm.display_name if dm else 'Unknown'}\n"
                f"Players:\n{players_text}"
            )