"""Offline HTTP contract tests for version 1.0 strict defaults and compatibility mode.

Documents the version 1.0 HTTP behavior in deterministic tests. Unimplemented
1.0 default wiring is marked xfail pending issue #284.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest
import requests

from mlbstatsapi import (
    Mlb,
    MlbDataAdapter,
    MlbDecodeError,
    MlbHttpError,
    MlbResult,
    MlbTimeoutError,
    MlbTransportError,
    TheMlbStatsApiException,
)
from mlbstatsapi.mlb_dataadapter import DEFAULT_TIMEOUT

from http_contract_support import (
    API_VERSIONS,
    COMPATIBILITY_CLIENT_ERRORS,
    HTTP_REASON_BY_STATUS,
    NOT_FOUND_STATUS,
    SERVER_ERRORS,
    XFAIL_PENDING_STRICT_DEFAULT,
    adapter_for_api_version,
    assert_library_retry_policy,
    standalone_adapter_for_version,
)

# Non-404 client errors asserted under strict mode (final 429 covered in retries).
STRICT_NON_404_CLIENT_ERRORS = tuple(
    code for code in COMPATIBILITY_CLIENT_ERRORS if code != 429
)


def _response(
    *,
    status_code: int,
    reason: str,
    url: str,
    content: bytes = b"",
    payload=None,
    text: str | None = None,
):
    """Build a fake requests Response for offline adapter tests."""
    response = MagicMock()
    response.status_code = status_code
    response.reason = reason
    response.url = url
    response.content = content
    if text is not None:
        response.text = text
    elif content:
        response.text = content.decode("utf-8", errors="replace")
    else:
        response.text = ""
    if payload is None:
        response.json.side_effect = ValueError("no json")
    else:
        response.json.return_value = payload
    return response


class RecordingSession:
    """Minimal session stand-in that records get() and close() calls."""

    def __init__(self):
        self.calls = []
        self.close_calls = 0
        self.headers = requests.structures.CaseInsensitiveDict()

    def get(self, url, params=None, timeout=None, **kwargs):
        self.calls.append(
            {
                "url": url,
                "params": params,
                "timeout": timeout,
                "kwargs": kwargs,
            }
        )
        return _response(
            status_code=200,
            reason="OK",
            url=url,
            content=b'{"sports": []}',
            payload={"sports": []},
        )

    def close(self):
        self.close_calls += 1


# --- Status matrices remain available for later strict-mode work ---


def test_status_matrices_document_compatibility_baseline():
    """Keep the shared status groups stable for contract and retry tests."""
    assert COMPATIBILITY_CLIENT_ERRORS == (400, 401, 403, 405, 409, 422, 429)
    assert STRICT_NON_404_CLIENT_ERRORS == (400, 401, 403, 405, 409, 422)
    assert NOT_FOUND_STATUS == 404
    assert SERVER_ERRORS == (500, 502, 503, 504)
    assert 404 not in COMPATIBILITY_CLIENT_ERRORS
    assert 409 in COMPATIBILITY_CLIENT_ERRORS
    assert 429 in COMPATIBILITY_CLIENT_ERRORS
    assert set(SERVER_ERRORS).isdisjoint(COMPATIBILITY_CLIENT_ERRORS)


# --- Version 1.0 default strict wiring (pending implementation #284) ---


@XFAIL_PENDING_STRICT_DEFAULT
def test_mlb_default_matches_explicit_strict_mode_wiring():
    """Mlb() must default to strict mode on the client and both adapters."""
    mlb = Mlb()
    try:
        assert mlb._strict_http is True
        assert mlb._mlb_adapter_v1._strict_http is True
        assert mlb._mlb_adapter_v1_1._strict_http is True
    finally:
        mlb.close()


@XFAIL_PENDING_STRICT_DEFAULT
def test_mlb_data_adapter_default_is_strict():
    """MlbDataAdapter() must default to strict HTTP in version 1.0."""
    adapter = MlbDataAdapter()
    try:
        assert adapter._strict_http is True
    finally:
        adapter.close()


def test_mlb_explicit_compatibility_mode_wiring():
    """Mlb(strict_http=False) keeps compatibility mode on both adapters."""
    mlb = Mlb(strict_http=False)
    try:
        assert mlb._strict_http is False
        assert mlb._mlb_adapter_v1._strict_http is False
        assert mlb._mlb_adapter_v1_1._strict_http is False
    finally:
        mlb.close()


def test_mlb_explicit_strict_mode_wires_both_adapters():
    """Mlb(strict_http=True) enables strict mode on both internal adapters."""
    mlb = Mlb(strict_http=True)
    try:
        assert mlb._strict_http is True
        assert mlb._mlb_adapter_v1._strict_http is True
        assert mlb._mlb_adapter_v1_1._strict_http is True
    finally:
        mlb.close()


@pytest.mark.parametrize("api_version", API_VERSIONS)
def test_explicit_strict_mode_wires_both_api_versions(api_version):
    """strict_http=True applies to standalone v1 and v1.1 adapters."""
    adapter = MlbDataAdapter(ver=api_version, strict_http=True)
    try:
        assert adapter._strict_http is True
    finally:
        adapter.close()


@pytest.mark.parametrize("api_version", API_VERSIONS)
def test_explicit_compatibility_mode_wires_both_api_versions(api_version):
    """strict_http=False applies to standalone v1 and v1.1 adapters."""
    adapter = MlbDataAdapter(ver=api_version, strict_http=False)
    try:
        assert adapter._strict_http is False
    finally:
        adapter.close()


# --- Explicit compatibility mode: empty MlbResult, no MlbHttpError ---


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("status_code", COMPATIBILITY_CLIENT_ERRORS)
def test_compatibility_client_errors_return_empty_mlb_result(
    api_version,
    status_code,
):
    """Non-404 4xx responses return an empty MlbResult in compatibility mode."""
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = f"https://statsapi.mlb.com/api/{api_version}/sports"
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
    )
    mlb = Mlb(session=session, strict_http=False)
    adapter = adapter_for_api_version(mlb, api_version)

    result = adapter.get(endpoint="sports")

    assert isinstance(result, MlbResult)
    assert result.status_code == status_code
    assert result.data == {}


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("status_code", COMPATIBILITY_CLIENT_ERRORS)
def test_compatibility_client_errors_do_not_raise_mlb_http_error(
    api_version,
    status_code,
):
    """Compatibility-mode client errors must not raise MlbHttpError."""
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = f"https://statsapi.mlb.com/api/{api_version}/sports"
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
    )
    adapter = standalone_adapter_for_version(
        session,
        api_version,
        strict_http=False,
    )

    result = adapter.get(endpoint="sports")

    assert result.status_code == status_code
    assert result.data == {}


# --- Version 1.0 default: final non-404 4xx raises (pending #284) ---


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("status_code", COMPATIBILITY_CLIENT_ERRORS)
@XFAIL_PENDING_STRICT_DEFAULT
def test_default_adapter_raises_on_final_non_404_client_error(
    api_version,
    status_code,
):
    """Default MlbDataAdapter() raises MlbHttpError for final non-404 4xx."""
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = f"https://statsapi.mlb.com/api/{api_version}/sports"
    payload = {"error": reason}
    body = json.dumps(payload).encode("utf-8")
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
        content=body,
        payload=payload,
    )
    adapter = standalone_adapter_for_version(session, api_version)

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert isinstance(exc, TheMlbStatsApiException)
    assert exc.status_code == status_code
    assert exc.reason == reason
    assert exc.url == url
    assert exc.method == "GET"
    assert exc.response_data == payload
    assert exc.body_excerpt is not None


@pytest.mark.parametrize("status_code", COMPATIBILITY_CLIENT_ERRORS)
@XFAIL_PENDING_STRICT_DEFAULT
def test_default_mlb_raises_on_final_non_404_client_error(status_code):
    """Default Mlb() raises MlbHttpError for final non-404 4xx."""
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = "https://statsapi.mlb.com/api/v1/sports"
    payload = {"message": "client error", "code": status_code}
    body = json.dumps(payload).encode("utf-8")
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
        content=body,
        payload=payload,
    )
    mlb = Mlb(session=session)

    with pytest.raises(MlbHttpError) as exc_info:
        mlb._mlb_adapter_v1.get(endpoint="sports")

    exc = exc_info.value
    assert isinstance(exc, TheMlbStatsApiException)
    assert exc.status_code == status_code
    assert exc.reason == reason
    assert exc.url == url
    assert exc.method == "GET"
    assert exc.response_data == payload
    assert exc.body_excerpt is not None
    assert "client error" in exc.body_excerpt


# --- Strict non-404 4xx raises enriched MlbHttpError ---


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("status_code", STRICT_NON_404_CLIENT_ERRORS)
def test_strict_non_404_client_errors_raise_enriched_mlb_http_error(
    api_version,
    status_code,
):
    """Strict mode raises MlbHttpError with richer context for non-404 4xx."""
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = f"https://statsapi.mlb.com/api/{api_version}/sports"
    payload = {"message": "client error", "code": status_code}
    body = json.dumps(payload).encode("utf-8")
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
        content=body,
        payload=payload,
    )
    mlb = Mlb(session=session, strict_http=True)
    adapter = adapter_for_api_version(mlb, api_version)

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert isinstance(exc, TheMlbStatsApiException)
    assert exc.status_code == status_code
    assert exc.reason == reason
    assert exc.url == url
    assert exc.method == "GET"
    assert exc.response_data == payload
    assert exc.body_excerpt is not None
    assert "client error" in exc.body_excerpt


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("status_code", STRICT_NON_404_CLIENT_ERRORS)
def test_strict_adapter_non_404_client_errors_raise_mlb_http_error(
    api_version,
    status_code,
):
    """Standalone adapters honor strict_http for non-404 4xx responses."""
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = f"https://statsapi.mlb.com/api/{api_version}/sports"
    payload = {"error": reason}
    body = json.dumps(payload).encode("utf-8")
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
        content=body,
        payload=payload,
    )
    adapter = standalone_adapter_for_version(
        session,
        api_version,
        strict_http=True,
    )

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.status_code == status_code
    assert exc.reason == reason
    assert exc.url == url
    assert exc.method == "GET"
    assert exc.response_data == payload
    assert exc.body_excerpt is not None


# --- Endpoint-specific 404 return shapes via public Mlb methods ---


def _mlb_for_strict_http(session, strict_http):
    if strict_http == "default":
        return Mlb(session=session)
    return Mlb(session=session, strict_http=strict_http)


@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_mlb_get_person_404_returns_none(strict_http):
    """Single-object endpoints keep returning None on 404."""
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url="https://statsapi.mlb.com/api/v1/people/999999",
    )
    mlb = _mlb_for_strict_http(session, strict_http)

    assert mlb.get_person(999999) is None


@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_mlb_get_teams_404_returns_empty_list(strict_http):
    """Collection endpoints keep returning an empty list on 404."""
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url="https://statsapi.mlb.com/api/v1/teams",
    )
    mlb = _mlb_for_strict_http(session, strict_http)

    assert mlb.get_teams() == []


@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_mlb_get_player_stats_404_returns_empty_mapping(strict_http):
    """Mapping endpoints keep returning an empty dict on 404."""
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url="https://statsapi.mlb.com/api/v1/people/999999/stats",
    )
    mlb = _mlb_for_strict_http(session, strict_http)

    assert mlb.get_player_stats(999999, ["season"], ["hitting"]) == {}


@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_mlb_endpoint_404_does_not_raise_mlb_http_error(strict_http):
    """Public 404 handling stays domain-level empty results, not MlbHttpError."""
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url="https://statsapi.mlb.com/api/v1/people/999999",
    )
    mlb = _mlb_for_strict_http(session, strict_http)

    assert mlb.get_person(999999) is None
    assert mlb.get_teams() == []
    assert mlb.get_player_stats(999999, ["season"], ["hitting"]) == {}


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("strict_http", [False, True])
def test_404_preserves_endpoint_shapes_in_both_modes(api_version, strict_http):
    """404 keeps None / [] / {} endpoint shapes in compatibility and strict modes."""
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url=f"https://statsapi.mlb.com/api/{api_version}/people/999999",
    )
    mlb = Mlb(session=session, strict_http=strict_http)

    assert mlb.get_person(999999) is None
    assert mlb.get_teams() == []
    assert mlb.get_player_stats(999999, ["season"], ["hitting"]) == {}


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_adapter_404_returns_mlb_result_in_all_modes(api_version, strict_http):
    """Adapters return a 404 MlbResult rather than raising in any HTTP mode."""
    url = f"https://statsapi.mlb.com/api/{api_version}/people/999999"
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url=url,
    )
    if strict_http == "default":
        adapter = standalone_adapter_for_version(session, api_version)
    else:
        adapter = standalone_adapter_for_version(
            session,
            api_version,
            strict_http=strict_http,
        )

    result = adapter.get(endpoint="people/999999")

    assert isinstance(result, MlbResult)
    assert result.status_code == NOT_FOUND_STATUS
    assert result.data == {}


# --- Final 5xx raises MlbHttpError with existing attributes ---


@pytest.mark.parametrize("status_code", SERVER_ERRORS)
def test_mlb_server_errors_raise_mlb_http_error_with_existing_attributes(status_code):
    """Persistent 5xx failures raise MlbHttpError with status_code, reason, and url."""
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = "https://statsapi.mlb.com/api/v1/people/664034"
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
    )
    mlb = Mlb(session=session)

    with pytest.raises(MlbHttpError) as exc_info:
        mlb.get_person(664034)

    exc = exc_info.value
    assert isinstance(exc, TheMlbStatsApiException)
    assert exc.status_code == status_code
    assert exc.reason == reason
    assert exc.url == url
    # Protect useful message content without freezing the full exception string;
    # issue #268 may enrich MlbHttpError while keeping these attributes.
    assert str(status_code) in str(exc)
    assert reason in str(exc)


@pytest.mark.parametrize("status_code", [500, 502])
@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_server_errors_raise_enriched_mlb_http_error_in_all_modes(
    status_code,
    api_version,
    strict_http,
):
    """Final 5xx responses raise enriched MlbHttpError in every HTTP mode."""
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = f"https://statsapi.mlb.com/api/{api_version}/sports"
    payload = {"message": "server error", "status": status_code}
    body = json.dumps(payload).encode("utf-8")
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
        content=body,
        payload=payload,
    )
    if strict_http == "default":
        mlb = Mlb(session=session)
    else:
        mlb = Mlb(session=session, strict_http=strict_http)
    adapter = adapter_for_api_version(mlb, api_version)

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.status_code == status_code
    assert exc.reason == reason
    assert exc.url == url
    assert exc.method == "GET"
    assert exc.response_data == payload
    assert exc.body_excerpt is not None
    assert "server error" in exc.body_excerpt


# --- Transport and decode errors are independent of compatibility mode ---


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_timeout_raises_mlb_timeout_error(api_version, strict_http):
    """Timeouts raise MlbTimeoutError in every HTTP mode."""
    original = requests.exceptions.Timeout("timed out")
    session = MagicMock()
    session.get.side_effect = original
    if strict_http == "default":
        adapter = standalone_adapter_for_version(session, api_version)
    else:
        adapter = standalone_adapter_for_version(
            session,
            api_version,
            strict_http=strict_http,
        )

    with pytest.raises(MlbTimeoutError, match=r"^Request failed$") as exc_info:
        adapter.get(endpoint="sports")

    assert isinstance(exc_info.value, MlbTransportError)
    assert not isinstance(exc_info.value, MlbHttpError)
    assert exc_info.value.__cause__ is original


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_connection_failure_raises_mlb_transport_error(api_version, strict_http):
    """Connection failures raise MlbTransportError in every HTTP mode."""
    original = requests.exceptions.ConnectionError("connection refused")
    session = MagicMock()
    session.get.side_effect = original
    if strict_http == "default":
        adapter = standalone_adapter_for_version(session, api_version)
    else:
        adapter = standalone_adapter_for_version(
            session,
            api_version,
            strict_http=strict_http,
        )

    with pytest.raises(MlbTransportError, match=r"^Request failed$") as exc_info:
        adapter.get(endpoint="sports")

    assert not isinstance(exc_info.value, MlbTimeoutError)
    assert not isinstance(exc_info.value, MlbHttpError)
    assert exc_info.value.__cause__ is original


@pytest.mark.parametrize("api_version", API_VERSIONS)
@pytest.mark.parametrize("strict_http", ["default", False, True])
def test_invalid_json_raises_mlb_decode_error(api_version, strict_http):
    """Malformed successful JSON raises MlbDecodeError in every HTTP mode."""
    url = f"https://statsapi.mlb.com/api/{api_version}/sports"
    session = MagicMock()
    session.get.return_value = _response(
        status_code=200,
        reason="OK",
        url=url,
        content=b'{"bad": json',
        text='{"bad": json',
    )
    session.get.return_value.json.side_effect = ValueError("Expecting value")
    if strict_http == "default":
        adapter = standalone_adapter_for_version(session, api_version)
    else:
        adapter = standalone_adapter_for_version(
            session,
            api_version,
            strict_http=strict_http,
        )

    with pytest.raises(MlbDecodeError, match=r"^Bad JSON in response$") as exc_info:
        adapter.get(endpoint="sports")

    assert not isinstance(exc_info.value, MlbHttpError)


# --- Library-created retry policy (contract-level guard) ---


def test_library_created_mlb_session_retains_retry_policy_contract():
    """Library-created Mlb Sessions keep the existing retry policy values."""
    mlb = Mlb()
    try:
        for scheme in ("https://", "http://"):
            assert_library_retry_policy(mlb._session.get_adapter(scheme).max_retries)
    finally:
        mlb.close()


# --- Constructor compatibility / positional argument order ---


def test_mlb_constructors_remain_compatible():
    """Existing Mlb() positional constructor usage continues to work."""
    mlb_default = Mlb()
    try:
        assert isinstance(mlb_default._session, requests.Session)
        assert mlb_default._timeout == DEFAULT_TIMEOUT
        assert mlb_default._strict_http is False
    finally:
        mlb_default.close()

    mlb_host = Mlb("statsapi.mlb.com")
    try:
        assert mlb_host._mlb_adapter_v1.url.startswith(
            "https://statsapi.mlb.com/api/v1/"
        )
    finally:
        mlb_host.close()

    logger = MagicMock()
    logger.level = 0
    mlb_logger = Mlb("statsapi.mlb.com", logger)
    try:
        assert mlb_logger._logger is logger
    finally:
        mlb_logger.close()


def test_mlb_positional_timeout_remains_third_argument():
    """Guard against inserting new positional args before timeout."""
    session = RecordingSession()
    mlb = Mlb("statsapi.mlb.com", None, 10, session)

    mlb._mlb_adapter_v1.get(endpoint="sports")
    mlb._mlb_adapter_v1_1.get(endpoint="game")

    assert session.calls[0]["timeout"] == 10
    assert session.calls[1]["timeout"] == 10
    assert mlb._session is session
    assert mlb._strict_http is False


def test_mlb_strict_http_is_keyword_only():
    """strict_http must not shift existing positional constructor arguments."""
    logger = MagicMock()
    logger.level = 0
    session = RecordingSession()

    mlb = Mlb("statsapi.mlb.com", logger, 10, session)
    assert mlb._session is session
    assert mlb._timeout == 10
    assert mlb._strict_http is False

    mlb_strict = Mlb(
        "statsapi.mlb.com",
        logger,
        10,
        session,
        strict_http=True,
    )
    assert mlb_strict._session is session
    assert mlb_strict._timeout == 10
    assert mlb_strict._strict_http is True
    assert mlb_strict._mlb_adapter_v1._strict_http is True
    assert mlb_strict._mlb_adapter_v1_1._strict_http is True

    with pytest.raises(TypeError):
        Mlb("statsapi.mlb.com", logger, 10, session, True)


def test_adapter_positional_construction_remains_compatible():
    """Existing MlbDataAdapter positional construction order stays intact."""
    logger = MagicMock()
    session = RecordingSession()
    adapter = MlbDataAdapter("statsapi.mlb.com", "v1.1", logger, (5.0, 60.0), session)

    assert adapter.url == "https://statsapi.mlb.com/api/v1.1/"
    assert adapter._logger is logger
    assert adapter._timeout == (5.0, 60.0)
    assert adapter._session is session
    assert adapter._strict_http is False

    adapter.get(endpoint="game")
    assert session.calls[0]["timeout"] == (5.0, 60.0)


def test_adapter_strict_http_is_keyword_only():
    """Adapter strict_http is keyword-only and does not shift positional args."""
    logger = MagicMock()
    session = RecordingSession()
    adapter = MlbDataAdapter(
        "statsapi.mlb.com",
        "v1.1",
        logger,
        (5.0, 60.0),
        session,
        strict_http=True,
    )
    assert adapter._strict_http is True

    with pytest.raises(TypeError):
        MlbDataAdapter(
            "statsapi.mlb.com",
            "v1.1",
            logger,
            (5.0, 60.0),
            session,
            True,
        )


# --- Timeout forwarding at the Mlb client level ---


def test_mlb_timeout_constructors_forward_to_both_adapters():
    """Default, scalar, and tuple timeouts reach both v1 and v1.1 adapters."""
    default_session = RecordingSession()
    mlb_default = Mlb(session=default_session)
    mlb_default._mlb_adapter_v1.get(endpoint="sports")
    mlb_default._mlb_adapter_v1_1.get(endpoint="game")
    assert default_session.calls[0]["timeout"] == DEFAULT_TIMEOUT
    assert default_session.calls[1]["timeout"] == DEFAULT_TIMEOUT

    scalar_session = RecordingSession()
    mlb_scalar = Mlb(session=scalar_session, timeout=10)
    mlb_scalar._mlb_adapter_v1.get(endpoint="sports")
    mlb_scalar._mlb_adapter_v1_1.get(endpoint="game")
    assert scalar_session.calls[0]["timeout"] == 10
    assert scalar_session.calls[1]["timeout"] == 10

    tuple_session = RecordingSession()
    mlb_tuple = Mlb(session=tuple_session, timeout=(5.0, 60.0))
    mlb_tuple._mlb_adapter_v1.get(endpoint="sports")
    mlb_tuple._mlb_adapter_v1_1.get(endpoint="game")
    assert tuple_session.calls[0]["timeout"] == (5.0, 60.0)
    assert tuple_session.calls[1]["timeout"] == (5.0, 60.0)
