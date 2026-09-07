---
title: New features
description: New features
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# New features

## Expanded file formats

In the new Reporting API, report formats have been expanded to support partitioned files, providing the ability to generate and work with much larger reports. Simply specify your `format` as either `PARTITIONED_GZIP_JSON` or `PARTITIONED_CSV`, and when the report is generated, it will be split up into multiple files. Currently, reports are split into up-to 1GB (uncompressed) chunks. Each of the partition files will be available in the `completedReportParts` property when you retrieve your report:

```json
{
  "error": null,
  "success": [
    {
      "index": 0,
      "report": {
        "completedDateTime": "2025-11-05T00:12:50.443Z",
        "completedReportParts": [
          {
            "sizeInBytes": 102400000,
            "url": "{PART_1_PRESIGNED_S3_URL}",
            "urlExpirationDateTime": "2025-11-05T00:14:50.443Z"
          },
          {
            "sizeInBytes": 5120000,
            "url": "{PART_2_PRESIGNED_S3_URL}",
            "urlExpirationDateTime": "2025-11-05T00:14:50.443Z"
          }
        ],
        "creationDateTime": "2025-11-05T00:00:38.285Z",
        "format": "CSV",
        "lastUpdatedDateTime": "2025-11-05T00:00:38.285Z",
        "periods": [
          {
            "datePeriod": {
              "startDate": "2025-10-28",
              "endDate": "2025-11-04"
            }
          }
        ],
        "query": {
          "fields": [
            "dateRange.value",
            "metric.addToList",
            "budgetCurrency.value",
            "campaign.bidStrategy",
            "campaign.budgetAmount",
            "campaign.budgetType",
            "campaign.id",
            "campaign.name",
            "campaign.deliveryStatus",
            "metric.impressions"
          ]
        },
        "reportId": "{YOUR_REPORT_ID}",
        "status": "COMPLETED"
      }
    }
  ]
}
```

## Metric currency conversion

When working with global accounts, it is common for you to have sales and spend data for multiple budget currencies. In this situation, you cannot sum up currency related fields (e.g. `metric.sales`) to view top-level performance. The new reporting API allows you to convert any currency related metric field into a common currency, providing you the ability to see global account performance in aggregate.

To use currency conversion, you need to:

1. Assign the `currencyOfView` setting to your desired currency code from the ISO 4217 standard (e.g. `CAD`)
2. Include the `convertedCurrency.value` dimension
3. Include any converted metric fields you desire (e.g. `metric.salesConverted`, `metric.totalCostConverted`)

```json
{
  "error": null,
  "success": [
    {
      "index": 0,
      "report": {
        "creationDateTime": "2025-11-05T00:00:38.285Z",
        "format": "CSV",
        "currencyOfView": "CAD",
        "lastUpdatedDateTime": "2025-11-05T00:00:38.285Z",
        "periods": [
          {
            "datePeriod": {
              "startDate": "2025-10-28",
              "endDate": "2025-11-04"
            }
          }
        ],
        "query": {
          "fields": [
            "dateRange.value",
            "advertiserAccount.id",
            "advertiserAccount.name",
            "convertedCurrency.value",
            "metric.salesConverted"
          ]
        },
        "reportId": "{YOUR_REPORT_ID}",
        "status": "PENDING"
      }
    }
  ]
}
```

The resulting report will use daily currency rate tables to convert from your original currency into your desired output currency while also including the specified output currency in the `convertedCurrency.value` column. See the [API specification](api-spec-v1-reports-BETA) for a complete list of the supported currencies.

> [TIP] When using currency conversion, you must include the converted variants of metric fields. All converted variants end with `Converted`, and they all require the `convertedCurrency.value` dimension. Visit our [metrics library](guides/reporting/ads-v1/metrics/library) to see all converted metrics.
