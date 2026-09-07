"""Token cache implementations — file-based and Redis-backed."""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from redis.asyncio import Redis


@dataclass
class TokenData:
    access_token: str
    expires_at: float


class BaseTokenCache(ABC):
    @abstractmethod
    async def read(self) -> TokenData | None: ...

    @abstractmethod
    async def write(self, data: TokenData) -> None: ...

    async def close(self) -> None:
        """Close cache resources if applicable."""


class FileTokenCache(BaseTokenCache):
    def __init__(self, cache_dir: Path, client_id: str, refresh_token: str) -> None:
        self._cache_file = cache_dir / f"token_{_cache_key(client_id, refresh_token)}.json"

    async def read(self) -> TokenData | None:
        return await asyncio.to_thread(self._read_sync)

    async def write(self, data: TokenData) -> None:
        await asyncio.to_thread(self._write_sync, data)

    def _read_sync(self) -> TokenData | None:
        if not self._cache_file.exists():
            return None
        try:
            raw = json.loads(self._cache_file.read_text(encoding="utf-8"))
            if "expires_at" in raw and raw.get("access_token"):
                return TokenData(
                    access_token=raw["access_token"],
                    expires_at=raw["expires_at"],
                )
        except (OSError, json.JSONDecodeError, KeyError) as e:
            logger.warning("Failed to read token cache: %s", e)
        return None

    def _write_sync(self, data: TokenData) -> None:
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "access_token": data.access_token,
            "expires_at": data.expires_at,
        }
        tmp = self._cache_file.with_suffix(f".tmp.{os.getpid()}")
        try:
            tmp.write_text(json.dumps(payload), encoding="utf-8")
            tmp.chmod(0o600)
            tmp.rename(self._cache_file)
        finally:
            if tmp.exists():
                tmp.unlink(missing_ok=True)


class RedisTokenCache(BaseTokenCache):
    def __init__(
        self,
        redis_url: str | None = None,
        client_id: str = "",
        refresh_token: str = "",
        *,
        redis_client: Redis | None = None,
        key_prefix: str = "amazon_ads:token:",
    ) -> None:
        self._owns_client = False
        if redis_client is not None:
            self._client: Redis = redis_client
        elif redis_url is not None:
            try:
                from redis.asyncio import Redis
            except ImportError:
                raise ImportError(
                    "Redis support requires the 'redis' extra: pip install async-amazon-ads-api-v1[redis]"
                ) from None
            self._client = Redis.from_url(redis_url, decode_responses=True)
            self._owns_client = True
        else:
            raise ValueError("Either redis_url or redis_client must be provided")

        self._key = f"{key_prefix}{_cache_key(client_id, refresh_token)}"

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def read(self) -> TokenData | None:
        raw = await self._client.get(self._key)
        if raw is None:
            return None
        try:
            data = json.loads(raw)
            if "expires_at" in data and data.get("access_token"):
                return TokenData(
                    access_token=data["access_token"],
                    expires_at=data["expires_at"],
                )
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Failed to parse Redis cache: %s", e)
        return None

    async def write(self, data: TokenData) -> None:
        payload = {
            "access_token": data.access_token,
            "expires_at": data.expires_at,
        }
        ttl = max(0, int(data.expires_at - time.time()))
        if ttl > 0:
            await self._client.set(self._key, json.dumps(payload), ex=ttl)
        else:
            await self._client.delete(self._key)


def _cache_key(client_id: str, refresh_token: str) -> str:
    return hashlib.sha256(f"{client_id}:{refresh_token}".encode()).hexdigest()[:16]
