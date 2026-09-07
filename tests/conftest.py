from __future__ import annotations

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
import pytest_asyncio

from ads_api.base import ClientContext
from ads_api.config.region import Region
from ads_api.config.settings import AmazonAdsConfig


@pytest.fixture
def config() -> AmazonAdsConfig:
    return AmazonAdsConfig(access_token="test-token", client_id="test-client-id", region=Region.NA)


@pytest_asyncio.fixture
async def ctx(config: AmazonAdsConfig) -> AsyncGenerator[ClientContext]:
    context = ClientContext(config)
    yield context
    if context._client is not None:
        await context._client.aclose()


@pytest.fixture
def mock_async_client() -> MagicMock:
    client = MagicMock(spec=httpx.AsyncClient)
    client.request = AsyncMock()
    return client


@pytest.fixture
def mock_response() -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = 200
    resp.content = b'{"dummy": "ok"}'
    return resp
