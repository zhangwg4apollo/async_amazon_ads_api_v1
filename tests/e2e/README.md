# ads_v1 e2e 行为契约测试

> 目的：验证 `ads_api` SDK 通过真实 HTTP 调用 `ads_v1_server` 时，是否符合 Amazon Ads API v1 的业务行为契约。测试完成标准不是“接口不报错”，而是请求上下文、状态码、错误格式、资源隔离、MultiStatus、过滤和删除语义都与模拟器记录的 Amazon 行为一致。

## 参考来源

- `/Users/jack/codex/ads_v1_server/docs/amazon-behavior/resources.md`
- `/Users/jack/codex/ads_v1_server/docs/amazon-behavior/token-endpoint.md`
- `/Users/jack/codex/ads_v1_server/docs/amazon-behavior/token-profile-relationship.md`
- `/Users/jack/codex/ads_v1_server/tests/test_ads_v1_contract.py`
- `/Users/jack/codex/ads_v1_server/tests/test_ads_v1_sdk_integration.py`

## 测试边界

e2e 测试只从 `ads_v1` SDK 侧发起请求，不导入 `ads_v1_server` 的 Python 模块。

默认目标服务：

```text
ADS_V1_E2E_BASE_URL=http://127.0.0.1:8000
```

默认使用 `ads_v1_server` seed 数据：

```text
client_id=amzn1.application-oa2-client.seedclient00001
refresh_token=Atzr|seed_refresh_token_002
profile_id=111111115
```

## 规划目录

```text
tests/e2e/
├── README.md                    # e2e 目标、边界、跑法
├── PROGRESS.md                  # 执行进度跟踪
├── conftest.py                  # e2e fixtures：健康检查、配置、唯一数据
├── config.py                    # seed 配置与环境变量读取
├── test_sp_campaigns.py         # SP campaigns 行为契约
├── test_sp_ad_groups.py         # 父子资源关系，后续阶段
└── reporting/                   # 可选：后续沉淀 findings
```

## 分层设计

```text
Layer 1: 环境与配置
  检查 ads_v1_server /health；服务不可用时跳过 e2e。

Layer 2: 协议与鉴权
  验证 refresh token、client id、profile scope、错误格式。

Layer 3: 资源行为契约
  验证 create/query/update/delete 的响应模型和业务语义。

Layer 4: 隔离与关系
  验证 profile 隔离、父子资源必须同 profile。

Layer 5: 报告与进度
  用 PROGRESS.md 跟踪阶段、结论、阻塞和遗留偏差。
```

## 首批覆盖项

### SP campaigns 生命周期

- `create` 返回 MultiStatus 模型，成功项包含 `campaign` 和 `index`。
- 响应使用 `campaignId`，不使用通用 `id`。
- campaign monetary budget 响应按 profile 货币补齐 `currencyCode`。
- `query` 返回 `campaigns` 和 `nextToken`。
- `campaignIdFilter`、`stateFilter`、`adProductFilter` 能正确过滤。
- `update` 返回 MultiStatus，并且后续 query 能看到字段持久化。
- `delete` 返回 MultiStatus，并将资源状态更新为 `ARCHIVED`。
- delete 后资源仍可通过 `stateFilter=ARCHIVED` 查询到。

### 负向契约

- 缺失 `Amazon-Ads-ClientId` 返回 Amazon Ads 错误体。
- `Amazon-Ads-ClientId` 与 access token 不匹配时返回 `UNAUTHORIZED`。
- 非数字 `Amazon-Advertising-API-Scope` 返回 `BAD_REQUEST`。
- 不可访问 profile 返回 profile 访问错误，而不是泄漏其他 profile 数据。

## 跑法

前置：启动并 seed `ads_v1_server`。

```bash
cd /Users/jack/codex/ads_v1_server
uv run --frozen ads-db reset
uv run --frozen ads-db seed
uv run --frozen uvicorn ads_v1_server.main:app --host 127.0.0.1 --port 8000
```

执行 e2e：

```bash
cd /Users/jack/codex/ads_v1
uv run --frozen pytest tests/e2e -v
```

或使用 marker：

```bash
uv run --frozen pytest -m e2e -v
```

可选环境变量：

```bash
ADS_V1_E2E_BASE_URL=http://127.0.0.1:8000 \
ADS_V1_E2E_PROFILE_ID=111111115 \
uv run --frozen pytest tests/e2e -v
```

## 完成标准

- 所有 e2e 用例通过。
- 每个用例至少验证一个明确的 Amazon 行为契约。
- 不以“HTTP 200/207 不报错”作为唯一断言。
- 对已知模拟器偏差，要在 `PROGRESS.md` 标记为偏差或后续任务。
- 新增测试运行前后不要求清空数据库；测试数据使用唯一名称，删除阶段归档清理。
