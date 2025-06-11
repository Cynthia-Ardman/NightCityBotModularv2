import json
import aiofiles
from pathlib import Path
from typing import Any, Dict, Optional

async def load_json_file(file_path: str, default: Any = None) -> Any:
    """Load JSON data from a file with async IO."""
    path = Path(file_path)
    try:
        if path.exists():
            async with aiofiles.open(str(path), 'r') as f:
                content = await f.read()
                return json.loads(content)
        return default
    except Exception as e:
        print(f"Error loading {path.name}: {e}")
        return default

async def save_json_file(file_path: str, data: Any) -> None:
    """Save JSON data to a file with async IO."""
    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(str(path), 'w') as f:
            await f.write(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error saving {path.name}: {e}")

def build_channel_name(usernames, max_length=100):
    """Build a Discord-friendly channel name."""
    import re
    full_name = "text-rp-" + "-".join(f"{name}-{uid}" for name, uid in usernames)
    if len(full_name) <= max_length:
        return re.sub(r"[^a-z0-9\-]", "", full_name.lower())

    simple_name = "text-rp-" + "-".join(name for name, _ in usernames)
    if len(simple_name) > max_length:
        simple_name = simple_name[:max_length]

    return re.sub(r"[^a-z0-9\-]", "", simple_name.lower())