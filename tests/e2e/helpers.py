from __future__ import annotations

from ads_api.models.v1.ad_groups.sp import SPAdGroupCreate, SPCreateAdGroupBid, SPCreateAdGroupRequest
from ads_api.models.v1.campaigns.sp import (
    SPCampaignCreate,
    SPCampaignUpdate,
    SPCreateAutoCreationSettings,
    SPCreateBudget,
    SPCreateBudgetValue,
    SPCreateCampaignRequest,
    SPCreateMonetaryBudget,
    SPCreateMonetaryBudgetValue,
    SPDeleteCampaignRequest,
    SPQueryCampaignRequest,
    SPUpdateCampaignRequest,
)


def campaign_create_request(name: str, marketplace: str) -> SPCreateCampaignRequest:
    return SPCreateCampaignRequest(
        campaigns=[
            SPCampaignCreate(
                adProduct="SPONSORED_PRODUCTS",
                autoCreationSettings=SPCreateAutoCreationSettings(autoCreateTargets=False),
                budgets=[
                    SPCreateBudget(
                        budgetType="MONETARY",
                        budgetValue=SPCreateBudgetValue(
                            monetaryBudgetValue=SPCreateMonetaryBudgetValue(
                                monetaryBudget=SPCreateMonetaryBudget(value=10.0),
                            ),
                        ),
                        recurrenceTimePeriod="DAILY",
                    ),
                ],
                marketplaceScope="SINGLE_MARKETPLACE",
                marketplaces=[marketplace],  # type: ignore[list-item]
                name=name,
                startDateTime="2026-06-09T00:00:00Z",
                state="ENABLED",
            )
        ]
    )


def campaign_query_request(campaign_id: str, *, state: str | None = None) -> SPQueryCampaignRequest:
    body: dict[str, object] = {
        "adProductFilter": {"include": ["SPONSORED_PRODUCTS"]},
        "campaignIdFilter": {"include": [campaign_id]},
    }
    if state is not None:
        body["stateFilter"] = {"include": [state]}
    return SPQueryCampaignRequest.model_validate(body)


def campaign_update_request(campaign_id: str, name: str) -> SPUpdateCampaignRequest:
    return SPUpdateCampaignRequest(campaigns=[SPCampaignUpdate(campaignId=campaign_id, name=name)])


def campaign_delete_request(campaign_id: str) -> SPDeleteCampaignRequest:
    return SPDeleteCampaignRequest(campaignIds=[campaign_id])


def ad_group_create_request(name: str, campaign_id: str) -> SPCreateAdGroupRequest:
    return SPCreateAdGroupRequest(
        adGroups=[
            SPAdGroupCreate(
                adProduct="SPONSORED_PRODUCTS",
                bid=SPCreateAdGroupBid(defaultBid=1.0),
                campaignId=campaign_id,
                name=name,
                state="ENABLED",
            )
        ]
    )
