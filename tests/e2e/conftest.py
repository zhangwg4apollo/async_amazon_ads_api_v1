from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from uuid import uuid4

import httpx
import pytest
import pytest_asyncio

from ads_api import AdsClient, AmazonAdsConfig, Region

from .config import E2ESettings, load_settings

E2E_DIR = Path(__file__).parent.resolve()


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        item_path = Path(str(item.fspath)).resolve()
        if item_path == E2E_DIR or E2E_DIR in item_path.parents:
            item.add_marker(pytest.mark.e2e)


@pytest.fixture(scope="session")
def e2e_settings() -> E2ESettings:
    return load_settings()


@pytest.fixture(scope="session", autouse=True)
def require_ads_v1_server(e2e_settings: E2ESettings) -> None:
    try:
        resp = httpx.get(
            f"{e2e_settings.base_url}/health",
            timeout=e2e_settings.timeout,
            trust_env=False,
        )
    except httpx.HTTPError as exc:
        pytest.skip(f"ads_v1_server 不可用：{exc}")
    if resp.status_code != 200:
        pytest.skip(f"ads_v1_server /health 返回 {resp.status_code}: {resp.text}")


@pytest.fixture
def amazon_ads_config(e2e_settings: E2ESettings) -> AmazonAdsConfig:
    return AmazonAdsConfig(
        client_id=e2e_settings.client_id,
        client_secret=e2e_settings.client_secret,
        refresh_token=e2e_settings.refresh_token,
        profile_id=e2e_settings.profile_id,
        region=Region.NA,
        endpoints={"na": e2e_settings.base_url},
        token_url=e2e_settings.token_url,
        timeout=e2e_settings.timeout,
    )


@pytest_asyncio.fixture
async def ads_client(amazon_ads_config: AmazonAdsConfig) -> AsyncGenerator[AdsClient]:
    async with AdsClient(amazon_ads_config) as client:
        yield client


@pytest_asyncio.fixture
async def access_token(e2e_settings: E2ESettings) -> str:
    async with httpx.AsyncClient(
        base_url=e2e_settings.base_url,
        timeout=e2e_settings.timeout,
        trust_env=False,
    ) as client:
        resp = await client.post(
            "/auth/o2/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": e2e_settings.refresh_token,
                "client_id": e2e_settings.client_id,
                "client_secret": e2e_settings.client_secret,
            },
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 3600
    assert body["refresh_token"] == e2e_settings.refresh_token
    return str(body["access_token"])


@pytest.fixture
def unique_name() -> str:
    return f"ads-v1-e2e-{uuid4()}"
