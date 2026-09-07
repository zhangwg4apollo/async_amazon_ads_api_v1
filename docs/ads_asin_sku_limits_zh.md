# Amazon Ads API (v1) - 各广告类型下的 ASIN / SKU 配置数量与规则限制

本文档基于 `codegen/v1/data/openapi/` 中的 Merged OpenAPI 规范，详细梳理在不同广告类型（SP、SB、SD、DSP、ST、SP Global）及其各自创意（Creative）设置下，单个广告（Ad）以及单个广告活动（Campaign）可关联的 ASIN / SKU 数量与规则限制。

---

## 1. 核心层级与计数关系

在 Amazon Ads API (v1) 中，广告实体的层级架构为：
$$\text{Campaign (广告活动)} \longrightarrow \text{Ad Group (广告组)} \longrightarrow \text{Ad (广告创意/实体)}$$

- **ASIN / SKU 绑定位置**：商品标识符（ASIN 或 SKU）均在 **Ad** 层级的创意（Creative）或商品配置（`advertisedProduct` / `products` / `landingPageAsins` 等）中定义。
- **Campaign 维度的商品总容量**：
  $$\text{Campaign 容纳 ASIN/SKU 总数} = \sum_{\text{AdGroups}} \sum_{\text{Ads}} (\text{单条 Ad 关联的 ASIN/SKU 数量})$$
- **单次 API 批量操作限制**：在批量接口（`CreateAdRequest` / `UpdateAdRequest` / `DeleteAdRequest`）中，单次请求可提交的广告对象数量（`ads` 数组 `maxItems`）因产品线而异（10 ~ 1000 不等）。

---

## 2. 全广告类型对比矩阵

