from __future__ import annotations

import ads_api
from ads_api import AdsClient, AmazonAdsConfig, Region, TokenCredentials, TokenManager


class TestAdsApiExports:
    def test_version(self) -> None:
        assert ads_api.__version__ == "0.10.0"

    def test_all(self) -> None:
        assert set(ads_api.__all__) == {
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
        }

    def test_imports(self) -> None:
        assert AdsClient is not None
        assert AmazonAdsConfig is not None
        assert Region is not None
        assert TokenManager is not None
        assert TokenCredentials is not None
