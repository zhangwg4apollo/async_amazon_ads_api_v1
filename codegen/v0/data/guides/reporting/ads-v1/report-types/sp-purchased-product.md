---
title: "Migrating from: spPurchasedProduct"
description: "Migrating from: spPurchasedProduct"
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Migrating from: spPurchasedProduct

## Version 3 Reporting API Example

**`POST /reporting/reports`**

```json
{
  "startDate": "2025-11-03",
  "endDate": "2025-11-10",
  "configuration": {
    "adProduct": "SPONSORED_PRODUCTS",
    "reportTypeId": "spPurchasedProduct",
    "groupBy": [
      "asin"
    ],
    "columns": [
      "endDate",
      "startDate",
      "adGroupId",
      "adGroupName",
      "addToList",
      "advertisedAsin",
      "advertisedSku",
      "campaignBudgetCurrencyCode",
      "campaignId",
      "campaignName",
      "keyword",
      "matchType",
      "portfolioId",
      "purchasedAsin",
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
          "advertisedProduct.id",
          "advertisedProduct.sku",
          "campaign.currencyCode",
          "campaign.id",
          "campaign.name",
          "target.value",
          "target.matchType",
          "portfolio.portfolioId",
          "convertedProduct.id",
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
- [spSearchTerm](guides/reporting/ads-v1/report-types/sp-search-term)
- [spTargeting](guides/reporting/ads-v1/report-types/sp-targeting)
