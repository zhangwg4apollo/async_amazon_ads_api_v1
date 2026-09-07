# Changelog

## Unreleased

## v0.10.1 (2026-09-07)

### refactor — 重构
- **代码生成器目录**: `script3/`、`script4/` 迁至 `codegen/v0/`、`codegen/v1/`。生成命令改为 `uv run python codegen/v0/generate.py` 与 `uv run python codegen/v1/generate.py`。
- **Reporting API (beta) 迁至 v1**: 指南与下载脚本从 `codegen/v0` 迁到 `codegen/v1`。Reports Contract 由 `download_openapi.py` 写入 `codegen/v1/data/openapi/`；markdown 仍由 `download_reporting_docs.py` 写入 `data/guides/`。

### feat — 新功能
- **v1 Reporting API (beta)**: 生成 `ads.v1.reports`（create / retrieve / delete report），模型在 `ads_api.models.v1.reports.general`。

### docs — 文档
- **对外身份**: README / 错误提示标明 PyPI 包名为 `async-amazon-ads-api-v1`、导入名为 `ads_api`；Redis extra 提示改为 `pip install async-amazon-ads-api-v1[redis]`。
- **枚举策略**: 文档与生成器说明改为实际输出（请求 `Literal`，响应 `Literal | str`），不再把 `lenient_enum` 写成生成模型形态。

## v0.10.0 (2026-09-07)

### breaking — 破坏性变更
- **移除旧包 `async_amazon_ads_api_v1` 与 `scripts/` 代码生成器**：SDK 仅保留 `ads_api`。已发布用户请锁定旧版本；新代码使用 `from ads_api import AdsClient`。

## v0.9.3 (2026-09-01)

### feat — 新功能
- **OAuth Token 刷新异常分类**: 新增 `TokenRefreshError` 与 `InvalidGrantError` 异常类。当 Refresh Token 已被撤销或失效（HTTP 400 `invalid_grant`）时精准抛出 `InvalidGrantError`，便于上层工作流立即终止无效重试。
- **导出错误类至 `ads_api.errors`**: 提供完整 SDK 异常层次结构。

## v0.9.2 (2026-09-01)

### feat — 新功能
- **AmazonAdsConfig 增加 account_type 配置**: 支持传入 `"seller"`, `"vendor"`, `"agency"` 等账号类型。
- **AdsClient 增加账号类型与上下文快捷属性**: 提供 `.config`, `.context`, `.account_type`, `.is_seller`, `.is_vendor`, `.is_agency` 等快捷属性，方便直接访问配置与判断账号身份。

## v0.9.1 (2026-09-01)

### feat — 新功能
- **v0 Products API**: 接入 Product metadata 与 Product eligibility，可通过 `ads.v0.products` 调用。
- **v0 Discovery API**: 接入 Locations 与 Targetable entities，可通过 `ads.v0.discovery` 调用。

### refactor — 重构
- **简化 TokenManager 的 token 获取**: `force` 时直接刷新；内存未命中才在锁内读 cache，避免 miss 时重复读取。

### chore — 杂项
- **sdist 排除 docs**: 发行包不再包含仓库内说明文档。

## v0.9.0 (2026-09-01)

### fix — 修复
- **Token 缓存不再写入 refresh_token**: 缓存只保存未过期的 `access_token`，刷新始终使用配置中的凭据，避免把 refresh_token 落到文件或 Redis。

### refactor — 重构
- **按字段推断 token 缓存**: `ads_api.AmazonAdsConfig` 按 `token_cache` / Redis / `token_cache_dir` 优先级自动选择缓存实现，不再依赖 `CacheBackend` 枚举。
- **移除 loader**: 删除未使用的 `from_toml` 与 `CacheBackend`。

## v0.6.13 (2026-09-01)

### feat — 新功能
- **v0 Portfolios API**: 接入 Portfolios（version 3），可通过 `ads.v0.portfolios` 调用 list / create / update / budget usage。
- **可选 requestBody**: OpenAPI 未标 `required: true` 的 requestBody 允许省略，不再强制传 body。
- **TokenManager 日志**: 补充 token 生命周期日志（缓存命中/未命中、强制刷新、刷新成功与失败），不记录 token 明文。

### breaking — 破坏性变更
- **接口默认返回 dict**: `ads_api` 客户端方法的 `mode` 默认值由 `"pydantic"` 改为 `"dict"`。需要 Pydantic 模型时请显式传入 `mode="pydantic"`。

## v0.6.12 (2026-08-31)

### feat — 新功能
- **同步最新 OpenAPI 规范**:
  - 同步官方 v1 Merged OpenAPI（ALL / DSP / SB / SP / ST）并重新生成 Client 与 Models。
  - 同步 Amazon Ads API v0（Ads Data Manager、Sponsored Products v3）规范。
- **v1 生成器跳过 deprecated 操作**: `script4` 忽略 OpenAPI 中 `deprecated: true` 的 operation（当前为 Commitments / CommitmentSpends 的 legacy `/dsp` 路径别名），避免把废弃接口挂到顶层客户端。
- **DSP Commitments / CommitmentSpends 正式路径**: 客户端改为调用产品无关 URL（如 `POST /adsApi/v1/retrieve/commitmentSpends`），不再使用 `/dsp` 后缀别名。
- **模型更新**: Commitment 增加 `adProduct`；DSP Ad Group query 增加 `inventoryTypeFilter`；若干字段描述与枚举说明同步官方 spec。

