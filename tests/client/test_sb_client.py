from __future__ import annotations

import pytest

from ads_api import AdsClient, AmazonAdsConfig, Region
from ads_api.client.v1.sb.ad_extensions import SBAdExtensions
from ads_api.client.v1.sb.ad_groups import SBAdGroups
from ads_api.client.v1.sb.ads import SBAds
from ads_api.client.v1.sb.advertising_deal_targets import SBAdvertisingDealTargets
from ads_api.client.v1.sb.advertising_deals import SBAdvertisingDeals
from ads_api.client.v1.sb.branded_keywords_pricings import SBBrandedKeywordsPricings
from ads_api.client.v1.sb.campaigns import SBCampaigns
from ads_api.client.v1.sb.keyword_reservation_validations import SBKeywordReservationValidations
from ads_api.client.v1.sb.recommendation_types import SBRecommendationTypes
from ads_api.client.v1.sb.recommendations import SBRecommendations
from ads_api.client.v1.sb.targets import SBTargets


class TestSBNamespace:
    @pytest.fixture
    def config(self) -> AmazonAdsConfig:
        return AmazonAdsConfig(access_token="test-token", client_id="test-client", region=Region.NA)

    @pytest.mark.asyncio
    async def test_context_manager(self, config: AmazonAdsConfig) -> None:
        async with AdsClient(config) as ads:
            assert ads.v1.sb is not None

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
        c = ads.v1.sb.campaigns
        assert isinstance(c, SBCampaigns)
        assert ads.v1.sb.campaigns is c

    def test_ad_groups_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ag = ads.v1.sb.ad_groups
        assert isinstance(ag, SBAdGroups)
        assert ads.v1.sb.ad_groups is ag

    def test_ads_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ad = ads.v1.sb.ads
        assert isinstance(ad, SBAds)
        assert ads.v1.sb.ads is ad

    def test_targets_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        t = ads.v1.sb.targets
        assert isinstance(t, SBTargets)
        assert ads.v1.sb.targets is t

    def test_ad_extensions_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ae = ads.v1.sb.ad_extensions
        assert isinstance(ae, SBAdExtensions)
        assert ads.v1.sb.ad_extensions is ae

    def test_advertising_deal_targets_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        adt = ads.v1.sb.advertising_deal_targets
        assert isinstance(adt, SBAdvertisingDealTargets)
        assert ads.v1.sb.advertising_deal_targets is adt

    def test_advertising_deals_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        ad = ads.v1.sb.advertising_deals
        assert isinstance(ad, SBAdvertisingDeals)
        assert ads.v1.sb.advertising_deals is ad

    def test_branded_keywords_pricings_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        bkp = ads.v1.sb.branded_keywords_pricings
        assert isinstance(bkp, SBBrandedKeywordsPricings)
        assert ads.v1.sb.branded_keywords_pricings is bkp

    def test_keyword_reservation_validations_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        krv = ads.v1.sb.keyword_reservation_validations
        assert isinstance(krv, SBKeywordReservationValidations)
        assert ads.v1.sb.keyword_reservation_validations is krv

    def test_recommendation_types_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        rt = ads.v1.sb.recommendation_types
        assert isinstance(rt, SBRecommendationTypes)
        assert ads.v1.sb.recommendation_types is rt

    def test_recommendations_property(self, config: AmazonAdsConfig) -> None:
        ads = AdsClient(config)
        r = ads.v1.sb.recommendations
        assert isinstance(r, SBRecommendations)
        assert ads.v1.sb.recommendations is r
