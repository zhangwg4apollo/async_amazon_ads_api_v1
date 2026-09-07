---
title: Getting started with the Reporting v1 API
description: Getting started with the Reporting v1 API
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Building Queries

The new reporting API provides much greater flexibility and freedom. This section provides example create report requests to demonstrate different use-cases and help you understand how they change the request shape. For brevity, the related headers and URL are not included. For a full account of how these APIs function, check the [OpenAPI specification](api-spec-v1-reports-BETA).


> [TIP] Did you know that you can generate an SDK directly from our OpenAPI specifications? [Get started now](guides/get-started/generate-sdk) to simplify your integration and avoid building JSON requests manually.

## Simple Report for a Single Account

This is a baseline example for a single account, simple dimensions, and a few metrics.

* Dimensions: `date`, `campaign`
* Accounts: single account
* Filter: N/A

```json
{
  "reports": [
    {
      "format": "GZIP_JSON",
      "periods": [
        {
          "datePeriod": {
            "startDate": "2025-02-01",
            "endDate": "2025-04-30"
          }
        }
      ],
      "query": {
        "fields": [
            "date.value",
            "campaign.id",
            "campaign.name",
            "metric.clicks",
            "metric.impressions",
            "metric.roas"
            ]
      }
    }
  ],
  "accessRequestedAccounts": [
    {
      "advertiserAccountId": "{YOUR_ACCOUNT_ID}"
    }
  ]
}
```

## Simple Report for Multiple Accounts

This is an extended example for multiple account types, simple dimensions, and a few metrics.

* Dimensions: `date`, `campaign`
* Accounts: multiple accounts
* Filter: N/A

```json
{
  "reports": [
    {
      "format": "GZIP_JSON",
      "periods": [
        {
          "datePeriod": {
            "startDate": "2025-02-01",
            "endDate": "2025-04-30"
          }
        }
      ],
      "query": {
        "fields": [
            "date.value",
            "campaign.id",
            "campaign.name",
            "metric.clicks",
            "metric.impressions",
            "metric.roas"
            ]
      }
    }
  ],
  "accessRequestedAccounts": [
    {
      "advertiserAccountId": "{YOUR_ACCOUNT_ID}"
    },
    {
      "managerAccountId": "{YOUR_MANAGER_ACCOUNT_ID}"
    }
  ]
}
```

## Multi-Dimensional Report

This is an example of a previously impossible scenario - reporting across multiple dimension categories.

* Dimensions: `date`, `adGroup`, `city`, `deviceType`
* Accounts: single account
* Filter: N/A

```json
{
  "reports": [
    {
      "format": "GZIP_JSON",
      "periods": [
        {
          "datePeriod": {
            "startDate": "2025-02-01",
            "endDate": "2025-04-30"
          }
        }
      ],
      "query": {
        "fields": [
            "date.value",
            "adGroup.id",
            "adGroup.name",
            "city.name",
            "deviceType.value",
            "metric.clicks",
            "metric.impressions",
            "metric.roas"
         ]
      }
    }
  ],
  "accessRequestedAccounts": [
    {
      "advertiserAccountId": "{YOUR_ACCOUNT_ID}"
    }
  ]
}
```

## Ad Product Filtered Report

By default, the new reporting API will include data from all ad products. This is an example of using filters to pull data on behalf of a specific ad product.

* Dimensions: `date`, `adGroup`, `city`, `deviceType`
* Accounts: single account
* Filter: one ad product

```json
{
  "reports": [
    {
      "format": "GZIP_JSON",
      "periods": [
        {
          "datePeriod": {
            "startDate": "2025-02-01",
            "endDate": "2025-04-30"
          }
        }
      ],
      "query": {
        "fields": [
            "date.value",
            "adGroup.id",
            "adGroup.name",
            "city.name",
            "deviceType.value",
            "metric.clicks",
            "metric.impressions",
            "metric.roas"
         ],
         "filter": {
           "on": {
             "field": "adProduct.value",
             "comparisonOperator": "EQUALS",
             "not": false,
             "values": ["`SPONSORED_BRANDS`"]
           }
         }
      }
    }
  ],
  "accessRequestedAccounts": [
    {
      "advertiserAccountId": "{YOUR_ACCOUNT_ID}"
    }
  ]
}
```

## Campaign ID Filtered Report

By default, the new reporting API will include data from all of your campaigns. This is an example of using filters to pull data on behalf of specific campaigns.

* Dimensions: `date`, `adGroup`, `city`, `deviceType`
* Accounts: single account
* Filter: two campaigns

```json
{
  "reports": [
    {
      "format": "GZIP_JSON",
      "periods": [
        {
          "datePeriod": {
            "startDate": "2025-02-01",
            "endDate": "2025-04-30"
          }
        }
      ],
      "query": {
        "fields": [
            "date.value",
            "adGroup.id",
            "adGroup.name",
            "city.name",
            "deviceType.value",
            "metric.clicks",
            "metric.impressions",
            "metric.roas"
         ],
         "filter": {
           "on": {
             "field": "campaign.id",
             "comparisonOperator": "IN",
             "not": false,
             "values": ["{YOUR_FIRST_CAMPAIGN_ID}", "{YOUR_SECOND_CAMPAIGN_ID}"]
           }
         }
      }
    }
  ],
  "accessRequestedAccounts": [
    {
      "advertiserAccountId": "{YOUR_ACCOUNT_ID}"
    }
  ]
}
```
