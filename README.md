# async-amazon-ads-api-v1

[![PyPI version](https://img.shields.io/pypi/v/async-amazon-ads-api-v1)](https://pypi.org/project/async-amazon-ads-api-v1/)
[![Python versions](https://img.shields.io/pypi/pyversions/async-amazon-ads-api-v1)](https://pypi.org/project/async-amazon-ads-api-v1/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Pure async Amazon Ads API client — **`ads_api`** 统一覆盖 v0 与 v1（SP、SB、SD、DSP、ST、SP Global、Accounts、Reporting、Ads Data Manager、Exports 等）。

## Installation

```bash
pip install async-amazon-ads-api-v1
# 或
uv add async-amazon-ads-api-v1
```

Redis 缓存支持：

```bash
pip install "async-amazon-ads-api-v1[redis]"
# 或
uv add "async-amazon-ads-api-v1[redis]"
```

## Quick Start

所有 API 方法仅接受 Pydantic model 实例，不支持 dict。默认 `mode="dict"`，需要模型对象时传 `mode="pydantic"`。

### 使用 Access Token

```python
import asyncio

from ads_api import AdsClient, AmazonAdsConfig, Region
from ads_api.models.v1.campaigns.sp import SPQueryCampaignRequest


async def main() -> None:
    config = AmazonAdsConfig(
        access_token="your-access-token",
        client_id="your-client-id",
        region=Region.NA,
    )
    body = SPQueryCampaignRequest(
        adProductFilter={"include": ["SPONSORED_PRODUCTS"]},
        stateFilter={"include": ["ENABLED"]},
    )

    async with AdsClient(config) as ads:
        resp = await ads.v1.sp.campaigns.query_campaign(body)
        print(resp)


asyncio.run(main())
```

### 使用 Refresh Token（自动续期）

```python
import asyncio

from ads_api import AdsClient, AmazonAdsConfig, Region
from ads_api.models.v1.campaigns.sp import SPQueryCampaignRequest


async def main() -> None:
    config = AmazonAdsConfig(
        client_id="your-client-id",
        refresh_token="your-refresh-token",
        client_secret="your-client-secret",
        region=Region.NA,
    )
    body = SPQueryCampaignRequest(
        adProductFilter={"include": ["SPONSORED_PRODUCTS"]},
        stateFilter={"include": ["ENABLED"]},
    )

    async with AdsClient(config) as ads:
        resp = await ads.v1.sp.campaigns.query_campaign(body, mode="pydantic")
        print(resp.model_dump_json(indent=2))


asyncio.run(main())
```

## Token Management

SDK 内置 OAuth token 生命周期管理。提供 `refresh_token` 与 `client_secret` 后会自动续期；缓存按字段推断：

```python
from ads_api import AmazonAdsConfig, Region

# 自动续期，不使用磁盘 / Redis 缓存
config = AmazonAdsConfig(
    client_id="your-client-id",
    client_secret="your-client-secret",
    refresh_token="your-refresh-token",
    region=Region.NA,
)

# 文件缓存
config = AmazonAdsConfig(
    client_id="your-client-id",
    client_secret="your-client-secret",
    refresh_token="your-refresh-token",
    region=Region.NA,
    token_cache_dir="~/.cache/ads_api",
)

# Redis 缓存
config = AmazonAdsConfig(
    client_id="your-client-id",
    client_secret="your-client-secret",
    refresh_token="your-refresh-token",
    region=Region.NA,
    redis_url="redis://localhost:6379",
)
```

## API 入口

```python
async with AdsClient(config) as ads:
    # v1
    await ads.v1.sp.campaigns.query_campaign(body)
    await ads.v1.sb.campaigns.query_campaign(body)
    await ads.v1.sd.campaigns.query_campaign(body)
    await ads.v1.selling_accounts.query_selling_account(body)

    # v0
    await ads.v0.accounts.profiles.list_profiles()
    await ads.v0.portfolios.list_portfolios()
    await ads.v0.sp_v3.campaigns.create_sponsored_products_campaigns(body)
    await ads.v0.sb_v4.budget_rules.create_budget_rules_for_sb_campaigns(body)
    await ads.v0.sd.creatives.create_creatives(body)
```

详细代码生成与说明请参见 [script4/README.md](script4/README.md) (v1) 与 [script3/README.md](script3/README.md) (v0)。

## License

[MIT](LICENSE)
