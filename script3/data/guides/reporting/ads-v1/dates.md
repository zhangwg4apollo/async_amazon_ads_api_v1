---
title: Dates and historical data retention
description: Dates and historical data retention
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Dates and historical data retention

## Measurement and aggregation dates

The new reporting API provides the ability to include multiple accounts from various different countries and timezones. By default, performance is measured and data is aggregated based on each campaign timezone, which can also be included in the report via the `timeZone.value` dimension field.

So, when you generate a report that includes `date.value`, `campaign.id`, `timeZone.value`, and `metric.impressions`, the metric totals for each row will be based on the relative 24-hour period:

| `date.value` | `campaign.id` | `timeZone.value` | `metric.impressions` | Effective 24-hour period                 |
|-------------|----------------|----------------|--------------------|------------------------------------------|
| 11/5/2025   | `{CAMPAIGN_1}`   | EST            | 100                | 2025-11-05 05:00 Z → 2025-11-06 04:59 Z  |
| 11/5/2025   | `{CAMPAIGN_2}`   | GMT            | 200                | 2025-11-05 00:00 Z → 2025-11-05 23:59 Z  |
| 11/5/2025   | `{CAMPAIGN_3}`   | CET            | 300                | 2025-11-04 23:00 Z → 2025-11-05 22:59 Z  |
| 11/5/2025   | `{CAMPAIGN_4}`   | JST            | 400                | 2025-11-04 15:00 Z → 2025-11-05 14:59 Z  |

Future releases will include support for UTC time zone normalization, enabling aggregation across a common 24-hour period.

## Date Periods

As mentioned above, the new reporting API uses campaign timezone for data aggregation. When you specify date periods, it uses the same methodology. In the example below, you would be requesting data from `2025-06-13` to `2025-06-19` in the relevant campaign timezones:

```json
{
  "periods": [
    {
      "datePeriod": {
        "startDate": "2025-06-13",
        "endDate": "2025-06-19"
      }
    }
  ]
}
```

> [NOTE] This period is inclusive, and it controls the amount of historical data that will be returned. Extending this period increases the amount of data scanned, and in some cases, also increases the size of the report. It is an important element to consider to avoid report failures or throttling.

## Historical Data Retention

Another element to consider is data retention. As part of the Ads API v1 Reporting release, reporting data retention periods are being extended to provide deeper insights:

| Time Dimension   | Data Retention | Max Report Date Range |
|------------------|----------------|-----------------------|
| `hour.value`       | 14 days        | 14 days               |
| `date.value`       | 24 months      | 120 days              |
| `week.value`       | 24 months      | 15 months             |
| `day.value`        | 24 months      | 15 months             |
| `dayOfWeek.value`  | 24 months      | 15 months             |
| `month.value`      | 6 years        | 25 months             |
| `year.value`       | 6 years        | 6 years               |
| `dateRange.value`  | 6 years        | 6 years               |

It is important to note that despite having extended access to historical data, combining extensive look backs with a large number of dimensions and metrics and a wide date range can result in the report generation failing due to the size of the expected report. It is recommended to limit the date range for reports, even when accessing extensive historical data.
