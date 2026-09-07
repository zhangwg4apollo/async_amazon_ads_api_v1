"""Amazon Ads API package."""

from ads_api.base import ClientContext
from ads_api.client import AdsClient
from ads_api.client.v0 import AdsClientV0
from ads_api.client.v1 import AdsClientV1
from ads_api.config.region import Region
from ads_api.config.settings import AmazonAdsConfig
from ads_api.config.token_cache import BaseTokenCache, FileTokenCache, RedisTokenCache
from ads_api.config.token_manager import TokenCredentials, TokenManager

__all__ = [
    "AdsClient",
    "AdsClientV0",
    "AdsClientV1",
    "AmazonAdsConfig",
    "BaseTokenCache",
    "ClientContext",
    "FileTokenCache",
    "RedisTokenCache",
    "Region",
    "TokenCredentials",
    "TokenManager",
]
__version__ = "0.10.0"
