---
title: Conversion definition (off-Amazon) (Conversion)
description: Conversion definition (off-Amazon) (Conversion)
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Conversion definition (off-Amazon) (Conversion)

The Conversion definition (off-Amazon) dimension contains 1 field, listed below:

## Conversion definition (off-Amazon) (Primary Key)

- **Reporting Field ID**: `offAmazonConversionDefinition.value`
- **Data Type**: `STRING`
- **Description**: The name of a custom conversion definition created by an advertiser within a broader conversion type. Conversion definitions let advertisers label and track conversion goals that matter to their business.
- **Required fields**: `conversionSourceEnvironment.value` [📎](guides/reporting/ads-v1/dimensions/conversion/conversion-source-environment#conversion-source-environment-primary-key), `offAmazonConversionType.value` [📎](guides/reporting/ads-v1/dimensions/conversion/conversion-type-off-amazon#conversion-type-off-amazon-primary-key)
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: N/A
- **Version 3 Reporting Name (Sponsored Ads)**: N/A


## Dimension Compatibility

| Dimension | Compatible |
|-----------|------------|
| [Ad](guides/reporting/ads-v1/dimensions/level-of-detail/ad) | ✅ |
| [Ad group](guides/reporting/ads-v1/dimensions/level-of-detail/ad-group) | ✅ |
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
| [Budget currency](guides/reporting/ads-v1/dimensions/currency/budget-currency) | ✅ |
| [Campaign](guides/reporting/ads-v1/dimensions/level-of-detail/campaign) | ✅ |
| [City](guides/reporting/ads-v1/dimensions/geography/city) | ❌ |
| [Content creator](guides/reporting/ads-v1/dimensions/supply/content-creator) | ❌ |
| [Content genre](guides/reporting/ads-v1/dimensions/supply/content-genre) | ❌ |
| [Content rating](guides/reporting/ads-v1/dimensions/supply/content-rating) | ❌ |
| [Content title](guides/reporting/ads-v1/dimensions/supply/content-title) | ❌ |
| [Content type](guides/reporting/ads-v1/dimensions/supply/content-type) | ❌ |
| [Conversion source](guides/reporting/ads-v1/dimensions/conversion/conversion-source) | ✅ |
| [Conversion source attribution type](guides/reporting/ads-v1/dimensions/conversion/conversion-source-attribution-type) | ✅ |
| [Conversion source environment](guides/reporting/ads-v1/dimensions/conversion/conversion-source-environment) | ✅ |
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
| [Frequency group](guides/reporting/ads-v1/dimensions/targeting/frequency-group) | ❌ |
| [Hour](guides/reporting/ads-v1/dimensions/time/hour) | ❌ |
| [Insertion order](guides/reporting/ads-v1/dimensions/level-of-detail/insertion-order) | ✅ |
| [Live event](guides/reporting/ads-v1/dimensions/supply/live-event) | ❌ |
| [Live event ad break](guides/reporting/ads-v1/dimensions/supply/live-event-ad-break) | ❌ |
| [Live event ad slot](guides/reporting/ads-v1/dimensions/supply/live-event-ad-slot) | ❌ |
| [Live event inventory type](guides/reporting/ads-v1/dimensions/supply/live-event-inventory-type) | ❌ |
| [Live event property](guides/reporting/ads-v1/dimensions/supply/live-event-property) | ❌ |
| [Matched target](guides/reporting/ads-v1/dimensions/targeting/matched-target) | ❌ |
| [Month](guides/reporting/ads-v1/dimensions/time/month) | ✅ |
| [Conversion type (off-Amazon)](guides/reporting/ads-v1/dimensions/conversion/conversion-type-off-amazon) | ✅ |
| [Operating system](guides/reporting/ads-v1/dimensions/technology/operating-system) | ❌ |
| [Placement](guides/reporting/ads-v1/dimensions/supply/placement) | ❌ |
| [Placement classification](guides/reporting/ads-v1/dimensions/supply/placement-classification) | ❌ |
| [Placement size](guides/reporting/ads-v1/dimensions/supply/placement-size) | ❌ |
| [Portfolio](guides/reporting/ads-v1/dimensions/level-of-detail/portfolio) | ✅ |
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

- `metric.offAmazonConversions` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-off-amazon)
- `metric.offAmazonConversionsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-from-clicks-off-amazon)
- `metric.offAmazonConversionsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-from-views-off-amazon)
- `metric.offAmazonConversionsOptimized` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-off-amazon-optimized)
- `metric.offAmazonConversionsValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-value-average-off-amazon)
- `metric.offAmazonConversionsValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-value-sum-off-amazon)
- `metric.offAmazonConversionsValueSumOptimized` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-value-sum-off-amazon-optimized)
- `metric.offAmazonSales` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#sales-off-amazon)
- `metric.offAmazonSalesConverted` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#sales-off-amazon-converted)
- `metric.offAmazonSalesFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#sales-from-clicks-off-amazon)
- `metric.offAmazonSalesFromClicksConverted` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#sales-from-clicks-off-amazon-converted)
- `metric.offAmazonSalesFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#sales-from-views-off-amazon)
- `metric.offAmazonSalesFromViewsConverted` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#sales-from-views-off-amazon-converted)
- `metric.offAmazonSalesOptimized` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#sales-off-amazon-optimized)
- `metric.offAmazonSalesOptimizedConverted` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#sales-off-amazon-optimized-converted)
- `metric.offAmazonUnitsSold` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#units-sold-off-amazon)
- `metric.offAmazonUnitsSoldFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#units-sold-from-clicks-off-amazon)
- `metric.offAmazonUnitsSoldFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#units-sold-from-views-off-amazon)


---

## See also

- [Conversion source](guides/reporting/ads-v1/dimensions/conversion/conversion-source)
- [Conversion type (off-Amazon)](guides/reporting/ads-v1/dimensions/conversion/conversion-type-off-amazon)
- [Conversion source environment](guides/reporting/ads-v1/dimensions/conversion/conversion-source-environment)
- [Conversion source attribution type](guides/reporting/ads-v1/dimensions/conversion/conversion-source-attribution-type)
