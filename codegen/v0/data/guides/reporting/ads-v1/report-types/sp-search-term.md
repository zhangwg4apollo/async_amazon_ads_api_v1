---
title: "Migrating from: spSearchTerm"
description: "Migrating from: spSearchTerm"
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Migrating from: spSearchTerm

## Version 3 Reporting API Example

**`POST /reporting/reports`**

```json
{
  "startDate": "2025-11-03",
  "endDate": "2025-11-10",
  "configuration": {
    "adProduct": "SPONSORED_PRODUCTS",
    "reportTypeId": "spSearchTerm",
    "groupBy": [
      "searchTerm"
    ],
    "columns": [
      "endDate",
      "startDate",
      "adGroupId",
      "adGroupName",
      "addToList",
      "campaignBudgetAmount",
      "campaignBudgetCurrencyCode",
      "campaignBudgetType",
      "campaignId",
      "campaignName",
      "campaignStatus",
      "impressions",
      "keyword",
      "matchType",
      "portfolioId",
      "searchTerm",
      "targeting"
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
          "adGroup.id",
          "adGroup.name",
          "metric.addToList",
          "campaign.budgetAmount",
          "campaign.currencyCode",
          "campaign.budgetType",
          "campaign.id",
          "campaign.name",
          "campaign.deliveryStatus",
          "metric.impressions",
          "target.value",
          "target.matchType",
          "portfolio.portfolioId",
          "searchTerm.value",
          "target.value"
        ]
      }
    }
  ]
}
```

---

## See also

- [spAdvertisedProduct](guides/reporting/ads-v1/report-types/sp-advertised-product)
- [spCampaigns](guides/reporting/ads-v1/report-types/sp-campaigns)
- [spPurchasedProduct](guides/reporting/ads-v1/report-types/sp-purchased-product)
- [spTargeting](guides/reporting/ads-v1/report-types/sp-targeting)
