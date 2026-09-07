# Ads API v1 代码生成器 (基于 Merged OpenAPI)

从 `codegen/v1/data/openapi/` 的 7 个 Merged OpenAPI 规范文件自动生成 `src/ads_api/client/v1` 与 `src/ads_api/models/v1`。

使用 Amazon Ads 官方提供的 7 个 Merged OpenAPI 规范，下载快、数据完整，产品归属准确（正确归属 SB 和 DSP 实体）。

## 命令

```bash
# 1. 下载 Merged OpenAPI 规范
uv run python codegen/v1/download_openapi.py

# 2. 自动生成 v1 代码
uv run python codegen/v1/generate.py
```

## OpenAPI 规范映射

| 规范文件名 | 产品 | 模块 | 资源类前缀 | 模型前缀 |
|---|---|---|---|---|
| `AmazonAdsAPISPMerged_prod_3p.json` | SP | `sp` | `SP` | `SP` |
| `AmazonAdsAPISPGLOBALMerged_prod_3p.json` | SPGLOBAL | `sp_global` | `SPGlobal` | `SPGlobal` |
| `AmazonAdsAPISBMerged_prod_3p.json` | SB | `sb` | `SB` | `SB` |
| `AmazonAdsAPISDMerged_prod_3p.json` | SD | `sd` | `SD` | `SD` |
| `AmazonAdsAPIDSPMerged_prod_3p.json` | DSP | `dsp` | `DSP` | `DSP` |
| `AmazonAdsAPISTMerged_prod_3p.json` | ST | `st` | `ST` | `ST` |
| `AmazonAdsAPIALLMerged_prod_3p.json` | ALL | `general`（models）/ 顶层（client） | 无 | 无 |

## 目录结构对应

| 输入 | 输出 |
|---|---|
| 各产品 Merged spec 中的 OpenAPI `tags`（如 `Campaigns`） | `src/ads_api/models/v1/<entity>/<product>.py` |
| 各广告产品（SP/SB/SD/DSP/ST/SPGLOBAL） | `src/ads_api/client/v1/<product>/<entity>.py` |
| ALL 中未被具体广告产品覆盖的通用操作 | `src/ads_api/client/v1/<entity>.py`（直接挂在 `AdsClientV1` 顶层） |
| 同一产品下跨实体共享的 Model | `src/ads_api/models/v1/_shared/<product>.py` |

## 模型与客户端规则

- **请求严格 / 响应向前兼容**：
  - 请求（INPUT）：`StrictModel` (`extra="forbid"`)，枚举为 `type X = Literal[...]`，非法值拒绝。
  - 响应（OUTPUT）：`LenientModel` (`extra="allow"`)，枚举字段为 `X | str`，未知值保留为 `str`。运行时用 `model_validate_json` 解析。
- **客户端挂载方式**：
  - 广告产品接口通过产品命名空间访问，如 `ads.v1.sp.campaigns`、`ads.v1.sb.advertising_deals`、`ads.v1.dsp.commitments`。
  - 无产品归属的通用接口直接挂在 `AdsClientV1` 顶层，如 `ads.v1.selling_accounts`、`ads.v1.brand_stores`。
