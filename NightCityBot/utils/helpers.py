from pathlib import Path
from typing import Any, Optional, Union, Dict
import discord
from discord.ext import commands
from NightCityBot.utils.config import config
from NightCityBot.utils.db import db


async def log_audit(
        user: Union[discord.Member, discord.User],
        action_desc: str,
        *,
        error: bool = False
) -> None:
    """Log an action to the audit channel."""
    audit_channel = user.guild.get_channel(config.channels['admin'])
    if not isinstance(audit_channel, discord.TextChannel):
        print(f"[AUDIT] Skipped: Channel {config.channels['admin']} is not a TextChannel")
        return

    embed = discord.Embed(
        title="📝 Audit Log",
        color=discord.Color.red() if error else discord.Color.blue()
    )
    embed.add_field(name="User", value=f"{user} ({user.id})", inline=False)
    embed.add_field(name="Action", value=action_desc, inline=False)

    await audit_channel.send(embed=embed)
    print(f"[AUDIT] {user}: {action_desc}")


def build_channel_name(usernames: list[tuple[str, int]], max_length: int = 100) -> str:
    """Build a Discord-friendly channel name."""
    import re
    full_name = "text-rp-" + "-".join(f"{name}-{uid}" for name, uid in usernames)
    if len(full_name) <= max_length:
        return re.sub(r"[^a-z0-9\-]", "", full_name.lower())

    simple_name = "text-rp-" + "-".join(name for name, _ in usernames)
    if len(simple_name) > max_length:
        simple_name = simple_name[:max_length]

    return re.sub(r"[^a-z0-9\-]", "", simple_name.lower())