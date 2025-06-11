from pathlib import Path
import aiofiles
import json
import asyncio
from typing import Dict, Any, Optional

class DatabaseManager:
    def __init__(self):
        self._locks: Dict[str, asyncio.Lock] = {}
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _get_lock(self, file_path: str) -> asyncio.Lock:
        """Get or create a lock for a file."""
        if file_path not in self._locks:
            self._locks[file_path] = asyncio.Lock()
        return self._locks[file_path]

    async def load(self, file_path: str, default: Any = None) -> Any:
        """Load data from file with proper locking."""
        path = Path(file_path)
        async with self._get_lock(str(path)):
            try:
                if path.exists():
                    async with aiofiles.open(path, 'r') as f:
                        content = await f.read()
                        data = json.loads(content)
                        self._cache[str(path)] = data
                        return data
                return default
            except Exception as e:
                print(f"Error loading {path.name}: {e}")
                return default

    async def save(self, file_path: str, data: Any) -> None:
        """Save data to file with proper locking."""
        path = Path(file_path)
        async with self._get_lock(str(path)):
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                async with aiofiles.open(path, 'w') as f:
                    await f.write(json.dumps(data, indent=2))
                self._cache[str(path)] = data
            except Exception as e:
                print(f"Error saving {path.name}: {e}")

    async def update(self, file_path: str, key: str, value: Any) -> None:
        """Atomically update a single key in a JSON file."""
        path = Path(file_path)
        async with self._get_lock(str(path)):
            data = await self.load(file_path, default={})
            data[key] = value
            await self.save(file_path, data)

    def get_cached(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get cached data for a file."""
        return self._cache.get(str(Path(file_path)))

db = DatabaseManager()