from __future__ import annotations

import asyncio
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ads_api.config.region import ENDPOINT_MAP, Region
from ads_api.config.settings import AmazonAdsConfig
from ads_api.config.token_cache import FileTokenCache, RedisTokenCache, TokenData
from ads_api.config.token_manager import TokenCredentials, TokenManager


class TestRegion:
    def test_str_enum_identity(self) -> None:
        assert str(Region.NA) == "na"
        assert Region.NA.value == "na"


class TestAmazonAdsConfig:
    def test_defaults(self) -> None:
        cfg = AmazonAdsConfig(access_token="abc", client_id="cli")
        assert cfg.access_token == "abc"
        assert cfg.client_id == "cli"
        assert cfg.base_url == ENDPOINT_MAP["na"]
        assert cfg.profile_id is None
        assert cfg.timeout == 600.0
        assert cfg.max_retries == 3

    def test_endpoints_override(self) -> None:
        cfg = AmazonAdsConfig(
            access_token="xyz",
            client_id="cli",
            endpoints={"eu": "http://localhost:8080"},
            region=Region.EU,
        )
        assert cfg.base_url == "http://localhost:8080"

    def test_endpoints_override_wrong_region_raises(self) -> None:
        cfg = AmazonAdsConfig(
            access_token="xyz",
            client_id="cli",
            endpoints={"na": "http://localhost:8080"},
            region=Region.EU,
        )
        with pytest.raises(KeyError):
            _ = cfg.base_url

    def test_endpoints_empty_dict_falls_back(self) -> None:
        cfg = AmazonAdsConfig(
            access_token="xyz",
            client_id="cli",
            endpoints={},
            region=Region.FE,
        )
        assert cfg.base_url == ENDPOINT_MAP["fe"]

    def test_region_based_base_url(self) -> None:
        cfg = AmazonAdsConfig(
            access_token="xyz",
            client_id="cli",
            region=Region.FE,
        )
        assert cfg.base_url == ENDPOINT_MAP["fe"]

    def test_invalid_region_raises(self) -> None:
        with pytest.raises(ValueError):
            AmazonAdsConfig(access_token="xyz", client_id="cli", region="invalid")

    def test_explicit_values(self) -> None:
        cfg = AmazonAdsConfig(
            access_token="xyz",
            client_id="cli",
            region=Region.EU,
            profile_id="123",
            timeout=30.0,
            max_retries=5,
        )
        assert cfg.access_token == "xyz"
        assert cfg.client_id == "cli"
        assert cfg.profile_id == "123"
        assert cfg.timeout == 30.0
        assert cfg.max_retries == 5

    def test_empty_token_raises(self) -> None:
        with pytest.raises(ValueError, match="access_token or both"):
            AmazonAdsConfig(access_token="", client_id="cli")

    def test_non_positive_timeout_raises(self) -> None:
        with pytest.raises(ValueError, match="timeout must be a positive number"):
            AmazonAdsConfig(access_token="t", client_id="cli", timeout=0)

    def test_negative_max_retries_raises(self) -> None:
        with pytest.raises(ValueError, match="max_retries cannot be negative"):
            AmazonAdsConfig(access_token="t", client_id="cli", max_retries=-1)


