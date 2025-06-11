import discord
from discord.ext import commands
from NightCityBot.utils.constants import ROLE_COSTS_BUSINESS

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def block_help(self, ctx):
        """Block default help command."""
        await ctx.send("❌ `!help` is disabled. Use `!helpme` or `!helpfixer` instead.")

    @commands.command(name="helpme")
    async def helpme(self, ctx):
        """Show help for regular users."""
        embed = discord.Embed(
            title="📘 NCRP Bot — Player Help",
            description="Basic commands for RP, rent, and rolling dice. Use `!helpfixer` if you're a Fixer.",
            color=discord.Color.teal()
        )

        embed.add_field(
            name="🎲 RP Tools",
            value=(
                "`!roll [XdY+Z]`\n"
                "→ Roll dice in any channel or DM.\n"
                "→ Netrunner Level 2 = +1, Level 3 = +2 bonus.\n"
                "→ Roll results in DMs are logged privately."
            ),
            inline=False
        )

        embed.add_field(
            name="💰 Rent & Cost of Living",
            value=(
                "Everyone pays a **$500/month** baseline fee for survival (food, water, etc).\n"
                "Even if you don't have a house or business — you're still eating Prepack.\n\n"
                "`!open_shop`\n"
                "→ Shop owners log up to 4 openings/month (Sundays only).\n"
                "→ Increases passive income if you're active."
            ),
            inline=False
        )

        # Calculate example income for Tier 2
        tier2_rent = ROLE_COSTS_BUSINESS["Business Tier 2"]
        tier2_example = int(tier2_rent * 0.6)  # 60% for 3 opens

        embed.add_field(
            name="🏪 Passive Income Breakdown",
            value=(
                "**Tier 0 (Free Stall):**\n"
                " • 1 open = $150\n"
                " • 2 opens = $250\n"
                " • 3 opens = $350\n"
                " • 4 opens = $500\n\n"

                "**Tiers 1–3 (Paid Roles):**\n"
                " • 1 open = 25% of rent\n"
                " • 2 opens = 40%\n"
                " • 3 opens = 60%\n"
                " • 4 opens = 80%\n\n"

                f"_Example: Tier 2 shop with 3 opens earns ${tier2_example} passive._"
            ),
            inline=False
        )

        embed.set_footer(text="Use !roll, pay your rent, stay alive.")
        await ctx.send(embed=embed)

    @commands.command(name="helpfixer")
    @commands.has_role("Fixer")
    async def helpfixer(self, ctx):
        """Show help for Fixers."""
        embed = discord.Embed(
            title="🛠️ NCRP Bot — Fixer & Admin Help",
            description="Advanced commands for messaging, RP management, rent, and testing.",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="📨 Anonymous Messaging",
            value=(
                "`!dm @user [message]`\n"
                "→ Sends an anonymous DM to a player.\n"
                "→ Commands like `!roll` will execute as that user.\n"
                "→ Attachments and messages are logged.\n\n"

                "`!post [channel/thread] [message]`\n"
                "→ Post anonymously into RP channels or threads.\n"
                "→ Include a command like `!roll` and a user to simulate them:\n"
                "  `!post thread-name !roll 2d6+1 (username or userid)`"
            ),
            inline=False
        )

        embed.add_field(
            name="🗨️ RP Channel Management",
            value=(
                "`!start_rp @user1 @user2`\n"
                "→ Starts a private RP text channel for a group.\n\n"
                "`!end_rp`\n"
                "→ Logs the full session to a forum thread and deletes the channel."
            ),
            inline=False
        )

        embed.add_field(
            name="💸 Rent & Economy Tools",
            value=(
                "`!collect_rent [@user]` — Full rent pipeline.\n"
                "`!collect_housing [@user]` — Manual housing deduction.\n"
                "`!collect_business [@user]` — Manual business deduction.\n"
                "`!collect_trauma [@user]` — Manual trauma subscription.\n"
                "`!open_shop` — Logs a shop opening (Sunday only)."
            ),
            inline=False
        )

        embed.add_field(
            name="🧪 Dev & Debug Commands",
            value=(
                "`!test_bot` — Runs full self-test suite.\n"
                "Validates DMs, rent logic, RP logging, roll parsing, and permissions."
            ),
            inline=False
        )

        embed.set_footer(text="Fixer tools by MedusaCascade | v1.2")
        await ctx.send(embed=embed)