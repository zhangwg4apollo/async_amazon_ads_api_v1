# Ads API v0 代码生成

从 toc2 的 **Amazon Ads API v0** 分组下载 OpenAPI，生成 `src/ads_api/client/v0` 与 `src/ads_api/models/v0`。runtime（`config` / `base` / `models/_core`）与 v1 共用 `src/ads_api`。

当前覆盖 **Accounts**、**Reporting**、**Ads data manager**、**Exports**、**Portfolios**（OpenAPI 3.0，叶子节点 → `portfolios`）、**Sponsored Products**（仅 Version 3 → `sp_v3`）、**Sponsored Brands**（仅 Version 4 → `sb_v4`）、**Sponsored Display**（仅一份 Campaign management spec → `sd`，不区分版本）。后续加 DSP / SP Version 2 等时，在 `codegen/spec.py` 的 `INCLUDED_TOC_SECTIONS`（及可选的 `INCLUDED_VERSIONS`）里加即可。实体名默认从 TOC 项名推断；只有不稳定的路径才写进 `ENTITY_OVERRIDES`。叶子 TOC 节点（无子项、自身带 `link`）作为单资源挂到 `AdsClientV0` 上。

## 命令

```bash
uv run python codegen/v0/download_openapi.py
uv run python codegen/v0/generate.py
```

`download_openapi.py` 自动从 Amazon Ads 文档下载 `toc2.json` 到 `codegen/v0/data/toc2.json`。

## 目录对应

| 输入 | 输出 |
|------|------|
| `data/api-spec-v0/<group>/<entity>/` | `src/ads_api/models/v0/<group>/<entity>.py` |
| 同上 | `src/ads_api/client/v0/<group>/<entity>.py` |
| TOC 项名为 `Version N` | 分组 `<product>_vN`（如 `sp_v3`、`sb_v4`），访问 `ads.v0.<product>_vN.<entity>` |
| TOC 项名（如 Profiles） | 实体 snake_case（`profiles`） |
| TOC 分组 Sponsored Products / Sponsored Brands / Sponsored Display | 产品前缀 `sp` / `sb` / `sd`（见 `GROUP_KEY_OVERRIDES`） |

Account management 一份 spec、两个资源 tag，会拆成 `advertising_accounts` + `terms_token`。Marketing Mix Modeling 拆成 `mmm_brand_groups` / `mmm_brand_group_overrides` / `mmm_reports`（`Reports` 与 Version 3 reporting 撞名时给兄弟 tag 加上父实体缩写前缀）。Ads data manager 按 tag 拆成 `audiences` / `data_rooms` 等。Exports / Portfolios 是叶子 TOC 节点，单资源直接挂在 `AdsClientV0.exports` / `AdsClientV0.portfolios`（Portfolios spec 含 Budget Usage tag，主 tag 与分组同名，不拆以免变成 `portfolios.portfolios`）。Sponsored Products Version 3 按 tag 拆到 `sp_v3/`；Sponsored Brands Version 4 按 tag 拆到 `sb_v4/`。Sponsored Display 只有 Campaign management 一份 spec（无 Version N），整份挂在 `sd/`，按 tag 拆成 `campaigns` / `ad_groups` 等。DSP Advertiser 的 OpenAPI 在 Amazon DSP 段，下载时用 v0 全局 `route → openapi` 索引补链。

## 访问

```python
from ads_api import AdsClient, AmazonAdsConfig, Region

async with AdsClient(config) as ads:
    await ads.v0.accounts.profiles.list_profiles()
    await ads.v0.accounts.advertising_accounts.list_ads_accounts(body)
    await ads.v0.reporting.reports.create_async_report(body)
    await ads.v0.ads_data_manager.audiences.list_audience_datasets()
    await ads.v0.exports.get_export(export_id, accept="application/vnd.campaignsexport.v1+json")
    await ads.v0.portfolios.list_portfolios(body)
    await ads.v0.sp_v3.campaigns.create_sponsored_products_campaigns(body)
    await ads.v0.sb_v4.campaigns.list_sponsored_brands_campaigns()
    await ads.v0.sd.campaigns.list_campaigns()
```

只需要 v0 时可用 `AdsClientV0(config)`。v1 的 `ads.v1.manager_accounts` 仍是 `/adsApi/v1/...`，互不影响。

## 与 v1 生成器的差异

- 实体名来自 TOC / route，不要求 OpenAPI 恰好 1 个 tag
- 相对 YAML 拼到 `https://d3a0d0y2hgofx6.cloudfront.net/openapi/en-us/`
- 无 `AmazonAdsAPI(ALL|SP|…)` 文件名前缀
- 请求体 `application/vnd.*+json` 写入 `Content-Type` / `Accept`
- 缺少 `operationId` 时用 HTTP method + path 生成方法名
- 无产品命名空间，按 TOC 分组挂在 `AdsClientV0` 上（`.accounts` / `.reporting` / `.ads_data_manager` / `.exports` / `.portfolios` / `.sp_v3` / `.sb_v4` / `.sd`）

## 生成器结构

```
codegen/v0/
  download_openapi.py
  generate.py
  codegen/
    spec.py      # TOC 分组白名单、实体名推断、YAML 规范化、operationId 回退
    schema.py    # 请求/响应闭包、Python 命名
    emit.py      # Pydantic + client；vendor media type
  data/api-spec-v0/<group>/<entity>/meta.json
  data/api-spec-v0/<product>_vN/meta.json   # Version N 产品 API，如 sp_v3
  data/api-spec-v0/<product>/meta.json      # 无版本产品 API，如 sd
```
