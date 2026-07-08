from __future__ import annotations

import json
import time
from typing import Any

from app.core.config import settings

_memory: dict[str, tuple[float, Any]] = {}


async def cache_get(key: str) -> Any | None:
    entry = _memory.get(key)
    if entry and entry[0] > time.time():
        return entry[1]

    try:
        import redis.asyncio as aioredis

        client = aioredis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=0.5)
        val = await client.get(key)
        await client.aclose()
        if val:
            parsed = json.loads(val)
            _memory[key] = (time.time() + 3600, parsed)
            return parsed
    except Exception:
        pass

    return None


async def cache_set(key: str, value: Any, ttl: int = 3600) -> None:
    _memory[key] = (time.time() + ttl, value)
    try:
        import redis.asyncio as aioredis

        client = aioredis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=0.5)
        await client.setex(key, ttl, json.dumps(value, default=str))
        await client.aclose()
    except Exception:
        pass
