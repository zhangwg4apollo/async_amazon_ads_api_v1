---
title: "Migrating from: spCampaigns"
description: "Migrating from: spCampaigns"
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Migrating from: spCampaigns

## Version 3 Reporting API Example

**`POST /reporting/reports`**

```json
{
  "startDate": "2025-11-03",
  "endDate": "2025-11-10",
  "configuration": {
    "adProduct": "SPONSORED_PRODUCTS",
    "reportTypeId": "spCampaigns",
    "groupBy": [
      "campaign"
    ],
    "columns": [
      "endDate",
      "startDate",
      "addToList",
      "campaignBiddingStrategy",
      "campaignBudgetAmount",
      "campaignBudgetCurrencyCode",
      "campaignBudgetType",
      "campaignId",
      "campaignName",
      "campaignStatus",
      "impressions"
    ],
    "timeUnit": "SUMMARY",
    "format": "CSV"
  }
}
```

## Reporting API v1 Example

**`POST /adsApi/v1/create/reports`**

```json
{
  "accessRequestedAccounts": [
    {
      "advertiserAccountId": "{YOUR_ACCOUNT_ID}"
    }
  ],
  "reports": [
    {
      "format": "CSV",
      "periods": [
        {
          "datePeriod": {
            "startDate": "2025-11-03",
            "endDate": "2025-11-10"
          }
        }
      ],
      "query": {
        "fields": [
          "dateRange.value",
          "metric.addToList",
          "campaign.bidStrategy",
          "campaign.budgetAmount",
          "campaign.currencyCode",
          "campaign.budgetType",
          "campaign.id",
          "campaign.name",
          "campaign.deliveryStatus",
          "metric.impressions"
        ]
      }
    }
  ]
}
```

---

## See also

- [spAdvertisedProduct](guides/reporting/ads-v1/report-types/sp-advertised-product)
- [spPurchasedProduct](guides/reporting/ads-v1/report-types/sp-purchased-product)
- [spSearchTerm](guides/reporting/ads-v1/report-types/sp-search-term)
- [spTargeting](guides/reporting/ads-v1/report-types/sp-targeting)
