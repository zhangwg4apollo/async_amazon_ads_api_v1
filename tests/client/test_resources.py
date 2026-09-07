"""Verify generated v1 resource classes expose the expected operations."""

from __future__ import annotations

from ads_api.client.v1.sb.branded_keywords_pricings import SBBrandedKeywordsPricings
from ads_api.client.v1.sb.keyword_reservation_validations import SBKeywordReservationValidations
from ads_api.client.v1.sb.recommendation_types import SBRecommendationTypes
from ads_api.client.v1.sb.recommendations import SBRecommendations
from ads_api.client.v1.sd.ad_groups import SDAdGroups
from ads_api.client.v1.sd.ads import SDAds
from ads_api.client.v1.sd.campaigns import SDCampaigns
from ads_api.client.v1.sd.targets import SDTargets
from ads_api.client.v1.sp.ad_extensions import SPAdExtensions
from ads_api.client.v1.sp.ad_groups import SPAdGroups
from ads_api.client.v1.sp.ads import SPAds
from ads_api.client.v1.sp.campaigns import SPCampaigns
from ads_api.client.v1.sp.targets import SPTargets


class TestCRUDResources:
    def test_sp_campaigns(self) -> None:
        assert hasattr(SPCampaigns, "create_campaign")
        assert hasattr(SPCampaigns, "query_campaign")
        assert hasattr(SPCampaigns, "update_campaign")
        assert hasattr(SPCampaigns, "delete_campaign")

    def test_sp_ad_groups(self) -> None:
        assert hasattr(SPAdGroups, "create_ad_group")
        assert hasattr(SPAdGroups, "query_ad_group")
        assert hasattr(SPAdGroups, "update_ad_group")
        assert hasattr(SPAdGroups, "delete_ad_group")

    def test_sp_ads(self) -> None:
        assert hasattr(SPAds, "create_ad")
        assert hasattr(SPAds, "query_ad")
        assert hasattr(SPAds, "update_ad")
        assert hasattr(SPAds, "delete_ad")

    def test_sp_targets(self) -> None:
        assert hasattr(SPTargets, "create_target")
        assert hasattr(SPTargets, "query_target")
        assert hasattr(SPTargets, "update_target")
        assert hasattr(SPTargets, "delete_target")

    def test_sp_ad_extensions(self) -> None:
        assert hasattr(SPAdExtensions, "create_ad_extension")
        assert hasattr(SPAdExtensions, "query_ad_extension")
        assert hasattr(SPAdExtensions, "update_ad_extension")
        assert not hasattr(SPAdExtensions, "delete_ad_extension")

    def test_sd_campaigns(self) -> None:
        assert hasattr(SDCampaigns, "create_campaign")
        assert hasattr(SDCampaigns, "query_campaign")
        assert hasattr(SDCampaigns, "update_campaign")
        assert hasattr(SDCampaigns, "delete_campaign")

    def test_sd_ad_groups(self) -> None:
        assert hasattr(SDAdGroups, "create_ad_group")
        assert hasattr(SDAdGroups, "query_ad_group")
        assert hasattr(SDAdGroups, "update_ad_group")
        assert hasattr(SDAdGroups, "delete_ad_group")

    def test_sd_ads(self) -> None:
        assert hasattr(SDAds, "create_ad")
        assert hasattr(SDAds, "query_ad")
        assert hasattr(SDAds, "update_ad")
        assert hasattr(SDAds, "delete_ad")

    def test_sd_targets(self) -> None:
        assert hasattr(SDTargets, "create_target")
        assert hasattr(SDTargets, "query_target")
        assert hasattr(SDTargets, "update_target")
        assert hasattr(SDTargets, "delete_target")


class TestPartialResources:
    def test_recommendation_types_query_only(self) -> None:
        assert hasattr(SBRecommendationTypes, "query_recommendation_type")
        assert not hasattr(SBRecommendationTypes, "create_recommendation_type")
        assert not hasattr(SBRecommendationTypes, "update_recommendation_type")
        assert not hasattr(SBRecommendationTypes, "delete_recommendation_type")

    def test_recommendations_create_only(self) -> None:
        assert hasattr(SBRecommendations, "create_recommendation")
        assert not hasattr(SBRecommendations, "query_recommendation")
        assert not hasattr(SBRecommendations, "update_recommendation")
        assert not hasattr(SBRecommendations, "delete_recommendation")

    def test_branded_keywords_pricings_create_only(self) -> None:
        assert hasattr(SBBrandedKeywordsPricings, "create_branded_keywords_pricing")
        assert not hasattr(SBBrandedKeywordsPricings, "query_branded_keywords_pricing")
        assert not hasattr(SBBrandedKeywordsPricings, "update_branded_keywords_pricing")
        assert not hasattr(SBBrandedKeywordsPricings, "delete_branded_keywords_pricing")

    def test_keyword_reservation_validations_create_only(self) -> None:
        assert hasattr(SBKeywordReservationValidations, "create_keyword_reservation_validation")
        assert not hasattr(SBKeywordReservationValidations, "query_keyword_reservation_validation")
        assert not hasattr(SBKeywordReservationValidations, "update_keyword_reservation_validation")
        assert not hasattr(SBKeywordReservationValidations, "delete_keyword_reservation_validation")