| 广告产品 (Ad Product) | 规范文件 | 支持标识符类型 | 创意类型 / 子设置 (Creative Settings) | 单条 Ad 的 ASIN/SKU 数量限制 | 单次批量请求限制 (`ads.maxItems`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SP** (Sponsored Products) | `AmazonAdsAPISPMerged_prod_3p.json` | `ASIN`, `SKU` | `productCreativeSettings`<br>(单品广告 / 焦点视频) | **固定 1 个** (`advertisedProduct`) | **1,000** |
| **SP Global** (全球推广) | `AmazonAdsAPISPGLOBALMerged_prod_3p.json` | `ASIN`, `SKU` | `productCreativeSettings`<br>(跨站点全球单品) | **每个站点 1 个**<br>(支持 1 ~ 30 个站点，最多 30 个) | **1,000** |
| **SB** (Sponsored Brands) | `AmazonAdsAPISBMerged_prod_3p.json` | 仅 `ASIN` | **Product Collection** (商品集) | 直接展示商品 `products`: **0 ~ 3 个**<br>落地页商品 `landingPageAsins`: **1 ~ 100 个** | **10** |
| | | 仅 `ASIN` | **Store Spotlight** (旗舰店焦点) | `cards`: **固定 3 张卡片**<br>(每张卡片 1 个 ASIN，共 3 个) | **10** |
| | | 仅 `ASIN` | **Product Video** (商品视频) | `products`: **0 ~ 3 个** | **10** |
| | | 仅 `ASIN` | **Manual Collection** (手动精选集) | `productInclusions`: **3 ~ 10 个** | **10** |
| | | 仅 `ASIN` | **Auto Collection** (自动集合) | `productExclusions`: **0 ~ 1,000 个** (排除项) | **10** |
| | | 仅 `ASIN` | **Brand Gallery** (品牌画廊) | `cards`: 0 ~ 5 张 (无直接 product 字段) | **10** |
| **SD** (Sponsored Display) | `AmazonAdsAPISDMerged_prod_3p.json` | `ASIN`, `SKU` | **Responsive eCommerce** (自适应电商) | `products`: **0 ~ 1 个** | **100** |
| | | `ASIN`, `SKU` | **Product Video** (商品视频) | `products`: **0 ~ 1 个** | **100** |
| | | `ASIN`, `SKU` | **Asset Based Creative** (素材引流) | 无 products 字段 (外链落地页) | **100** |
| **DSP** (Demand Side Platform) | `AmazonAdsAPIDSPMerged_prod_3p.json` | 仅 `ASIN` | **Responsive eCommerce** (自适应电商) | `products`: **1 ~ 20 个** | **10** |
| | | 仅 `ASIN` | **Standard Audio** (标准音频广告) | `products`: **0 ~ 10 个** | **10** |
| | | 仅 `ASIN` | **Streaming TV** (流媒体电视视频) | `products`: **0 ~ 20 个** | **10** |
| | | 仅 `ASIN` | **Online Video** (在线视频) | `products`: **0 ~ 1 个** (单个对象) | **10** |
| | | 仅 `ASIN` | **Standard Display / 3P** (标准展示/三方) | 无 products 字段 (纯图片或 VAST/HTML) | **10** |
| **ST** (Sponsored Television) | `AmazonAdsAPISTMerged_prod_3p.json` | `ASIN`, `SKU` | **Streaming TV** (流媒体电视广告) | `products`: **0 ~ 1 个** | **100** |

---

## 3. 各广告产品详细规格剖析

### 3.1 Sponsored Products (SP)
- **规范文件**: `codegen/v1/data/openapi/AmazonAdsAPISPMerged_prod_3p.json`
- **支持类型**: `SPProductIdType` (`ASIN`, `SKU`)
- **核心结构**:
  - `creative.productCreative.productCreativeSettings.advertisedProduct` 为单一对象：
    - `productId`: 商品标识符字符串 (必填)
    - `productIdType`: `ASIN` 或 `SKU` (必填)
  - 可选附带 `spotlightVideos.videos` (1 ~ 5 个视频)，但所推广的主体商品始终为 **1 个**。
- **批量请求限制**:
  - `SPCreateAdRequest.ads`: `minItems: 1`, `maxItems: 1000`
  - `SPUpdateAdRequest.ads`: `minItems: 1`, `maxItems: 1000`
  - `SPDeleteAdRequest.adIds`: `minItems: 1`, `maxItems: 1000`

### 3.2 Sponsored Products Global (SP Global)
- **规范文件**: `codegen/v1/data/openapi/AmazonAdsAPISPGLOBALMerged_prod_3p.json`
- **支持类型**: `SPGlobalProductIdType` (`ASIN`, `SKU`)
- **核心结构**:
  - `advertisedProduct.marketplaceSettings` 为数组 (`minItems: 0`, `maxItems: 30`)：
    - 允许针对不同国家站点（Marketplace，如 US, UK, DE 等）配置对应的 `productId`。
    - 每个站点配置 1 个商品标识符，单条 Global Ad 最多可同时覆盖 30 个站点对应的 30 个商品。
- **批量请求限制**:
  - `SPGlobalCreateAdRequest.ads`: `minItems: 1`, `maxItems: 1000`

### 3.3 Sponsored Brands (SB)
- **规范文件**: `codegen/v1/data/openapi/AmazonAdsAPISBMerged_prod_3p.json`
- **支持类型**: `SBProductIdType` (仅支持 `ASIN`)
- **各创意场景与限制**:
  1. **Product Collection (`productCollectionSettings`)**:
     - `products`: 直接展示商品列表，`minItems: 0`, `maxItems: 3` (最多 3 个 ASIN)。
     - `landingPage`: 若类型为 `ASIN_LIST`，其 `landingPageAsins.asins` 列表包含 **1 ~ 100 个** ASIN 作为落地页展示清单。
  2. **Store Spotlight (`storeSpotlightSettings`)**:
     - `cards`: **固定为 3 张卡片** (`minItems: 3`, `maxItems: 3`)。
     - 每张卡片 (`SBCreateCardCreativeElement`) 必须包含 1 个 `products` (ASIN) 并链接到 Brand Store 子页面。
  3. **Product Video (`productVideoSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 3` (最多 3 个 ASIN)。
  4. **Manual Collection (`manualCollectionSettings`)**:
     - `productInclusions`: 手动选品集合，`minItems: 3`, `maxItems: 10` (必须包含 3 ~ 10 个 ASIN)。
  5. **Auto Collection (`autoCollectionSettings`)**:
     - `productExclusions`: 自动集合中的排除商品列表，`minItems: 0`, `maxItems: 1000` (最多排除 1000 个 ASIN)。
  6. **Brand Gallery (`brandGallerySettings`)**:
     - `cards`: `minItems: 0`, `maxItems: 5` (跳转至品牌旗舰店，无直接商品字段)。
- **批量请求限制**:
  - `SBCreateAdRequest.ads`: `minItems: 1`, `maxItems: 10`

### 3.4 Sponsored Display (SD)
- **规范文件**: `codegen/v1/data/openapi/AmazonAdsAPISDMerged_prod_3p.json`
- **支持类型**: `SDProductIdType` (`ASIN`, `SKU`)
- **各创意场景与限制**:
  1. **Responsive eCommerce (`responsiveEcommerceSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 1` (最多 1 个 ASIN/SKU)。
  2. **Product Video (`productVideoSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 1` (最多 1 个 ASIN/SKU)。
  3. **Asset Based Creative (`assetBasedCreativeSettings`)**:
     - 无 `products` 字段，主要通过 `OFF_AMAZON_LINK` 落地页进行站外引流。
- **批量请求限制**:
  - `SDCreateAdRequest.ads`: `minItems: 1`, `maxItems: 100`

### 3.5 Demand Side Platform (DSP)
- **规范文件**: `codegen/v1/data/openapi/AmazonAdsAPIDSPMerged_prod_3p.json`
- **支持类型**: `DSPProductIdType` (仅支持 `ASIN`)
- **各创意场景与限制**:
  1. **Responsive eCommerce (`responsiveEcommerceSettings`)**:
     - `products`: `minItems: 1`, `maxItems: 20` (必须包含 **1 ~ 20 个** ASIN)。
  2. **Standard Audio (`standardAudioExperienceSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 10` (最多 10 个 ASIN)。
  3. **Streaming TV Video (`streamingTvSettings`)**:
     - `products`: `minItems: 0`, `maxItems: 20` (最多 20 个 ASIN)。
  4. **Online Video (`onlineVideoSettings`)**:
     - `products`: 单个 `DSPCreateAdvertisedProducts` 对象 (0 或 1 个 ASIN)。
  5. **Standard Display / Brand Store / Third Party**:
     - 无 `products` ASIN 字段。
- **批量请求限制**:
  - `DSPCreateAdRequest.ads`: `minItems: 1`, `maxItems: 10`

### 3.6 Sponsored Television (ST)
- **规范文件**: `codegen/v1/data/openapi/AmazonAdsAPISTMerged_prod_3p.json`
- **支持类型**: `STProductIdType` (`ASIN`, `SKU`)
- **核心结构**:
  - `creative.videoCreative.streamingTvSettings.products`: 数组 (`minItems: 0`, `maxItems: 1`)，支持 0 或 1 个 ASIN / SKU。
- **批量请求限制**:
  - `STCreateAdRequest.ads`: `minItems: 1`, `maxItems: 100`