class TestTokenManager:
    def _manager(self, cache: AsyncMock | None = None) -> TokenManager:
        return TokenManager(
            credentials=TokenCredentials(client_id="cid", client_secret="sec", refresh_token="rt"),
            cache=cache,
        )

    @pytest.mark.asyncio
    async def test_force_refresh_bypasses_cache(self) -> None:
        tm = self._manager()
        tm.access_token = "cached-token"
        tm._expires_at = 9999999999.0

        assert await tm.get_access_token(force=False) == "cached-token"

        with patch.object(TokenManager, "_refresh", AsyncMock(return_value="fresh-token")) as mock_refresh:
            token = await tm.get_access_token(force=True)
            assert token == "fresh-token"
            mock_refresh.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_memory_hit_skips_cache_and_refresh(self) -> None:
        cache = AsyncMock()
        tm = self._manager(cache)
        tm.access_token = "mem-token"
        tm._expires_at = time.time() + 3600

        assert await tm.get_access_token() == "mem-token"
        cache.read.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_cache_hit_reads_once(self) -> None:
        cache = AsyncMock()
        cache.read = AsyncMock(return_value=TokenData(access_token="cached-token", expires_at=time.time() + 3600))
        tm = self._manager(cache)

        with patch.object(type(tm), "_refresh", AsyncMock()) as mock_refresh:
            assert await tm.get_access_token() == "cached-token"
            cache.read.assert_awaited_once()
            mock_refresh.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_cache_miss_reads_once_then_refreshes(self) -> None:
        cache = AsyncMock()
        cache.read = AsyncMock(return_value=None)
        tm = self._manager(cache)

        with patch.object(type(tm), "_refresh", AsyncMock(return_value="fresh-token")) as mock_refresh:
            assert await tm.get_access_token() == "fresh-token"
            cache.read.assert_awaited_once()
            mock_refresh.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_force_skips_memory_and_cache(self) -> None:
        cache = AsyncMock()
        tm = self._manager(cache)
        tm.access_token = "mem-token"
        tm._expires_at = time.time() + 3600

        with patch.object(type(tm), "_refresh", AsyncMock(return_value="fresh-token")) as mock_refresh:
            assert await tm.get_access_token(force=True) == "fresh-token"
            cache.read.assert_not_awaited()
            mock_refresh.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_concurrent_calls_refresh_once(self) -> None:
        cache = AsyncMock()
        cache.read = AsyncMock(return_value=None)
        tm = self._manager(cache)
        refresh_calls = 0

        async def fake_refresh(_self: object) -> str:
            nonlocal refresh_calls
            refresh_calls += 1
            await asyncio.sleep(0)
            tm.access_token = "fresh-token"
            tm._expires_at = time.time() + 3600
            return "fresh-token"

        with patch.object(type(tm), "_refresh", fake_refresh):
            results = await asyncio.gather(tm.get_access_token(), tm.get_access_token())
        assert results == ["fresh-token", "fresh-token"]
        assert refresh_calls == 1
        cache.read.assert_awaited_once()


_CREDS = {"client_id": "cid", "client_secret": "sec", "refresh_token": "rt"}


class TestCacheInference:
    def test_no_cache_by_default(self) -> None:
        cfg = AmazonAdsConfig(**_CREDS)
        assert cfg._token_manager is not None
        assert cfg._token_manager._cache is None

    def test_file_cache_from_dir(self, tmp_path: Path) -> None:
        cfg = AmazonAdsConfig(**_CREDS, token_cache_dir=str(tmp_path))
        assert isinstance(cfg._token_manager._cache, FileTokenCache)

    def test_redis_from_client(self) -> None:
        cfg = AmazonAdsConfig(**_CREDS, redis_client=MagicMock())
        assert isinstance(cfg._token_manager._cache, RedisTokenCache)

    def test_custom_cache_wins(self, tmp_path: Path) -> None:
        custom = FileTokenCache(cache_dir=tmp_path, client_id="cid", refresh_token="rt")
        cfg = AmazonAdsConfig(
            **_CREDS,
            token_cache=custom,
            redis_url="redis://localhost:6379/0",
            token_cache_dir=str(tmp_path),
        )
        assert cfg._token_manager._cache is custom

    def test_redis_wins_over_file(self, tmp_path: Path) -> None:
        with patch("redis.asyncio.Redis.from_url", return_value=MagicMock()):
            cfg = AmazonAdsConfig(
                **_CREDS,
                redis_url="redis://localhost:6379/0",
                token_cache_dir=str(tmp_path),
            )
        assert isinstance(cfg._token_manager._cache, RedisTokenCache)
