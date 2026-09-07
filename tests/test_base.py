from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, call, patch

import httpx
import pytest
from pydantic import BaseModel

from ads_api.base import BaseResource, ClientContext, _parse_retry_after
from ads_api.config.settings import AmazonAdsConfig


class DummyModel(BaseModel):
    name: str
    value: int


class DummyDateModel(BaseModel):
    startDateTime: datetime  # noqa: N815 - Amazon API 字段使用 camelCase
    note: str | None = None


class TestClientContext:
    @pytest.mark.asyncio
    async def test_get_client_lazy_init(self, config: AmazonAdsConfig) -> None:
        ctx = ClientContext(config)
        assert ctx._client is None
        client = await ctx.get_client()
        assert client is not None
        assert client is ctx._client

    @pytest.mark.asyncio
    async def test_get_client_base_url(self, config: AmazonAdsConfig) -> None:
        ctx = ClientContext(config)
        client = await ctx.get_client()
        assert str(client.base_url) == "https://advertising-api.amazon.com"

    @pytest.mark.asyncio
    async def test_get_client_cached(self, config: AmazonAdsConfig) -> None:
        ctx = ClientContext(config)
        c1 = await ctx.get_client()
        c2 = await ctx.get_client()
        assert c1 is c2


class TestBaseResource:
    @pytest.fixture
    def resource(self, config: AmazonAdsConfig) -> BaseResource:
        return BaseResource(ClientContext(config))

    def test_dump_json_none_is_empty_object(self, resource: BaseResource) -> None:
        assert resource.dump_json(None) == {}

    def test_dump_json_model(self, resource: BaseResource) -> None:
        assert resource.dump_json(DummyModel(name="a", value=1)) == {"name": "a", "value": 1}

    def test_dump_json_sequence(self, resource: BaseResource) -> None:
        dumped = resource.dump_json([DummyModel(name="a", value=1), DummyModel(name="b", value=2)])
        assert dumped == [{"name": "a", "value": 1}, {"name": "b", "value": 2}]

    def test_dump_json_uses_json_mode(self, resource: BaseResource) -> None:
        dumped = resource.dump_json([DummyDateModel(startDateTime=datetime(2026, 6, 8, tzinfo=UTC))])
        assert dumped == [{"startDateTime": "2026-06-08T00:00:00Z"}]

    def test_response_default_is_dict(self, resource: BaseResource) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.json.return_value = {"name": "test", "value": 123}
        result = resource._response(DummyModel, resp)
        assert isinstance(result, dict)
        assert result == {"name": "test", "value": 123}

    def test_response_pydantic_mode(self, resource: BaseResource) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.text = '{"name": "test", "value": 123}'
        result = resource._response(DummyModel, resp, mode="pydantic")
        assert isinstance(result, DummyModel)
        assert result.name == "test"
        assert result.value == 123

    def test_response_dict_mode(self, resource: BaseResource) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.json.return_value = {"name": "test", "value": 123}
        result = resource._response(DummyModel, resp, mode="dict")
        assert isinstance(result, dict)
        assert result == {"name": "test", "value": 123}

    def test_response_raw_mode(self, resource: BaseResource) -> None:
        resp = MagicMock(spec=httpx.Response)
        result = resource._response(DummyModel, resp, mode="raw")
        assert result is resp

    def test_response_list_default_is_dict(self, resource: BaseResource) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.json.return_value = [{"name": "item1", "value": 1}]
        result = resource._response_list(DummyModel, resp)
        assert isinstance(result, list)
        assert result == [{"name": "item1", "value": 1}]

    def test_response_list_pydantic_mode(self, resource: BaseResource) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.text = '[{"name": "item1", "value": 1}, {"name": "item2", "value": 2}]'
        result = resource._response_list(DummyModel, resp, mode="pydantic")
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], DummyModel)
        assert result[0].name == "item1"
        assert result[1].value == 2

    def test_response_list_dict_mode(self, resource: BaseResource) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.json.return_value = [{"name": "item1", "value": 1}]
        result = resource._response_list(DummyModel, resp, mode="dict")
        assert isinstance(result, list)
        assert result == [{"name": "item1", "value": 1}]

    def test_response_list_raw_mode(self, resource: BaseResource) -> None:
        resp = MagicMock(spec=httpx.Response)
        result = resource._response_list(DummyModel, resp, mode="raw")
        assert result is resp

    @pytest.mark.asyncio
    async def test_request_retry_on_401_with_force_refresh(self, resource: BaseResource) -> None:
        resource._ctx.config._token_manager = MagicMock()
        auth_error_resp = MagicMock(spec=httpx.Response)
        auth_error_resp.status_code = 401
        auth_error_resp.is_error = True
        auth_error_resp.text = "Unauthorized"

        ok_resp = MagicMock(spec=httpx.Response)
        ok_resp.status_code = 200
        ok_resp.is_error = False

        mock_client = MagicMock(spec=httpx.AsyncClient)
        mock_client.request = AsyncMock(side_effect=[auth_error_resp, ok_resp])

        with (
            patch.object(ClientContext, "get_client", AsyncMock(return_value=mock_client)),
            patch.object(
                AmazonAdsConfig, "refresh_access_token", AsyncMock(return_value="refreshed-token")
            ) as mock_refresh,
        ):
            resp = await resource._request("GET", "/test")

        assert resp.status_code == 200
        assert mock_refresh.await_args_list == [call(), call(force=True)]
        assert mock_client.request.call_count == 2

    @pytest.mark.asyncio
    async def test_request_retry_on_429_with_retry_after(self, resource: BaseResource) -> None:
        rate_limit_resp = MagicMock(spec=httpx.Response)
        rate_limit_resp.status_code = 429
        rate_limit_resp.is_error = True
        rate_limit_resp.headers = {"Retry-After": "3"}

        ok_resp = MagicMock(spec=httpx.Response)
        ok_resp.status_code = 200
        ok_resp.is_error = False

        mock_client = MagicMock(spec=httpx.AsyncClient)
        mock_client.request = AsyncMock(side_effect=[rate_limit_resp, ok_resp])

        with (
            patch.object(ClientContext, "get_client", AsyncMock(return_value=mock_client)),
            patch("asyncio.sleep", AsyncMock()) as mock_sleep,
        ):
            resp = await resource._request("GET", "/test")

        assert resp.status_code == 200
        assert mock_sleep.await_count == 1
        assert mock_sleep.await_args is not None
        slept = mock_sleep.await_args.args[0]
        assert 3.0 <= slept <= 3.5

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "transient_error",
        [
            httpx.ConnectError("Connection refused"),
            httpx.ReadTimeout("The read operation timed out"),
            httpx.ConnectTimeout("The connection timed out"),
            httpx.RemoteProtocolError("Server disconnected unexpectedly"),
        ],
    )
    async def test_request_retry_on_transient_network_errors(
        self, resource: BaseResource, transient_error: Exception
    ) -> None:
        ok_resp = MagicMock(spec=httpx.Response)
        ok_resp.status_code = 200
        ok_resp.is_error = False

        mock_client = MagicMock(spec=httpx.AsyncClient)
        mock_client.request = AsyncMock(side_effect=[transient_error, ok_resp])

        with (
            patch.object(ClientContext, "get_client", AsyncMock(return_value=mock_client)),
            patch("asyncio.sleep", AsyncMock()) as mock_sleep,
        ):
            resp = await resource._request("GET", "/test")

        assert resp.status_code == 200
        assert mock_client.request.call_count == 2
        assert mock_sleep.await_count == 1


