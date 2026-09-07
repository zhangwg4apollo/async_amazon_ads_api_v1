---
title: Frequency group (Targeting)
description: Frequency group (Targeting)
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Frequency group (Targeting)

The Frequency group dimension contains 3 fields, listed below:

## Frequency group ID (Primary Key)

- **Reporting Field ID**: `frequencyGroup.id`
- **Data Type**: `STRING`
- **Description**: The unique ID associated with the frequency group. A frequency group helps advertisers set caps on the number of times a unique user is exposed to an ads across multiple orders.
- **Required fields**: N/A
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: `frequencyGroupId`
- **Version 3 Reporting Name (Sponsored Ads)**: N/A

## Frequency group name

- **Reporting Field ID**: `frequencyGroup.name`
- **Data Type**: `STRING`
- **Description**: The user-defined name of the frequency group. A frequency group helps advertisers set caps on the number of times a unique user is exposed to an ad across multiple orders.
- **Required fields**: `frequencyGroup.id` [📎](guides/reporting/ads-v1/dimensions/targeting/frequency-group#frequency-group-id-primary-key)
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: `frequencyGroupName`
- **Version 3 Reporting Name (Sponsored Ads)**: N/A

## Frequency group type

- **Reporting Field ID**: `frequencyGroup.type`
- **Data Type**: `STRING`
- **Description**: The level at which the frequency cap is created, such as- advertiser or manager account
- **Required fields**: `frequencyGroup.id` [📎](guides/reporting/ads-v1/dimensions/targeting/frequency-group#frequency-group-id-primary-key)
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: `frequencyGroupType`
- **Version 3 Reporting Name (Sponsored Ads)**: N/A


## Dimension Compatibility

| Dimension | Compatible |
|-----------|------------|
| [Ad](guides/reporting/ads-v1/dimensions/level-of-detail/ad) | ❌ |
| [Ad group](guides/reporting/ads-v1/dimensions/level-of-detail/ad-group) | ❌ |
| [Target](guides/reporting/ads-v1/dimensions/targeting/target) | ❌ |
| [Ad product](guides/reporting/ads-v1/dimensions/level-of-detail/ad-product) | ✅ |
| [Advertised product](guides/reporting/ads-v1/dimensions/product/advertised-product) | ❌ |
| [Advertised product marketplace](guides/reporting/ads-v1/dimensions/product/advertised-product-marketplace) | ❌ |
| [Advertised product SKU](guides/reporting/ads-v1/dimensions/product/advertised-product-sku) | ❌ |
| [Advertiser account](guides/reporting/ads-v1/dimensions/level-of-detail/advertiser-account) | ✅ |
| [Audience segment](guides/reporting/ads-v1/dimensions/audience/audience-segment) | ❌ |
| [Audience segment targeting status](guides/reporting/ads-v1/dimensions/audience/audience-segment-targeting-status) | ❌ |
| [Brand suitability content exclusion category](guides/reporting/ads-v1/dimensions/supply/brand-suitability-content-exclusion-category) | ❌ |
| [Brand suitability inventory tier](guides/reporting/ads-v1/dimensions/supply/brand-suitability-inventory-tier) | ❌ |
| [Browser name](guides/reporting/ads-v1/dimensions/technology/browser-name) | ❌ |
| [Browser version](guides/reporting/ads-v1/dimensions/technology/browser-version) | ❌ |
| [Budget currency](guides/reporting/ads-v1/dimensions/currency/budget-currency) | ❌ |
| [Campaign](guides/reporting/ads-v1/dimensions/level-of-detail/campaign) | ❌ |
| [City](guides/reporting/ads-v1/dimensions/geography/city) | ❌ |
| [Content creator](guides/reporting/ads-v1/dimensions/supply/content-creator) | ❌ |
| [Content genre](guides/reporting/ads-v1/dimensions/supply/content-genre) | ❌ |
| [Content rating](guides/reporting/ads-v1/dimensions/supply/content-rating) | ❌ |
| [Content title](guides/reporting/ads-v1/dimensions/supply/content-title) | ❌ |
| [Content type](guides/reporting/ads-v1/dimensions/supply/content-type) | ❌ |
| [Conversion source](guides/reporting/ads-v1/dimensions/conversion/conversion-source) | ❌ |
| [Conversion source attribution type](guides/reporting/ads-v1/dimensions/conversion/conversion-source-attribution-type) | ❌ |
| [Conversion source environment](guides/reporting/ads-v1/dimensions/conversion/conversion-source-environment) | ❌ |
| [Converted currency](guides/reporting/ads-v1/dimensions/currency/converted-currency) | ✅ |
| [Converted product](guides/reporting/ads-v1/dimensions/product/converted-product) | ❌ |
| [Converted product marketplace](guides/reporting/ads-v1/dimensions/product/converted-product-marketplace) | ❌ |
| [Country](guides/reporting/ads-v1/dimensions/geography/country) | ❌ |
| [Date](guides/reporting/ads-v1/dimensions/time/date) | ✅ |
| [Date range](guides/reporting/ads-v1/dimensions/time/date-range) | ✅ |
| [Day of month](guides/reporting/ads-v1/dimensions/time/day-of-month) | ✅ |
| [Day of week](guides/reporting/ads-v1/dimensions/time/day-of-week) | ✅ |
| [Deal](guides/reporting/ads-v1/dimensions/supply/deal) | ❌ |
| [Device type](guides/reporting/ads-v1/dimensions/technology/device-type) | ❌ |
| [DMA](guides/reporting/ads-v1/dimensions/geography/dma) | ❌ |
| [Environment](guides/reporting/ads-v1/dimensions/technology/environment) | ❌ |
| [Flight](guides/reporting/ads-v1/dimensions/level-of-detail/flight) | ❌ |
| [Hour](guides/reporting/ads-v1/dimensions/time/hour) | ❌ |
| [Insertion order](guides/reporting/ads-v1/dimensions/level-of-detail/insertion-order) | ❌ |
| [Live event](guides/reporting/ads-v1/dimensions/supply/live-event) | ❌ |
| [Live event ad break](guides/reporting/ads-v1/dimensions/supply/live-event-ad-break) | ❌ |
| [Live event ad slot](guides/reporting/ads-v1/dimensions/supply/live-event-ad-slot) | ❌ |
| [Live event inventory type](guides/reporting/ads-v1/dimensions/supply/live-event-inventory-type) | ❌ |
| [Live event property](guides/reporting/ads-v1/dimensions/supply/live-event-property) | ❌ |
| [Matched target](guides/reporting/ads-v1/dimensions/targeting/matched-target) | ❌ |
| [Month](guides/reporting/ads-v1/dimensions/time/month) | ✅ |
| [Conversion definition (off-Amazon)](guides/reporting/ads-v1/dimensions/conversion/conversion-definition-off-amazon) | ❌ |
| [Conversion type (off-Amazon)](guides/reporting/ads-v1/dimensions/conversion/conversion-type-off-amazon) | ❌ |
| [Operating system](guides/reporting/ads-v1/dimensions/technology/operating-system) | ❌ |
| [Placement](guides/reporting/ads-v1/dimensions/supply/placement) | ❌ |
| [Placement classification](guides/reporting/ads-v1/dimensions/supply/placement-classification) | ❌ |
| [Placement size](guides/reporting/ads-v1/dimensions/supply/placement-size) | ❌ |
| [Portfolio](guides/reporting/ads-v1/dimensions/level-of-detail/portfolio) | ❌ |
| [Postal code](guides/reporting/ads-v1/dimensions/geography/postal-code) | ❌ |
| [Product relevance](guides/reporting/ads-v1/dimensions/product/product-relevance) | ❌ |
| [Region](guides/reporting/ads-v1/dimensions/geography/region) | ❌ |
| [Search term](guides/reporting/ads-v1/dimensions/targeting/search-term) | ❌ |
| [Site or app](guides/reporting/ads-v1/dimensions/supply/site-or-app) | ❌ |
| [Supply source](guides/reporting/ads-v1/dimensions/supply/supply-source) | ❌ |
| [Targeting](guides/reporting/ads-v1/dimensions/targeting/targeting) | ❌ |
| [Targeting match type](guides/reporting/ads-v1/dimensions/targeting/targeting-match-type) | ❌ |
| [Week](guides/reporting/ads-v1/dimensions/time/week) | ✅ |
| [Year](guides/reporting/ads-v1/dimensions/time/year) | ✅ |


## Compatible metrics

- `metric.averageUserImpressionFrequency` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#average-user-impression-frequency)
- `metric.userFrequency1` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-1)
- `metric.userFrequency10Plus` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-10)
- `metric.userFrequency2` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-2)
- `metric.userFrequency3` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-3)
- `metric.userFrequency4` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-4)
- `metric.userFrequency5` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-5)
- `metric.userFrequency6` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-6)
- `metric.userFrequency7` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-7)
- `metric.userFrequency8` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-8)
- `metric.userFrequency9` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-frequency-9)
- `metric.userReach` [📎](guides/reporting/ads-v1/metrics/reach/user-reach#user-reach)


---

## See also

- [Target](guides/reporting/ads-v1/dimensions/targeting/target)
- [Targeting](guides/reporting/ads-v1/dimensions/targeting/targeting)
- [Targeting match type](guides/reporting/ads-v1/dimensions/targeting/targeting-match-type)
- [Search term](guides/reporting/ads-v1/dimensions/targeting/search-term)
- [Matched target](guides/reporting/ads-v1/dimensions/targeting/matched-target)
