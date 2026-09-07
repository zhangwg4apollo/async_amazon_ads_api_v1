---
title: Audience segment (Audience)
description: Audience segment (Audience)
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Audience segment (Audience)

The Audience segment dimension contains 5 fields, listed below:

## Audience segment ID (Primary Key)

- **Reporting Field ID**: `audienceSegment.id`
- **Data Type**: `STRING`
- **Description**: The ID assigned to a specific group of users with shared characteristics or behaviors.
- **Required fields**: `audienceSegment.classCode` [📎](guides/reporting/ads-v1/dimensions/audience/audience-segment#audience-segment-class-code), `audienceSegment.name` [📎](guides/reporting/ads-v1/dimensions/audience/audience-segment#audience-segment-name), `audienceSegment.source` [📎](guides/reporting/ads-v1/dimensions/audience/audience-segment#audience-segment-source), `audienceSegment.type` [📎](guides/reporting/ads-v1/dimensions/audience/audience-segment#audience-segment-type), `audienceSegmentCountry.code`
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: `segmentId`
- **Version 3 Reporting Name (Sponsored Ads)**: N/A

## Audience segment name

- **Reporting Field ID**: `audienceSegment.name`
- **Data Type**: `STRING`
- **Description**: The name of an audience segment.
- **Required fields**: `audienceSegment.id` [📎](guides/reporting/ads-v1/dimensions/audience/audience-segment#audience-segment-id-primary-key)
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: `Segment`
- **Version 3 Reporting Name (Sponsored Ads)**: N/A

## Audience segment type

- **Reporting Field ID**: `audienceSegment.type`
- **Data Type**: `STRING`
- **Description**: The type of audience segment like remarketing.
- **Required fields**: `audienceSegment.id` [📎](guides/reporting/ads-v1/dimensions/audience/audience-segment#audience-segment-id-primary-key)
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: `segmentType`
- **Version 3 Reporting Name (Sponsored Ads)**: N/A

## Audience segment class code

- **Reporting Field ID**: `audienceSegment.classCode`
- **Data Type**: `STRING`
- **Description**: A segment class like behavioral or user agent.
- **Required fields**: `audienceSegment.id` [📎](guides/reporting/ads-v1/dimensions/audience/audience-segment#audience-segment-id-primary-key)
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: `segmentClassCode`
- **Version 3 Reporting Name (Sponsored Ads)**: N/A

## Audience segment source

- **Reporting Field ID**: `audienceSegment.source`
- **Data Type**: `STRING`
- **Description**: The source of the audience segment, for example AAX.
- **Required fields**: `audienceSegment.id` [📎](guides/reporting/ads-v1/dimensions/audience/audience-segment#audience-segment-id-primary-key)
- **Complementary fields**: N/A
- **Version 3 Reporting Name (DSP)**: N/A
- **Version 3 Reporting Name (Sponsored Ads)**: N/A


## Dimension Compatibility

| Dimension | Compatible |
|-----------|------------|
| [Ad](guides/reporting/ads-v1/dimensions/level-of-detail/ad) | ❌ |
| [Ad group](guides/reporting/ads-v1/dimensions/level-of-detail/ad-group) | ✅ |
| [Target](guides/reporting/ads-v1/dimensions/targeting/target) | ❌ |
| [Ad product](guides/reporting/ads-v1/dimensions/level-of-detail/ad-product) | ✅ |
| [Advertised product](guides/reporting/ads-v1/dimensions/product/advertised-product) | ❌ |
| [Advertised product marketplace](guides/reporting/ads-v1/dimensions/product/advertised-product-marketplace) | ❌ |
| [Advertised product SKU](guides/reporting/ads-v1/dimensions/product/advertised-product-sku) | ❌ |
| [Advertiser account](guides/reporting/ads-v1/dimensions/level-of-detail/advertiser-account) | ✅ |
| [Audience segment targeting status](guides/reporting/ads-v1/dimensions/audience/audience-segment-targeting-status) | ✅ |
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
| [Conversion definition (off-Amazon)](guides/reporting/ads-v1/dimensions/conversion/conversion-definition-off-amazon) | ❌ |
| [Conversion type (off-Amazon)](guides/reporting/ads-v1/dimensions/conversion/conversion-type-off-amazon) | ❌ |
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

- `metric.addToCartFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-cart#add-to-cart-from-clicks-promoted)
- `metric.addToCartFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-cart#add-to-cart-from-views-promoted)
- `metric.addToCartPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-cart#add-to-cart-promoted)
- `metric.addToCartRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-cart#add-to-cart-rate-promoted)
- `metric.addToListFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-list#add-to-list-from-clicks-promoted)
- `metric.addToListFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-list#add-to-list-from-views-promoted)
- `metric.addToListPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-list#add-to-list-promoted)
- `metric.addToListRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-list#add-to-list-rate-promoted)
- `metric.addToWatchlist` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/add-to-watchlist#add-to-watchlist)
- `metric.addToWatchlistFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/add-to-watchlist#add-to-watchlist-from-clicks)
- `metric.addToWatchlistFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/add-to-watchlist#add-to-watchlist-from-views)
- `metric.addToWatchlistRate` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/add-to-watchlist#add-to-watchlist-rate)
- `metric.alexaSkillEnable` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-enable#alexa-skill-enable)
- `metric.alexaSkillEnableFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-enable#alexa-skill-enable-from-clicks)
- `metric.alexaSkillEnableFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-enable#alexa-skill-enable-from-views)
- `metric.alexaSkillEnableRate` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-enable#alexa-skill-enable-rate)
- `metric.alexaSkillInvocationRate` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-invocations#alexa-skill-invocation-rate)
- `metric.alexaSkillInvocations` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-invocations#alexa-skill-invocations)
- `metric.alexaSkillInvocationsFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-invocations#alexa-skill-invocations-from-clicks)
- `metric.alexaSkillInvocationsFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-invocations#alexa-skill-invocations-from-views)
- `metric.amazonAudienceFees` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/fees#amazon-audience-fees)
- `metric.amazonAudienceFeesConverted` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/fees#amazon-audience-fees-converted)
- `metric.amazonConsoleFees` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/fees#amazon-console-fees)
- `metric.amazonConsoleFeesConverted` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/fees#amazon-console-fees-converted)
- `metric.brandedSearchRate` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/branded-searches#branded-search-rate)
- `metric.brandedSearches` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/branded-searches#branded-searches)
- `metric.brandedSearchesFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/branded-searches#branded-searches-from-clicks)
- `metric.brandedSearchesFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/branded-searches#branded-searches-from-views)
- `metric.clicks` [📎](guides/reporting/ads-v1/metrics/delivery/clicks#clicks)
- `metric.completeListensAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#complete-listens-audio-ad)
- `metric.completeViewsVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#complete-views-video-ad)
- `metric.completionRateAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#completion-rate-audio-ad)
- `metric.completionRateVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#completion-rate-video-ad)
- `metric.costPerAddToCartPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-cart#cost-per-add-to-cart-promoted)
- `metric.costPerAddToListPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/add-to-list#cost-per-add-to-list-promoted)
- `metric.costPerAddToWatchlist` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/add-to-watchlist#cost-per-add-to-watchlist)
- `metric.costPerAlexaSkillEnable` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-enable#cost-per-alexa-skill-enable)
- `metric.costPerAlexaSkillInvocation` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/alexa-skill-invocations#cost-per-alexa-skill-invocation)
- `metric.costPerBrandedSearch` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/branded-searches#cost-per-branded-search)
- `metric.costPerCompletedListenAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#cost-per-completed-listen-audio-ad)
- `metric.costPerCompletedViewVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#cost-per-completed-view-video-ad)
- `metric.costPerDetailPageViewFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views#cost-per-detail-page-view-from-clicks-promoted)
- `metric.costPerDetailPageViewPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views#cost-per-detail-page-view-promoted)
- `metric.costPerDownloadedVideoPlay` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/downloaded-video-plays#cost-per-downloaded-video-play)
- `metric.costPerFreeTrialSubscriptionSignUp` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/free-trial-subscription-sign-ups#cost-per-free-trial-subscription-sign-up)
- `metric.costPerNewToBrandDetailPageView` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#cost-per-detail-page-view-new-to-brand)
- `metric.costPerNewToBrandDetailPageViewPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#cost-per-detail-page-view-new-to-brand-promoted)
- `metric.costPerNewToBrandPurchasePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases-new-to-brand#cost-per-purchase-new-to-brand-promoted)
- `metric.costPerPaidSubscriptionSignUp` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/paid-subscription-sign-ups#cost-per-paid-subscription-sign-up)
- `metric.costPerProductReviewPageVisitPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/product-review-page-visits#cost-per-review-page-visit-promoted)
- `metric.costPerPurchaseFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#cost-per-purchase-from-clicks-promoted)
- `metric.costPerPurchasePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#cost-per-purchase-promoted)
- `metric.costPerRental` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/rentals#cost-per-rental)
- `metric.costPerSubscribeAndSaveSubscriptionPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/subscribe-save-subscriptions#cost-per-subscribe--save-subscription-promoted)
- `metric.costPerSubscriptionSignUp` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/subscription-sign-ups#cost-per-subscription-sign-up)
- `metric.costPerTrailerPlay` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/trailer-plays#cost-per-trailer-play)
- `metric.costPerVideoStreamPlay` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/video-stream-plays#cost-per-video-stream-play)
- `metric.cpc` [📎](guides/reporting/ads-v1/metrics/delivery/clicks#cpc)
- `metric.cpcConverted` [📎](guides/reporting/ads-v1/metrics/delivery/clicks#cpc-converted)
- `metric.cpm` [📎](guides/reporting/ads-v1/metrics/delivery/impressions#cpm)
- `metric.ctr` [📎](guides/reporting/ads-v1/metrics/delivery/clicks#ctr)
- `metric.detailPageViewFromClickRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views#detail-page-view-from-click-rate-promoted)
- `metric.detailPageViewRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views#detail-page-view-rate-promoted)
- `metric.detailPageViewsFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views#detail-page-views-from-clicks-promoted)
- `metric.detailPageViewsFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views#detail-page-views-from-views-promoted)
- `metric.detailPageViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views#detail-page-views-promoted)
- `metric.downloadedVideoPlayRate` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/downloaded-video-plays#downloaded-video-play-rate)
- `metric.downloadedVideoPlays` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/downloaded-video-plays#downloaded-video-plays)
- `metric.downloadedVideoPlaysFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/downloaded-video-plays#downloaded-video-plays-from-clicks)
- `metric.downloadedVideoPlaysFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/downloaded-video-plays#downloaded-video-play-from-views)
- `metric.firstQuartileAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#first-quartile-audio-ad)
- `metric.firstQuartileVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#first-quartile-video-ad)
- `metric.freeTrialAppSubscriptionSignUpRate` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/free-trial-app-subscription-sign-ups#free-trial-app-subscription-sign-up-rate)
- `metric.freeTrialSubscriptionSignUpRate` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/free-trial-subscription-sign-ups#free-trial-subscription-sign-up-rate)
- `metric.freeTrialSubscriptionSignUps` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/free-trial-subscription-sign-ups#free-trial-subscription-sign-ups)
- `metric.freeTrialSubscriptionSignUpsFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/free-trial-subscription-sign-ups#free-trial-subscription-sign-ups-from-clicks)
- `metric.freeTrialSubscriptionSignUpsFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/free-trial-subscription-sign-ups#free-trial-subscription-sign-ups-from-views)
- `metric.grossClicks` [📎](guides/reporting/ads-v1/metrics/delivery/clicks#gross-clicks)
- `metric.impressions` [📎](guides/reporting/ads-v1/metrics/delivery/impressions#impressions)
- `metric.impressionsAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#impressions-audio-ad)
- `metric.impressionsVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#impressions-video-ad)
- `metric.interactiveImpressions` [📎](guides/reporting/ads-v1/metrics/engagement/interaction#interactive-impressions)
- `metric.invalidClickRate` [📎](guides/reporting/ads-v1/metrics/delivery/clicks#invalid-click-rate)
- `metric.invalidClicks` [📎](guides/reporting/ads-v1/metrics/delivery/clicks#invalid-clicks)
- `metric.invalidImpressionRate` [📎](guides/reporting/ads-v1/metrics/delivery/impressions#invalid-impression-rate)
- `metric.invalidImpressions` [📎](guides/reporting/ads-v1/metrics/delivery/impressions#invalid-impressions)
- `metric.mainImdbAdClicks` [📎](guides/reporting/ads-v1/metrics/delivery/clicks#main-imdb-ad-clicks)
- `metric.mainImdbAdImpressions` [📎](guides/reporting/ads-v1/metrics/delivery/impressions#main-imdb-ad-impressions)
- `metric.mediaSpendCpm` [📎](guides/reporting/ads-v1/metrics/delivery/impressions#media-spend-cpm)
- `metric.midpointAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#midpoint-audio-ad)
- `metric.midpointVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#midpoint-video-ad)
- `metric.mutesAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#mutes-audio-ad)
- `metric.mutesVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#mutes-video-ad)
- `metric.newToBrandDetailPageViewRate` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#detail-page-view-rate-new-to-brand)
- `metric.newToBrandDetailPageViewRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#detail-page-view-rate-new-to-brand-promoted)
- `metric.newToBrandDetailPageViews` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#detail-page-views-new-to-brand)
- `metric.newToBrandDetailPageViewsFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#detail-page-views-from-clicks-new-to-brand)
- `metric.newToBrandDetailPageViewsFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#detail-page-views-from-clicks-new-to-brand-promoted)
- `metric.newToBrandDetailPageViewsFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#detail-page-views-from-views-new-to-brand)
- `metric.newToBrandDetailPageViewsFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#detail-page-views-from-views-new-to-brand-promoted)
- `metric.newToBrandDetailPageViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/detail-page-views-new-to-brand#detail-page-views-new-to-brand-promoted)
- `metric.newToBrandPurchaseRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases-new-to-brand#purchase-rate-new-to-brand-promoted)
- `metric.newToBrandPurchasesFromClicksHalo` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases-new-to-brand#purchases-from-clicks-new-to-brand-halo)
- `metric.newToBrandPurchasesFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases-new-to-brand#purchases-from-clicks-new-to-brand-promoted)
- `metric.newToBrandPurchasesFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases-new-to-brand#purchases-from-views-new-to-brand-promoted)
- `metric.newToBrandPurchasesPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases-new-to-brand#purchases-new-to-brand-promoted)
- `metric.notificationClicks` [📎](guides/reporting/ads-v1/metrics/engagement/interaction#notification-clicks)
- `metric.notificationOpens` [📎](guides/reporting/ads-v1/metrics/engagement/interaction#notification-opens)
- `metric.offAmazonAddToShoppingCart` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/add-to-shopping-cart-off-amazon#add-to-shopping-cart-off-amazon)
- `metric.offAmazonAddToShoppingCartFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/add-to-shopping-cart-off-amazon#add-to-shopping-cart-from-clicks-off-amazon)
- `metric.offAmazonAddToShoppingCartFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/add-to-shopping-cart-off-amazon#add-to-shopping-cart-from-views-off-amazon)
- `metric.offAmazonAddToShoppingCartRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/add-to-shopping-cart-off-amazon#add-to-shopping-cart-rate-off-amazon)
- `metric.offAmazonAddToShoppingCartValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/add-to-shopping-cart-off-amazon#add-to-shopping-cart-value-average-off-amazon)
- `metric.offAmazonAddToShoppingCartValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/add-to-shopping-cart-off-amazon#add-to-shopping-cart-value-sum-off-amazon)
- `metric.offAmazonApplicationRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/applications-off-amazon#application-rate-off-amazon)
- `metric.offAmazonApplications` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/applications-off-amazon#applications-off-amazon)
- `metric.offAmazonApplicationsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/applications-off-amazon#applications-from-clicks-off-amazon)
- `metric.offAmazonApplicationsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/applications-off-amazon#applications-from-views-off-amazon)
- `metric.offAmazonApplicationsValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/applications-off-amazon#applications-value-average-off-amazon)
- `metric.offAmazonApplicationsValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/applications-off-amazon#applications-value-sum-off-amazon)
- `metric.offAmazonCheckoutRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/checkouts-off-amazon#checkout-rate-off-amazon)
- `metric.offAmazonCheckouts` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/checkouts-off-amazon#checkouts-off-amazon)
- `metric.offAmazonCheckoutsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/checkouts-off-amazon#checkouts-from-clicks-off-amazon)
- `metric.offAmazonCheckoutsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/checkouts-off-amazon#checkouts-from-views-off-amazon)
- `metric.offAmazonCheckoutsValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/checkouts-off-amazon#checkouts-value-average-off-amazon)
- `metric.offAmazonCheckoutsValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/checkouts-off-amazon#checkouts-value-sum-off-amazon)
- `metric.offAmazonContactRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/contacts-off-amazon#contact-rate-off-amazon)
- `metric.offAmazonContacts` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/contacts-off-amazon#contacts-off-amazon)
- `metric.offAmazonContactsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/contacts-off-amazon#contacts-from-clicks-off-amazon)
- `metric.offAmazonContactsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/contacts-off-amazon#contacts-from-views-off-amazon)
- `metric.offAmazonContactsValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/contacts-off-amazon#contacts-value-average-off-amazon)
- `metric.offAmazonContactsValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/contacts-off-amazon#contacts-value-sum-off-amazon)
- `metric.offAmazonConversionRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversion-rate-off-amazon)
- `metric.offAmazonConversions` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-off-amazon)
- `metric.offAmazonConversionsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-from-clicks-off-amazon)
- `metric.offAmazonConversionsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#conversions-from-views-off-amazon)
- `metric.offAmazonCostPerAddToShoppingCart` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/add-to-shopping-cart-off-amazon#cost-per-add-to-shopping-cart-off-amazon)
- `metric.offAmazonCostPerApplication` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/applications-off-amazon#cost-per-application-off-amazon)
- `metric.offAmazonCostPerCheckout` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/checkouts-off-amazon#cost-per-checkout-off-amazon)
- `metric.offAmazonCostPerContact` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/contacts-off-amazon#cost-per-contact-off-amazon)
- `metric.offAmazonCostPerConversion` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/conversions-off-amazon#cost-per-conversion-off-amazon)
- `metric.offAmazonCostPerInstall` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/installs-off-amazon#cost-per-install-off-amazon)
- `metric.offAmazonCostPerLead` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/leads-off-amazon#cost-per-lead-off-amazon)
- `metric.offAmazonCostPerOther` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/other-off-amazon#cost-per-other-off-amazon)
- `metric.offAmazonCostPerPageView` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/page-views-off-amazon#cost-per-page-view-off-amazon)
- `metric.offAmazonCostPerPurchase` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#cost-per-purchase-off-amazon)
- `metric.offAmazonCostPerSearch` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/searches-off-amazon#cost-per-search-off-amazon)
- `metric.offAmazonCostPerSignUp` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/sign-ups-off-amazon#cost-per-sign-up-off-amazon)
- `metric.offAmazonCostPerSubscribe` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/subscribe-off-amazon#cost-per-subscribe-off-amazon)
- `metric.offAmazonInstallRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/installs-off-amazon#install-rate-off-amazon)
- `metric.offAmazonInstalls` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/installs-off-amazon#installs-off-amazon)
- `metric.offAmazonInstallsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/installs-off-amazon#installs-from-clicks-off-amazon)
- `metric.offAmazonInstallsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/installs-off-amazon#installs-from-views-off-amazon)
- `metric.offAmazonInstallsValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/installs-off-amazon#installs-value-average-off-amazon)
- `metric.offAmazonInstallsValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/installs-off-amazon#installs-value-sum-off-amazon)
- `metric.offAmazonLeadRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/leads-off-amazon#lead-rate-off-amazon)
- `metric.offAmazonLeads` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/leads-off-amazon#leads-off-amazon)
- `metric.offAmazonLeadsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/leads-off-amazon#leads-from-clicks-off-amazon)
- `metric.offAmazonLeadsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/leads-off-amazon#leads-from-views-off-amazon)
- `metric.offAmazonLeadsValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/leads-off-amazon#leads-value-average-off-amazon)
- `metric.offAmazonLeadsValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/leads-off-amazon#leads-value-sum-off-amazon)
- `metric.offAmazonOther` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/other-off-amazon#other-off-amazon)
- `metric.offAmazonOtherFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/other-off-amazon#other-from-clicks-off-amazon)
- `metric.offAmazonOtherFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/other-off-amazon#other-from-views-off-amazon)
- `metric.offAmazonOtherRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/other-off-amazon#other-rate-off-amazon)
- `metric.offAmazonOtherValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/other-off-amazon#other-value-average-off-amazon)
- `metric.offAmazonOtherValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/other-off-amazon#other-value-sum-off-amazon)
- `metric.offAmazonPageViewRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/page-views-off-amazon#page-view-rate-off-amazon)
- `metric.offAmazonPageViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/page-views-off-amazon#page-views-off-amazon)
- `metric.offAmazonPageViewsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/page-views-off-amazon#page-views-from-clicks-off-amazon)
- `metric.offAmazonPageViewsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/page-views-off-amazon#page-views-from-views-off-amazon)
- `metric.offAmazonPageViewsValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/page-views-off-amazon#page-views-value-average-off-amazon)
- `metric.offAmazonPageViewsValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/page-views-off-amazon#page-views-value-sum-off-amazon)
- `metric.offAmazonPurchaseRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#purchase-rate-off-amazon)
- `metric.offAmazonPurchases` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#purchases-off-amazon)
- `metric.offAmazonPurchasesFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#purchases-from-clicks-off-amazon)
- `metric.offAmazonPurchasesFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/purchases-off-amazon#purchases-from-views-off-amazon)
- `metric.offAmazonSearchRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/searches-off-amazon#search-rate-off-amazon)
- `metric.offAmazonSearches` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/searches-off-amazon#searches-off-amazon)
- `metric.offAmazonSearchesFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/searches-off-amazon#searches-from-clicks-off-amazon)
- `metric.offAmazonSearchesFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/searches-off-amazon#searches-from-views-off-amazon)
- `metric.offAmazonSearchesValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/searches-off-amazon#searches-value-average-off-amazon)
- `metric.offAmazonSearchesValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/searches-off-amazon#searches-value-sum-off-amazon)
- `metric.offAmazonSignUpRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/sign-ups-off-amazon#sign-up-rate-off-amazon)
- `metric.offAmazonSignUps` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/sign-ups-off-amazon#sign-ups-off-amazon)
- `metric.offAmazonSignUpsFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/sign-ups-off-amazon#sign-ups-from-clicks-off-amazon)
- `metric.offAmazonSignUpsFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/sign-ups-off-amazon#sign-ups-from-views-off-amazon)
- `metric.offAmazonSignUpsValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/sign-ups-off-amazon#sign-ups-value-average-off-amazon)
- `metric.offAmazonSignUpsValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/sign-ups-off-amazon#sign-ups-value-sum-off-amazon)
- `metric.offAmazonSubscribe` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/subscribe-off-amazon#subscribe-off-amazon)
- `metric.offAmazonSubscribeFromClicks` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/subscribe-off-amazon#subscribe-from-clicks-off-amazon)
- `metric.offAmazonSubscribeFromViews` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/subscribe-off-amazon#subscribe-from-views-off-amazon)
- `metric.offAmazonSubscribeRate` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/subscribe-off-amazon#subscribe-rate-off-amazon)
- `metric.offAmazonSubscribeValueAverage` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/subscribe-off-amazon#subscribe-value-average-off-amazon)
- `metric.offAmazonSubscribeValueSum` [📎](guides/reporting/ads-v1/metrics/off-amazon-conversions/subscribe-off-amazon#subscribe-value-sum-off-amazon)
- `metric.omnichannelMetricFees` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/fees#omnichannel-metrics-fees)
- `metric.omnichannelMetricFeesConverted` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/fees#omnichannel-metrics-fees-converted)
- `metric.paidSubscriptionSignUpRate` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/paid-subscription-sign-ups#paid-subscription-sign-up-rate)
- `metric.paidSubscriptionSignUps` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/paid-subscription-sign-ups#paid-subscription-sign-ups)
- `metric.paidSubscriptionSignUpsFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/paid-subscription-sign-ups#paid-subscription-sign-ups-from-clicks)
- `metric.paidSubscriptionSignUpsFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/paid-subscription-sign-ups#paid-subscription-sign-ups-from-views)
- `metric.pausesAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#pauses-audio-ad)
- `metric.pausesVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#pauses-video-ad)
- `metric.percentOfPurchasesNewToBrandPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases-new-to-brand#percent-of-purchases-new-to-brand-promoted)
- `metric.playsAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#plays-audio-ad)
- `metric.productReviewPageVisitRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/product-review-page-visits#review-page-visit-rate-promoted)
- `metric.productReviewPageVisitsFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/product-review-page-visits#review-page-visits-from-clicks-promoted)
- `metric.productReviewPageVisitsFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/product-review-page-visits#review-page-visits-from-views-promoted)
- `metric.productReviewPageVisitsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/product-review-page-visits#review-page-visits-promoted)
- `metric.progressAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#progress-audio-ad)
- `metric.purchaseFromClickRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#purchase-from-click-rate-promoted)
- `metric.purchaseRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#purchase-rate-promoted)
- `metric.purchases` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#purchases)
- `metric.purchasesFromClicksHalo` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#purchases-from-clicks-halo)
- `metric.purchasesFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#purchases-from-clicks-promoted)
- `metric.purchasesFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#purchases-from-views-promoted)
- `metric.purchasesPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#purchases-promoted)
- `metric.rentalRate` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/rentals#rental-rate)
- `metric.rentals` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/rentals#rentals)
- `metric.rentalsFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/rentals#rentals-from-clicks)
- `metric.rentalsFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/rentals#rentals-from-views)
- `metric.replaysVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#replays-video-ad)
- `metric.resumesAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#resumes-audio-ad)
- `metric.resumesVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#resumes-video-ad)
- `metric.rewindsAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#rewinds-audio-ad)
- `metric.roas` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#roas)
- `metric.roasFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#roas-from-clicks-promoted)
- `metric.sales` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#sales)
- `metric.salesFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#sales-from-clicks-promoted)
- `metric.salesFromClicksPromotedConverted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#sales-from-clicks-promoted-converted)
- `metric.salesFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#sales-from-views-promoted)
- `metric.salesFromViewsPromotedConverted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#sales-from-views-promoted-converted)
- `metric.skipsAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#skips-audio-ad)
- `metric.skipsBackVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#skips-backs-video-ad)
- `metric.skipsForwardVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#skips-forward-video-ad)
- `metric.startsAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#starts-audio-ad)
- `metric.startsVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#starts-video-ad)
- `metric.subscribeAndSaveSubscriptionRatePromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/subscribe-save-subscriptions#subscribe--save-subscription-rate-promoted)
- `metric.subscribeAndSaveSubscriptionsFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/subscribe-save-subscriptions#subscribe--save-subscriptions-from-clicks-promoted)
- `metric.subscribeAndSaveSubscriptionsFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/subscribe-save-subscriptions#subscribe--save-subscriptions-from-views-promoted)
- `metric.subscribeAndSaveSubscriptionsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/subscribe-save-subscriptions#subscribe--save-subscriptions-promoted)
- `metric.subscriptionSignUpRate` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/subscription-sign-ups#subscription-sign-up-rate)
- `metric.subscriptionSignUps` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/subscription-sign-ups#subscription-sign-ups)
- `metric.subscriptionSignUpsFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/subscription-sign-ups#subscription-sign-ups-from-clicks)
- `metric.subscriptionSignUpsFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-device-conversions/subscription-sign-ups#subscription-sign-ups-from-views)
- `metric.supplyCost` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/costs#supply-cost)
- `metric.supplyCostConverted` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/costs#supply-cost-converted)
- `metric.thirdQuartileAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#third-quartile-audio-ad)
- `metric.thirdQuartileVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#third-quartile-video-ad)
- `metric.totalCost` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/costs#total-cost)
- `metric.totalCostConverted` [📎](guides/reporting/ads-v1/metrics/costs-and-fees/costs#total-cost-converted)
- `metric.trailerPlayRate` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/trailer-plays#trailer-play-rate)
- `metric.trailerPlays` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/trailer-plays#trailer-plays)
- `metric.trailerPlaysFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/trailer-plays#trailer-plays-from-clicks)
- `metric.trailerPlaysFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/trailer-plays#trailer-plays-from-views)
- `metric.unitsSold` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#units-sold)
- `metric.unitsSoldFromClicksPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#units-sold-from-clicks-promoted)
- `metric.unitsSoldFromViewsPromoted` [📎](guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#units-sold-from-views-promoted)
- `metric.unmutesAudioAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-audio-ad#unmutes-audio-ad)
- `metric.unmutesVideoAd` [📎](guides/reporting/ads-v1/metrics/engagement/attention-video-ad#unmutes-video-ad)
- `metric.videoStreamPlayRate` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/video-stream-plays#video-stream-play-rate)
- `metric.videoStreamPlays` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/video-stream-plays#video-stream-plays)
- `metric.videoStreamPlaysFromClicks` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/video-stream-plays#video-stream-plays-from-clicks)
- `metric.videoStreamPlaysFromViews` [📎](guides/reporting/ads-v1/metrics/amazon-video-conversions/video-stream-plays#video-stream-play-from-views)


---

## See also

- [Audience segment targeting status](guides/reporting/ads-v1/dimensions/audience/audience-segment-targeting-status)