class TestParseRetryAfter:
    def test_delta_seconds(self) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.headers = {"Retry-After": "5"}
        result = _parse_retry_after(resp, fallback_seconds=1.0)
        assert 5.0 <= result <= 5.5

    def test_delta_seconds_float(self) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.headers = {"Retry-After": "2.5"}
        result = _parse_retry_after(resp, fallback_seconds=1.0)
        assert 2.5 <= result <= 3.0

    def test_missing_header_uses_fallback(self) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.headers = {}
        result = _parse_retry_after(resp, fallback_seconds=3.0)
        assert result == 3.0

    def test_invalid_header_uses_fallback(self) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.headers = {"Retry-After": "not-a-valid-value"}
        result = _parse_retry_after(resp, fallback_seconds=4.0)
        assert result == 4.0

    def test_max_wait_cap(self) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.headers = {"Retry-After": "1000"}
        result = _parse_retry_after(resp, fallback_seconds=1.0, max_wait=30.0)
        assert result == 30.0

    def test_http_date_format(self) -> None:
        import email.utils
        from datetime import timedelta

        future = datetime.now(UTC) + timedelta(seconds=10)
        date_str = email.utils.format_datetime(future)

        resp = MagicMock(spec=httpx.Response)
        resp.headers = {"Retry-After": date_str}
        result = _parse_retry_after(resp, fallback_seconds=1.0)
        assert 9.0 <= result <= 11.0
