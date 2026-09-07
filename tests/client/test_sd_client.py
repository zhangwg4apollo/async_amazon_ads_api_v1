from __future__ import annotations

import pytest

from ads_api import AdsClient, AmazonAdsConfig, Region
from ads_api.client.v1.sd.ad_groups import SDAdGroups
from ads_api.client.v1.sd.ads import SDAds
from ads_api.client.v1.sd.campaigns import SDCampaigns
from ads_api.client.v1.sd.targets import SDTargets


class TestSDNamespace:
    @pytest.fixture
    def config(self) -> AmazonAdsConfig:
        return AmazonAdsConfig(access_token="test-token", client_id="test-client", region=Region.NA)

    @pytest.mark.asyncio
    async def test_context_manager(self, config: AmazonAdsConfig) -> None:
        async with AdsClient(config) as ads:
            assert ads.v1.sd is not None

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
        c = ads.v1.sd.campaigns
        assert isinstance(c, SDCampaigns)
        assert ads.v1.sd.campaigns is c

    def test_ad_groups_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ag = ads.v1.sd.ad_groups
        assert isinstance(ag, SDAdGroups)
        assert ads.v1.sd.ad_groups is ag

    def test_ads_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ad = ads.v1.sd.ads
        assert isinstance(ad, SDAds)
        assert ads.v1.sd.ads is ad

    def test_targets_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        t = ads.v1.sd.targets
        assert isinstance(t, SDTargets)
        assert ads.v1.sd.targets is t
