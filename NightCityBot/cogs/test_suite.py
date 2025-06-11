import os
import discord
from discord.ext import commands
from typing import Optional, List, Dict
from dotenv import load_dotenv
from NightCityBot.utils.permissions import is_fixer

load_dotenv()


class TestSuite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test_channel_id = int(os.getenv('TEST_CHANNEL_ID', '0'))
        self.test_data_file = os.getenv('TEST_DATA_FILE', 'data/test_data.json')
        self.test_results: Dict[str, List[dict]] = {}

    @commands.group(invoke_without_command=True)
    @is_fixer()
    async def test(self, ctx):
        """Run test suite or show test commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Available test commands:\n"
                "`test run` - Run all tests\n"
                "`test commands` - Test command functionality\n"
                "`test permissions` - Test permission settings\n"
                "`test economy` - Test economy features\n"
                "`test dm` - Test DM functionality"
            )

    @test.command(name="run")
    @is_fixer()
    async def run_tests(self, ctx):
        """Run all tests."""
        await ctx.send("🧪 Running test suite...")

        results = []

        # Test bot status
        results.append({
            "name": "Bot Status",
            "success": self.bot.is_ready(),
            "details": f"Latency: {round(self.bot.latency * 1000)}ms"
        })

        # Test permissions
        test_user = await self.get_test_user(ctx)
        results.append({
            "name": "Permission Check",
            "success": test_user is not None,
            "details": f"Test user: {test_user.name if test_user else 'Not found'}"
        })

        # Send results
        embed = await self.format_test_results(results)
        await ctx.send(embed=embed)

    @test.command(name="commands")
    @is_fixer()
    async def test_commands(self, ctx):
        """Test basic command functionality."""
        await ctx.send("🧪 Testing commands...")

        results = []

        # Test ping command
        try:
            test_ctx = await self.bot.get_context(ctx.message)
            ping_cog = self.bot.get_cog('Admin')
            await ping_cog.ping(test_ctx)
            results.append({
                "name": "Ping Command",
                "success": True,
                "details": "Command executed successfully"
            })
        except Exception as e:
            results.append({
                "name": "Ping Command",
                "success": False,
                "details": f"Error: {str(e)}"
            })

        # Send results
        embed = await self.format_test_results(results)
        await ctx.send(embed=embed)

    async def get_test_user(self, ctx) -> Optional[discord.Member]:
        """Get a test user from the server."""
        test_user_id = os.getenv('TEST_USER_ID')
        if test_user_id:
            try:
                return await ctx.guild.fetch_member(int(test_user_id))
            except:
                pass
        return None

    async def format_test_results(self, results: List[dict]) -> discord.Embed:
        """Format test results into an embed."""
        embed = discord.Embed(
            title="Test Results",
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )

        for result in results:
            status = "✅" if result["success"] else "❌"
            embed.add_field(
                name=f"{status} {result['name']}",
                value=result["details"],
                inline=False
            )

        return embed

    @test.command(name="permissions")
    @is_fixer()
    async def test_permissions(self, ctx):
        """Test permission settings."""
        await ctx.send("🧪 Testing permissions...")

        results = []
        test_user = await self.get_test_user(ctx)

        if test_user:
            # Test Fixer role
            has_fixer = any(role.name == os.getenv('FIXER_ROLE_NAME', 'Fixer')
                            for role in test_user.roles)
            results.append({
                "name": "Fixer Role Check",
                "success": has_fixer,
                "details": f"User {'has' if has_fixer else 'does not have'} Fixer role"
            })
        else:
            results.append({
                "name": "Test User",
                "success": False,
                "details": "Could not find test user"
            })

        embed = await self.format_test_results(results)
        await ctx.send(embed=embed)

    @test.command(name="economy")
    @is_fixer()
    async def test_economy(self, ctx):
        """Test economy features."""
        await ctx.send("🧪 Testing economy system...")

        results = []
        test_user = await self.get_test_user(ctx)

        if test_user:
            try:
                economy_cog = self.bot.get_cog('Economy')
                balance = await economy_cog.get_balance(str(test_user.id))
                results.append({
                    "name": "Balance Check",
                    "success": True,
                    "details": f"Balance: {balance} {economy_cog.currency_name}"
                })
            except Exception as e:
                results.append({
                    "name": "Balance Check",
                    "success": False,
                    "details": f"Error: {str(e)}"
                })
        else:
            results.append({
                "name": "Test User",
                "success": False,
                "details": "Could not find test user"
            })

        embed = await self.format_test_results(results)
        await ctx.send(embed=embed)

    @test.command(name="dm")
    @is_fixer()
    async def test_dm(self, ctx):
        """Test DM functionality."""
        await ctx.send("🧪 Testing DM system...")

        results = []
        test_user = await self.get_test_user(ctx)

        if test_user:
            try:
                dm_cog = self.bot.get_cog('DMHandler')
                thread = await dm_cog.get_or_create_dm_thread(test_user)
                results.append({
                    "name": "DM Thread Creation",
                    "success": True,
                    "details": f"Thread created: {thread.name}"
                })
            except Exception as e:
                results.append({
                    "name": "DM Thread Creation",
                    "success": False,
                    "details": f"Error: {str(e)}"
                })
        else:
            results.append({
                "name": "Test User",
                "success": False,
                "details": "Could not find test user"
            })

        embed = await self.format_test_results(results)
        await ctx.send(embed=embed)