from __future__ import annotations

import pytest

from ads_api import AdsClient, AmazonAdsConfig, Region
from ads_api.models.v1.ad_groups.sp import SPAdGroupMultiStatusResponse
from ads_api.models.v1.campaigns.sp import SPCampaignMultiStatusResponse

from .config import E2ESettings
from .helpers import ad_group_create_request, campaign_create_request, campaign_delete_request


def _config_for_profile(e2e_settings: E2ESettings, profile_id: str) -> AmazonAdsConfig:
    return AmazonAdsConfig(
        client_id=e2e_settings.client_id,
        client_secret=e2e_settings.client_secret,
        refresh_token=e2e_settings.refresh_token,
        profile_id=profile_id,
        region=Region.NA,
        endpoints={"na": e2e_settings.base_url},
        token_url=e2e_settings.token_url,
        timeout=e2e_settings.timeout,
    )


@pytest.mark.asyncio
async def test_sp_ad_groups_require_campaign_in_same_profile(
    e2e_settings: E2ESettings,
    unique_name: str,
) -> None:
    owner_config = _config_for_profile(e2e_settings, e2e_settings.profile_id)
    other_config = _config_for_profile(e2e_settings, e2e_settings.other_profile_id)

    async with AdsClient(owner_config) as owner_client:
        missing_parent = await owner_client.v1.sp.ad_groups.create_ad_group(
            ad_group_create_request(f"{unique_name}-missing-parent", "missing-campaign"),
            mode="pydantic",
        )
        assert isinstance(missing_parent, SPAdGroupMultiStatusResponse)
        assert missing_parent.success == []
        assert missing_parent.error is not None
        assert missing_parent.error[0].index == 0
        assert missing_parent.error[0].errors[0].code == "RESOURCE_DOES_NOT_BELONG_TO_PARENT"

        campaign_result = await owner_client.v1.sp.campaigns.create_campaign(
            campaign_create_request(f"{unique_name}-parent", e2e_settings.marketplace),
            mode="pydantic",
        )
        assert isinstance(campaign_result, SPCampaignMultiStatusResponse)
        assert campaign_result.error == []
        assert campaign_result.success is not None
        campaign_id = campaign_result.success[0].campaign.campaignId

        try:
            async with AdsClient(other_config) as other_client:
                cross_profile = await other_client.v1.sp.ad_groups.create_ad_group(
                    ad_group_create_request(f"{unique_name}-cross-profile", campaign_id),
                    mode="pydantic",
                )
            assert isinstance(cross_profile, SPAdGroupMultiStatusResponse)
            assert cross_profile.success == []
            assert cross_profile.error is not None
            assert cross_profile.error[0].index == 0
            assert cross_profile.error[0].errors[0].code == "RESOURCE_DOES_NOT_BELONG_TO_PARENT"

            same_profile = await owner_client.v1.sp.ad_groups.create_ad_group(
                ad_group_create_request(f"{unique_name}-same-profile", campaign_id),
                mode="pydantic",
            )
            assert isinstance(same_profile, SPAdGroupMultiStatusResponse)
            assert same_profile.error == []
            assert same_profile.success is not None
            ad_group = same_profile.success[0].adGroup
            assert ad_group.campaignId == campaign_id
            assert ad_group.adProduct == "SPONSORED_PRODUCTS"
            assert ad_group.bid.currencyCode == e2e_settings.expected_currency_code
        finally:
            await owner_client.v1.sp.campaigns.delete_campaign(
                campaign_delete_request(campaign_id),
                mode="pydantic",
            )
