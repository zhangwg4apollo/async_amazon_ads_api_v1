from __future__ import annotations

import os
import time
from collections.abc import AsyncGenerator
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from ads_api.config.token_cache import BaseTokenCache, FileTokenCache, RedisTokenCache, TokenData

REDIS_URL = os.environ.get("TEST_REDIS_URL", "redis://localhost:6379/0")
HAS_REDIS = os.environ.get("TEST_REDIS_URL") is not None


@pytest.fixture
def token_data() -> TokenData:
    return TokenData(
        access_token="test-access-token",
        expires_at=time.time() + 3600,
    )


@pytest.fixture
def file_cache(tmp_path: Path) -> FileTokenCache:
    return FileTokenCache(
        cache_dir=tmp_path,
        client_id="test-client",
        refresh_token="test-refresh",
    )


@pytest_asyncio.fixture
async def redis_cache() -> AsyncGenerator[RedisTokenCache]:
    cache = RedisTokenCache(
        redis_url=REDIS_URL,
        client_id="test-client",
        refresh_token="test-refresh",
    )
    await cache._client.flushdb()
    yield cache
    await cache.close()


@pytest.mark.asyncio
class TestFileTokenCache:
    async def test_read_empty_cache(self, file_cache: FileTokenCache) -> None:
        result = await file_cache.read()
        assert result is None

    async def test_write_and_read(self, file_cache: FileTokenCache, token_data: TokenData) -> None:
        await file_cache.write(token_data)
        result = await file_cache.read()
        assert result is not None
        assert result.access_token == token_data.access_token
        assert result.expires_at == token_data.expires_at

    async def test_overwrite(self, file_cache: FileTokenCache) -> None:
        data1 = TokenData(access_token="token-1", expires_at=time.time() + 100)
        data2 = TokenData(access_token="token-2", expires_at=time.time() + 200)

        await file_cache.write(data1)
        await file_cache.write(data2)

        result = await file_cache.read()
        assert result is not None
        assert result.access_token == "token-2"

    async def test_corrupted_file_returns_none(self, file_cache: FileTokenCache) -> None:
        file_cache._cache_file.parent.mkdir(parents=True, exist_ok=True)
        file_cache._cache_file.write_text("not valid json", encoding="utf-8")
        result = await file_cache.read()
        assert result is None

    async def test_missing_fields_returns_none(self, file_cache: FileTokenCache) -> None:
        import json

        file_cache._cache_file.parent.mkdir(parents=True, exist_ok=True)
        file_cache._cache_file.write_text(json.dumps({"foo": "bar"}), encoding="utf-8")
        result = await file_cache.read()
        assert result is None

    async def test_different_credentials_different_files(self, tmp_path: Path) -> None:
        cache1 = FileTokenCache(cache_dir=tmp_path, client_id="client1", refresh_token="rt1")
        cache2 = FileTokenCache(cache_dir=tmp_path, client_id="client2", refresh_token="rt2")

        data = TokenData(access_token="tok", expires_at=time.time() + 100)
        await cache1.write(data)

        assert await cache1.read() is not None
        assert await cache2.read() is None


@pytest.mark.asyncio
@pytest.mark.skipif(not HAS_REDIS, reason="TEST_REDIS_URL not set")
class TestRedisTokenCache:
    async def test_read_empty_cache(self, redis_cache: RedisTokenCache) -> None:
        result = await redis_cache.read()
        assert result is None

    async def test_write_and_read(self, redis_cache: RedisTokenCache, token_data: TokenData) -> None:
        await redis_cache.write(token_data)
        result = await redis_cache.read()
        assert result is not None
        assert result.access_token == token_data.access_token
        assert result.expires_at == token_data.expires_at

    async def test_ttl_based_on_expires_at(self, redis_cache: RedisTokenCache) -> None:
        data = TokenData(
            access_token="tok",
            expires_at=time.time() + 60,
        )
        await redis_cache.write(data)
        ttl = await redis_cache._client.ttl(redis_cache._key)
        assert 50 <= ttl <= 60

    async def test_expired_token_not_written(self, redis_cache: RedisTokenCache) -> None:
        data = TokenData(
            access_token="tok",
            expires_at=time.time() - 10,
        )
        await redis_cache.write(data)
        result = await redis_cache.read()
        assert result is None

    async def test_overwrite(self, redis_cache: RedisTokenCache) -> None:
        data1 = TokenData(access_token="token-1", expires_at=time.time() + 100)
        data2 = TokenData(access_token="token-2", expires_at=time.time() + 200)

        await redis_cache.write(data1)
        await redis_cache.write(data2)

        result = await redis_cache.read()
        assert result is not None
        assert result.access_token == "token-2"

    async def test_different_credentials_different_keys(self, redis_cache: RedisTokenCache) -> None:
        cache2 = RedisTokenCache(redis_url=REDIS_URL, client_id="c2", refresh_token="rt2")
        try:
            data = TokenData(access_token="tok", expires_at=time.time() + 100)
            await redis_cache.write(data)

            assert await redis_cache.read() is not None
            assert await cache2.read() is None
        finally:
            await cache2.close()


class TestBaseTokenCache:
    def test_cannot_instantiate_abstract(self) -> None:
        with pytest.raises(TypeError):
            BaseTokenCache()  # type: ignore[abstract]


@pytest.mark.asyncio
class TestRedisTokenCacheInjected:
    async def test_injected_client_is_not_closed(self) -> None:
        mock_redis = MagicMock()
        mock_redis.get = AsyncMock(return_value='{"access_token": "redis-tok", "expires_at": 9999999999.0}')
        mock_redis.set = AsyncMock()
        mock_redis.aclose = AsyncMock()

        cache = RedisTokenCache(client_id="cid", refresh_token="rt", redis_client=mock_redis)
        assert cache._owns_client is False

        data = await cache.read()
        assert data is not None
        assert data.access_token == "redis-tok"

        await cache.write(TokenData(access_token="new-tok", expires_at=time.time() + 3600))
        mock_redis.set.assert_awaited_once()

        await cache.close()
        mock_redis.aclose.assert_not_awaited()

    async def test_owned_client_is_closed(self) -> None:
        mock_redis = MagicMock()
        mock_redis.aclose = AsyncMock()

        with patch("redis.asyncio.Redis.from_url", return_value=mock_redis):
            cache = RedisTokenCache(redis_url="redis://localhost:6379/0", client_id="cid", refresh_token="rt")
            assert cache._owns_client is True
            await cache.close()
            mock_redis.aclose.assert_awaited_once()
