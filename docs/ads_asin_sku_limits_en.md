# Amazon Ads API (v1) - ASIN / SKU Capacity and Constraints by Ad Product

This document provides a comprehensive breakdown of the allowable number of ASINs/SKUs and identifier constraints per Ad and per Campaign across different Amazon Ads products (SP, SB, SD, DSP, ST, SP Global), based on the Merged OpenAPI specifications located in `codegen/v1/data/openapi/`.

---

## 1. Hierarchy and Counting Architecture

In Amazon Ads API (v1), the entity hierarchy is organized as follows:
$$\text{Campaign} \longrightarrow \text{Ad Group} \longrightarrow \text{Ad (Creative / Entity)}$$

- **ASIN / SKU Binding Level**: Product identifiers (ASIN or SKU) are defined at the **Ad** level within its creative configuration (such as `advertisedProduct`, `products`, `landingPageAsins`, etc.).
- **Total ASIN / SKU Capacity per Campaign**:
  $$\text{Campaign Product Capacity} = \sum_{\text{AdGroups}} \sum_{\text{Ads}} (\text{ASINs/SKUs per Ad})$$
- **Single API Batch Request Limits**: In batch endpoints (`CreateAdRequest`, `UpdateAdRequest`, `DeleteAdRequest`), the maximum number of Ad objects submitted in a single request (`ads` array `maxItems`) varies by ad product (ranging from 10 to 1,000).

---

## 2. Comparison Matrix Across All Ad Products

