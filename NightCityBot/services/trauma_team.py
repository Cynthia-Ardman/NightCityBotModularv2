import os
import discord
from dotenv import load_dotenv
from typing import Optional, List, Dict
from NightCityBot.utils.constants import TRAUMA_ROLE_COSTS
from NightCityBot.services.unbelievaboat import UnbelievaBoatAPI

load_dotenv()

class TraumaTeam:
    def __init__(self):
        self.response_channel_id = int(os.getenv('TRAUMA_RESPONSE_CHANNEL_ID', '0'))
        self.trauma_forum_channel_id = int(os.getenv('TRAUMA_FORUM_CHANNEL_ID', '0'))
        self.trauma_team_role_id = int(os.getenv('TRAUMA_TEAM_ROLE_ID', '0'))
        self.cooldown_minutes = int(os.getenv('TRAUMA_COOLDOWN_MINUTES', '60'))
        self.cost = int(os.getenv('TRAUMA_COST', '5000'))
        self.unbelievaboat = UnbelievaBoatAPI()

    async def process_trauma_team_payment(
            self,
            member: discord.Member,
            trauma_channel: discord.ForumChannel,
            *,
            log: Optional[List[str]] = None
    ) -> None:
        """Process Trauma Team subscription payment for a member."""
        if not isinstance(trauma_channel, discord.ForumChannel):
            if log is not None:
                log.append("⚠️ TT forum channel not found.")
            return

        balance = await self.unbelievaboat.get_balance(member.id)
        if not balance:
            if log is not None:
                log.append("⚠️ Could not fetch balance for Trauma processing.")
            return

        cash = balance["cash"]
        bank = balance["bank"]

        trauma_role = next(
            (r for r in member.roles if r.name in TRAUMA_ROLE_COSTS),
            None
        )
        if not trauma_role:
            return  # no subscription

        cost = TRAUMA_ROLE_COSTS[trauma_role.name]
        if log is not None:
            log.append(f"🔎 {trauma_role.name} → Subscription: ${cost}")
            log.append(f"💊 Deducting ${cost} for Trauma Team plan: {trauma_role.name}")

        # Find user's trauma thread
        thread_name_suffix = f"- {member.id}"
        target_thread = next(
            (t for t in trauma_channel.threads if t.name.endswith(thread_name_suffix)),
            None
        )
        if not target_thread:
            if log is not None:
                log.append(f"⚠️ Could not locate Trauma Team thread for <@{member.id}>")
            return

        if cash + bank < cost:
            mention = f"<@&{self.trauma_team_role_id}>"
            await target_thread.send(
                f"❌ Payment for **{trauma_role.name}** (${cost}) by <@{member.id}> failed."
                f"\n## {mention} Subscription suspended."
            )
            if log is not None:
                log.append("❌ Insufficient funds for Trauma payment.")
            return

        payload = {
            "cash": -min(cash, cost),
            "bank": -(cost - min(cash, cost)),
        }
        success = await self.unbelievaboat.update_balance(
            member.id,
            payload,
            reason="Trauma Team Subscription"
        )

        if success:
            await target_thread.send(
                f"✅ **Payment Successful** — <@{member.id}> paid `${cost}` for **{trauma_role.name}** coverage."
            )
            if log is not None:
                log.append("✅ Trauma Team payment completed. Notice Sent to users #tt-plans-payment thread.")
        else:
            await target_thread.send(
                f"⚠️ **Deduction failed** for <@{member.id}> despite available funds."
            )
            if log is not None:
                log.append("⚠️ PATCH failed for Trauma Team payment.")