## v0.6.11 (2026-08-20)

### feat — 新功能
- **基于 Merged OpenAPI 重构 v1 代码生成器 (`script4`)**:
  - 接入官方 7 个 Merged OpenAPI 规范文件替代原先分散碎片文件。
  - 修正产品归属，将原本挂在顶层的 24 个实体正确归入 SB (12 个) 与 DSP (21 个) 命名空间。
  - 彻底废弃旧版 `script2`。
- **同步最新 OpenAPI 规范**:
  - 同步 2026-08-20 官方 OpenAPI v1 规范，重新生成全量 v1 Client 与 Models。
  - 同步 Amazon Ads API v0 (Ads Data Manager) 最新规范并更新数据模型。
- **Token 与重试机制增强**:
  - `TokenCache`: 优化生命周期管理与 Redis 客户端注入支持。
  - `RequestRunner`: 支持解析 HTTP `Retry-After` 响应头实现智能退避重试。
  - `TokenManager`: 支持 401 响应下强制刷新 Token (`force=True`)，避免缓存失效陷阱。

### fix — 修复
- **代码生成器 ID 类型修复**: 修复生成器将 ID 字段错误映射为 `float` 的问题，统一修正为 `int`。
- **瞬态网络异常重试**: 扩大网络瞬态抖动异常捕获范围，支持超时与连接重置自动重试。

### refactor — 重构
- **Python 3.13 语法升级**: 升级为 Python 3.13 PEP 695 泛型与类型别名语法。

### docs — 文档
- 新增各广告类型 ASIN/SKU 数量与规则限制中英文文档。

## v0.6.10 (2026-08-18)

### refactor — 重构
- **枚举全面迁移为 Literal 类型别名**:
  - 请求模型（Request Models）采用严格 `Literal` 校验，防止非法枚举参数传入并提供精准的 IDE 类型提示。
  - 响应模型（Response Models）采用 `Literal[...] | str` 联合类型，保留未知枚举值的向前兼容容忍（Forward Compatibility）。
  - 优化内联枚举逻辑，属性内联枚举直接在模型字段声明中内联 `Literal`，消除多余的枚举类定义与命名冲突。

### fix — 修复
- **生成器数组枚举校验修复**: 修复代码生成器对于请求模型中数组内枚举类型（如 `list[Literal[...]]`）在严格模式下的解析与类型声明。
- 重新基于优化后的生成器生成全量 `ads_api.v0` 与 `ads_api.v1` 客户端模型。

## v0.6.9 (2026-08-18)

### feat — 新功能
- **Sponsored Display (SD)**: 在 `ads_api.v0` 中引入全新的 Sponsored Display (`sd`) 全量客户端与数据模型（覆盖 ad_groups, bid_recommendations, brand_safety_list, budget_recommendations, budget_rules, budget_usage, campaigns, creatives, forecasts, headline_recommendations, locations_beta, negative_targeting, optimization_rules_beta, product_ads, reports, snapshots, targeting, targeting_recommendations 共 18 个子资源）。
- **生成器与类型优化**: 增强 v0 代码生成器对于复杂 schema 依赖解析、操作参数与共用模型的处理逻辑。

## v0.6.8 (2026-08-17)

### feat — 新功能
- **Sponsored Brands v4**: 在 `ads_api.v0` 中引入全新的 Sponsored Brands Version 4 (`sb_v4`) 全量客户端与数据模型（覆盖 ad_creatives, ad_groups, ads, budget_rules, budget_usage, campaigns, forecasts, insights, optimization_rules, product_targeting_categories, recommendations, v3_campaign_migration 共 12 个子资源）。
- **客户端架构优化**: `AdsClient` / `AdsClientV0` / `AdsClientV1` 统一基于共享 `ClientContext` 构建，支持资源间连接与 Token 管理的高效复用。
- **生成器优化**: v0 代码生成器支持默认值类型纠偏及操作参数级别的 Schema 依赖自动导入。

### refactor — 重构
- 统一客户端未传入必要配置时的异常处理，抛出规范的 `MissingConfigError`。

## v0.6.7 (2026-08-17)

### fix — 修复
- 修复 sdist 源码打包规则，排除 `script2`、`script3` 代码生成器与 spec 数据文件。

## v0.6.6 (2026-08-17)

### feat — 新功能
- 引入全新 `ads_api` 架构数据模型（支持 v0 与 v1 全实体及向前兼容）。
- 标记 `async_amazon_ads_api_v1` 为即将废弃状态，指导迁移至 `ads_api`。

## v0.6.0 (2026-07-08)

### feat — 新功能
- 基于 OpenAPI 规范重写所有 Legacy API，模型自动生成：
  - **SP BudgetRules**: 预算规则关联（创建、查询、更新、删除）
  - **SB BudgetRules**: 预算规则关联（创建、查询、更新、删除）
  - **SD BudgetRules**: 预算规则关联（创建、查询、更新、删除）
  - **SD Creatives**: 创意管理
  - **Portfolios**: 投资组合管理
- `generate_all.py` 集成所有 legacy 生成脚本，一键生成

### refactor — 重构
- `TokenManager` 直接判断 token 过期，不再依赖异常捕获
- 默认请求超时从 60s 提升到 600s
- 模型层移除所有 `import *`，改用显式子模块导入
- 清理已废弃的旧版 `BudgetRules` 客户端和模型
- 提取共享函数到 `scripts/_gen_utils.py`，消除代码重复
