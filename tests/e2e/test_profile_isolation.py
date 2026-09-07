from __future__ import annotations

import pytest

from ads_api import AdsClient, AmazonAdsConfig, Region
from ads_api.models.v1.campaigns.sp import SPCampaignMultiStatusResponse, SPCampaignSuccessResponse

from .config import E2ESettings
from .helpers import campaign_create_request, campaign_delete_request, campaign_query_request


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
async def test_sp_campaigns_are_isolated_by_profile_scope(
    e2e_settings: E2ESettings,
    unique_name: str,
) -> None:
    owner_config = _config_for_profile(e2e_settings, e2e_settings.profile_id)
    other_config = _config_for_profile(e2e_settings, e2e_settings.other_profile_id)

    async with AdsClient(owner_config) as owner_client:
        create_result = await owner_client.v1.sp.campaigns.create_campaign(
            campaign_create_request(unique_name, e2e_settings.marketplace),
            mode="pydantic",
        )
        assert isinstance(create_result, SPCampaignMultiStatusResponse)
        assert create_result.error == []
        assert create_result.success is not None
        campaign_id = create_result.success[0].campaign.campaignId

        owner_query = await owner_client.v1.sp.campaigns.query_campaign(
            campaign_query_request(campaign_id, state="ENABLED"),
            mode="pydantic",
        )
        assert isinstance(owner_query, SPCampaignSuccessResponse)
        assert owner_query.campaigns is not None
        assert [item.campaignId for item in owner_query.campaigns] == [campaign_id]

        try:
            async with AdsClient(other_config) as other_client:
                other_query = await other_client.v1.sp.campaigns.query_campaign(
                    campaign_query_request(campaign_id, state="ENABLED"),
                    mode="pydantic",
                )
            assert isinstance(other_query, SPCampaignSuccessResponse)
            assert other_query.campaigns == []
        finally:
            await owner_client.v1.sp.campaigns.delete_campaign(
                campaign_delete_request(campaign_id),
                mode="pydantic",
            )
