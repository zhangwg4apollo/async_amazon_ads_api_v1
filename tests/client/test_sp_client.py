from __future__ import annotations

import pytest

from ads_api import AdsClient, AmazonAdsConfig, Region
from ads_api.client.v1.sp.ad_extensions import SPAdExtensions
from ads_api.client.v1.sp.ad_groups import SPAdGroups
from ads_api.client.v1.sp.ads import SPAds
from ads_api.client.v1.sp.campaigns import SPCampaigns
from ads_api.client.v1.sp.targets import SPTargets


class TestSPNamespace:
    @pytest.fixture
    def config(self) -> AmazonAdsConfig:
        return AmazonAdsConfig(access_token="test-token", client_id="test-client", region=Region.NA)

    @pytest.mark.asyncio
    async def test_context_manager(self, config: AmazonAdsConfig) -> None:
        async with AdsClient(config) as ads:
            assert ads.v1.sp is not None

    @pytest.mark.asyncio
    async def test_close_without_client(self, config: AmazonAdsConfig) -> None:
        client = AdsClient(config)
        await client.close()

    @pytest.mark.asyncio
    async def test_close_cleans_up(self, config: AmazonAdsConfig) -> None:
        async with AdsClient(config) as ads:
            ctx = ads._ctx
            await ctx.get_client()
            assert ctx._client is not None
        assert ctx._client is None

    def test_campaigns_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        c = ads.v1.sp.campaigns
        assert isinstance(c, SPCampaigns)
        assert ads.v1.sp.campaigns is c

    def test_ad_groups_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ag = ads.v1.sp.ad_groups
        assert isinstance(ag, SPAdGroups)
        assert ads.v1.sp.ad_groups is ag

    def test_ads_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ad = ads.v1.sp.ads
        assert isinstance(ad, SPAds)
        assert ads.v1.sp.ads is ad

    def test_targets_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        t = ads.v1.sp.targets
        assert isinstance(t, SPTargets)
        assert ads.v1.sp.targets is t

    def test_ad_extensions_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ae = ads.v1.sp.ad_extensions
        assert isinstance(ae, SPAdExtensions)
        assert ads.v1.sp.ad_extensions is ae
