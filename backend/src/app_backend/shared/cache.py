"""
Redis cache helper untuk analytics endpoints.
Semua error Redis dibungkus silently agar tidak merusak request jika Redis down.
"""

import json
import os
from typing import Any, Optional

import redis

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/2")
ANALYTICS_CACHE_TTL = 300  # 5 menit


def _client() -> redis.Redis:
    return redis.from_url(REDIS_URL, decode_responses=True)


def cache_get(key: str) -> Optional[Any]:
    try:
        data = _client().get(key)
        return json.loads(data) if data else None
    except Exception:
        return None


def cache_set(key: str, value: Any, ttl: int = ANALYTICS_CACHE_TTL) -> None:
    try:
        _client().setex(key, ttl, json.dumps(value, default=str))
    except Exception:
        pass


def cache_delete(key: str) -> None:
    try:
        _client().delete(key)
    except Exception:
        pass


def cache_ttl(key: str) -> int:
    """Kembalikan TTL key dalam detik, atau -2 jika tidak ada."""
    try:
        return _client().ttl(key)
    except Exception:
        return -2
