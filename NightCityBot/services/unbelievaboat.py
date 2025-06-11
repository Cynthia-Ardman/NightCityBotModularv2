import os
import aiohttp
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()


class UnbelievaBoatAPI:
    def __init__(self):
        self.api_token = os.getenv('UNBELIEVABOAT_TOKEN')
        self.guild_id = int(os.getenv('GUILD_ID', '0'))
        self.api_base = "https://unbelievaboat.com/api/v1"

    async def get_balance(self, user_id: int) -> Optional[Dict[str, int]]:
        """Get a user's balance from UnbelievaBoat."""
        url = f"{self.api_base}/guilds/{self.guild_id}/users/{user_id}"
        headers = {"Authorization": self.api_token}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None

    async def update_balance(
            self,
            user_id: int,
            amount_dict: Dict[str, int],
            reason: str = "Automated transaction"
    ) -> bool:
        """Update a user's balance on UnbelievaBoat."""
        url = f"{self.api_base}/guilds/{self.guild_id}/users/{user_id}"
        headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json"
        }
        payload = {**amount_dict, "reason": reason}

        async with aiohttp.ClientSession() as session:
            async with session.patch(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    print(f"❌ PATCH failed: {resp.status} — {error}")
                return resp.status == 200