from __future__ import annotations

import httpx
import pytest

from ads_api.errors import (
    STATUS_CODE_ERROR_MAP,
    AmazonAdsAPIError,
    AmazonAdsError,
    BadRequestError,
    ConfigurationError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    InvalidGrantError,
    MissingConfigError,
    NotFoundError,
    RateLimitError,
    TokenRefreshError,
    UnauthorizedError,
    UnprocessableEntityError,
    raise_for_status,
)
from ads_api.models.v1._shared.general import Error, ErrorsIndex


class TestExceptionHierarchy:
    def test_missing_config_is_configuration_error(self) -> None:
        err = MissingConfigError()
        assert isinstance(err, ConfigurationError)
        assert isinstance(err, AmazonAdsError)
        assert isinstance(err, ValueError)
        assert str(err) == "Either 'config' or 'ctx' must be provided."

    def test_invalid_grant_is_token_refresh_error(self) -> None:
        err = InvalidGrantError(error_description="revoked")
        assert isinstance(err, TokenRefreshError)
        assert isinstance(err, AmazonAdsError)
        assert err.error_code == "invalid_grant"
        assert "invalid_grant" in str(err)

    def test_status_code_map(self) -> None:
        assert STATUS_CODE_ERROR_MAP[400] is BadRequestError
        assert STATUS_CODE_ERROR_MAP[401] is UnauthorizedError
        assert STATUS_CODE_ERROR_MAP[403] is ForbiddenError
        assert STATUS_CODE_ERROR_MAP[404] is NotFoundError
        assert STATUS_CODE_ERROR_MAP[409] is ConflictError
        assert STATUS_CODE_ERROR_MAP[422] is UnprocessableEntityError
        assert STATUS_CODE_ERROR_MAP[429] is RateLimitError
        assert STATUS_CODE_ERROR_MAP[500] is InternalServerError


class TestRaiseForStatus:
    def test_success_is_noop(self) -> None:
        resp = httpx.Response(200, json={"ok": True})
        raise_for_status(resp)

    def test_maps_status_to_typed_error(self) -> None:
        resp = httpx.Response(401, json={"message": "no auth"})
        with pytest.raises(UnauthorizedError) as exc_info:
            raise_for_status(resp)
        assert exc_info.value.status_code == 401
        assert "no auth" in str(exc_info.value)

    def test_unknown_status_uses_base_api_error(self) -> None:
        resp = httpx.Response(418, json={"message": "teapot"})
        with pytest.raises(AmazonAdsAPIError) as exc_info:
            raise_for_status(resp)
        assert type(exc_info.value) is AmazonAdsAPIError
        assert exc_info.value.status_code == 418


class TestErrorModels:
    def test_error_known_code(self) -> None:
        err = Error(code="BAD_REQUEST", message="bad")
        assert err.code == "BAD_REQUEST"
        assert err.message == "bad"
        assert err.fieldLocation is None

    def test_error_unknown_code_kept_as_str(self) -> None:
        err = Error(code="UNKNOWN_CODE", message="x")
        assert err.code == "UNKNOWN_CODE"

    def test_errors_index(self) -> None:
        ei = ErrorsIndex(errors=[Error(code="BAD_REQUEST", message="e1")], index=0)
        assert len(ei.errors) == 1
        assert ei.index == 0