| Ad Product | OpenAPI Spec File | Supported ID Types | Creative Setting / Sub-type | ASIN / SKU Count per Ad | Single API Batch Limit (`ads.maxItems`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SP** (Sponsored Products) | `AmazonAdsAPISPMerged_prod_3p.json` | `ASIN`, `SKU` | `productCreativeSettings`<br>(Standard product / spotlight video) | **Exactly 1** (`advertisedProduct`) | **1,000** |
| **SP Global** (Global SP) | `AmazonAdsAPISPGLOBALMerged_prod_3p.json` | `ASIN`, `SKU` | `productCreativeSettings`<br>(Cross-marketplace global ad) | **1 per marketplace**<br>(Supports 1 ~ 30 marketplaces, max 30) | **1,000** |
| **SB** (Sponsored Brands) | `AmazonAdsAPISBMerged_prod_3p.json` | `ASIN` only | **Product Collection** | Promoted `products`: **0 ~ 3**<br>Landing page (`ASIN_LIST`): **1 ~ 100** | **10** |
| | | `ASIN` only | **Store Spotlight** | `cards`: **Exactly 3 cards**<br>(1 ASIN per card, total 3 ASINs) | **10** |
| | | `ASIN` only | **Product Video** | `products`: **0 ~ 3** | **10** |
| | | `ASIN` only | **Manual Collection** | `productInclusions`: **3 ~ 10** | **10** |
| | | `ASIN` only | **Auto Collection** | `productExclusions`: **0 ~ 1,000** (exclusions) | **10** |
| | | `ASIN` only | **Brand Gallery** | `cards`: 0 ~ 5 cards (no direct product field) | **10** |
| **SD** (Sponsored Display) | `AmazonAdsAPISDMerged_prod_3p.json` | `ASIN`, `SKU` | **Responsive eCommerce** | `products`: **0 ~ 1** | **100** |
| | | `ASIN`, `SKU` | **Product Video** | `products`: **0 ~ 1** | **100** |
| | | `ASIN`, `SKU` | **Asset Based Creative** | None (off-Amazon landing page) | **100** |
| **DSP** (Demand Side Platform) | `AmazonAdsAPIDSPMerged_prod_3p.json` | `ASIN` only | **Responsive eCommerce** | `products`: **1 ~ 20** | **10** |
| | | `ASIN` only | **Standard Audio** | `products`: **0 ~ 10** | **10** |
| | | `ASIN` only | **Streaming TV Video** | `products`: **0 ~ 20** | **10** |
| | | `ASIN` only | **Online Video** | `products`: **0 ~ 1** (single object) | **10** |
| | | `ASIN` only | **Standard Display / 3P** | None (pure image or VAST/HTML) | **10** |
| **ST** (Sponsored Television) | `AmazonAdsAPISTMerged_prod_3p.json` | `ASIN`, `SKU` | **Streaming TV Video** | `products`: **0 ~ 1** | **100** |

---

## 3. Detailed Specifications by Ad Product

### 3.1 Sponsored Products (SP)
- **Spec File**: `codegen/v1/data/openapi/AmazonAdsAPISPMerged_prod_3p.json`
- **Supported ID Types**: `SPProductIdType` (`ASIN`, `SKU`)
- **Key Structure**:
  - `creative.productCreative.productCreativeSettings.advertisedProduct` is a single object:
    - `productId`: Product identifier string (required)
    - `productIdType`: `ASIN` or `SKU` (required)
  - Optional `spotlightVideos.videos` (1 ~ 5 video assets), but the advertised product remains **1 product**.
- **Batch Request Limits**:
  - `SPCreateAdRequest.ads`: `minItems: 1`, `maxItems: 1000`
  - `SPUpdateAdRequest.ads`: `minItems: 1`, `maxItems: 1000`
  - `SPDeleteAdRequest.adIds`: `minItems: 1`, `maxItems: 1000`

### 3.2 Sponsored Products Global (SP Global)
- **Spec File**: `codegen/v1/data/openapi/AmazonAdsAPISPGLOBALMerged_prod_3p.json`
- **Supported ID Types**: `SPGlobalProductIdType` (`ASIN`, `SKU`)
- **Key Structure**:
  - `advertisedProduct.marketplaceSettings` is an array (`minItems: 0`, `maxItems: 30`):
    - Allows configuring different `productId` values for individual marketplaces (e.g. US, UK, DE).
    - 1 product identifier per marketplace; a single global ad can cover up to 30 marketplaces with up to 30 products.
- **Batch Request Limits**:
  - `SPGlobalCreateAdRequest.ads`: `minItems: 1`, `maxItems: 1000`

### 3.3 Sponsored Brands (SB)
- **Spec File**: `codegen/v1/data/openapi/AmazonAdsAPISBMerged_prod_3p.json`
- **Supported ID Types**: `SBProductIdType` (`ASIN` only, SKU is not supported)
- **Creative Settings & Constraints**:
  1. **Product Collection (`productCollectionSettings`)**:
     - `products`: Promoted products list, `minItems: 0`, `maxItems: 3` (up to 3 ASINs).
     - `landingPage`: If `landingPageType` is `ASIN_LIST`, the `landingPageAsins.asins` list must contain **1 ~ 100 ASINs** to construct the collection page.
  2. **Store Spotlight (`storeSpotlightSettings`)**:
     - `cards`: **Fixed at 3 cards** (`minItems: 3`, `maxItems: 3`).
     - Each card (`SBCreateCardCreativeElement`) must specify 1 `products` (ASIN) linking to a Brand Store sub-page.
  3. **Product Video (`productVideoSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 3` (up to 3 ASINs).
  4. **Manual Collection (`manualCollectionSettings`)**:
     - `productInclusions`: Curated product list, `minItems: 3`, `maxItems: 10` (must contain 3 ~ 10 ASINs).
  5. **Auto Collection (`autoCollectionSettings`)**:
     - `productExclusions`: Excluded products list for automated collections, `minItems: 0`, `maxItems: 1000` (up to 1,000 excluded ASINs).
  6. **Brand Gallery (`brandGallerySettings`)**:
     - `cards`: `minItems: 0`, `maxItems: 5` (links to Brand Store, no direct product field).
- **Batch Request Limits**:
  - `SBCreateAdRequest.ads`: `minItems: 1`, `maxItems: 10`

### 3.4 Sponsored Display (SD)
- **Spec File**: `codegen/v1/data/openapi/AmazonAdsAPISDMerged_prod_3p.json`
- **Supported ID Types**: `SDProductIdType` (`ASIN`, `SKU`)
- **Creative Settings & Constraints**:
  1. **Responsive eCommerce (`responsiveEcommerceSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 1` (0 or 1 ASIN/SKU).
  2. **Product Video (`productVideoSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 1` (0 or 1 ASIN/SKU).
  3. **Asset Based Creative (`assetBasedCreativeSettings`)**:
     - No `products` field; redirects via `OFF_AMAZON_LINK` landing page.
- **Batch Request Limits**:
  - `SDCreateAdRequest.ads`: `minItems: 1`, `maxItems: 100`

### 3.5 Demand Side Platform (DSP)
- **Spec File**: `codegen/v1/data/openapi/AmazonAdsAPIDSPMerged_prod_3p.json`
- **Supported ID Types**: `DSPProductIdType` (`ASIN` only)
- **Creative Settings & Constraints**:
  1. **Responsive eCommerce (`responsiveEcommerceSettings`)**:
     - `products`: `minItems: 1`, `maxItems: 20` (must contain **1 ~ 20 ASINs**).
  2. **Standard Audio (`standardAudioExperienceSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 10` (up to 10 ASINs).
  3. **Streaming TV Video (`streamingTvSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 20` (up to 20 ASINs).
  4. **Online Video (`onlineVideoSettings`)**:
     - `products`: Single `DSPCreateAdvertisedProducts` object (0 or 1 ASIN).
  5. **Standard Display / Brand Store / Third Party**:
     - No `products` ASIN field.
- **Batch Request Limits**:
  - `DSPCreateAdRequest.ads`: `minItems: 1`, `maxItems: 10`

### 3.6 Sponsored Television (ST)
- **Spec File**: `codegen/v1/data/openapi/AmazonAdsAPISTMerged_prod_3p.json`
- **Supported ID Types**: `STProductIdType` (`ASIN`, `SKU`)
- **Key Structure**:
  - `creative.videoCreative.streamingTvSettings.products`: Array (`minItems: 0`, `maxItems: 1`), supporting 0 or 1 ASIN / SKU.
- **Batch Request Limits**:
  - `STCreateAdRequest.ads`: `minItems: 1`, `maxItems: 100`
