---
title: "Migrating from: spAdvertisedProduct"
description: "Migrating from: spAdvertisedProduct"
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Migrating from: spAdvertisedProduct

## Version 3 Reporting API Example

`POST /reporting/reports`

```json
{
  "startDate": "2025-11-03",
  "endDate": "2025-11-10",
  "configuration": {
    "adProduct": "SPONSORED_PRODUCTS",
    "reportTypeId": "spAdvertisedProduct",
    "groupBy": [
      "advertiser"
    ],
    "columns": [
      "endDate",
      "startDate",
      "adGroupId",
      "adGroupName",
      "adId",
      "addToList",
      "advertisedAsin",
      "advertisedSku",
      "campaignBudgetAmount",
      "campaignBudgetCurrencyCode",
      "campaignBudgetType",
      "campaignId",
      "campaignName",
      "campaignStatus",
      "impressions",
      "portfolioId"
    ],
    "timeUnit": "SUMMARY",
    "format": "CSV"
  }
}
```

## Reporting API v1 Example

`POST /adsApi/v1/create/reports`

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
          "ad.id",
          "metric.addToList",
          "advertisedProduct.id",
          "advertisedProduct.sku",
          "campaign.budgetAmount",
          "campaign.currencyCode",
          "campaign.budgetType",
          "campaign.id",
          "campaign.name",
          "campaign.deliveryStatus",
          "metric.impressions",
          "portfolio.portfolioId"
        ]
      }
    }
  ]
}
```

---

## See also

- [spCampaigns](guides/reporting/ads-v1/report-types/sp-campaigns)
- [spPurchasedProduct](guides/reporting/ads-v1/report-types/sp-purchased-product)
- [spSearchTerm](guides/reporting/ads-v1/report-types/sp-search-term)
- [spTargeting](guides/reporting/ads-v1/report-types/sp-targeting)
