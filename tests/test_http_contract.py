"""High-level offline HTTP compatibility contract for version 0.9.0.

Protects existing version 0.8.0 public behavior before configurable transport
features are implemented. These tests intentionally validate current
compatibility behavior only; they do not enable strict mode or add production
features.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
import requests

from mlbstatsapi import (
    Mlb,
    MlbDataAdapter,
    MlbHttpError,
    MlbResult,
    TheMlbStatsApiException,
)
from mlbstatsapi.mlb_dataadapter import DEFAULT_TIMEOUT

from http_contract_support import (
    COMPATIBILITY_CLIENT_ERRORS,
    HTTP_REASON_BY_STATUS,
    NOT_FOUND_STATUS,
    SERVER_ERRORS,
    assert_library_retry_policy,
)


def _response(
    *,
    status_code: int,
    reason: str,
    url: str,
    content: bytes = b"",
    payload=None,
):
    response = MagicMock()
    response.status_code = status_code
    response.reason = reason
    response.url = url
    response.content = content
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
    assert COMPATIBILITY_CLIENT_ERRORS == (400, 401, 403, 405, 422, 429)
    assert NOT_FOUND_STATUS == 404
    assert SERVER_ERRORS == (500, 502, 503, 504)
    assert 404 not in COMPATIBILITY_CLIENT_ERRORS
    assert 429 in COMPATIBILITY_CLIENT_ERRORS
    assert set(SERVER_ERRORS).isdisjoint(COMPATIBILITY_CLIENT_ERRORS)


# --- Default 4xx compatibility (empty MlbResult, no MlbHttpError) ---


@pytest.mark.parametrize("status_code", COMPATIBILITY_CLIENT_ERRORS)
def test_compatibility_client_errors_return_empty_mlb_result(status_code):
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = f"https://statsapi.mlb.com/api/v1/sports"
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
    )
    mlb = Mlb(session=session)

    result = mlb._mlb_adapter_v1.get(endpoint="sports")

    assert isinstance(result, MlbResult)
    assert result.status_code == status_code
    assert result.data == {}


@pytest.mark.parametrize("status_code", COMPATIBILITY_CLIENT_ERRORS)
def test_compatibility_client_errors_do_not_raise_mlb_http_error(status_code):
    reason = HTTP_REASON_BY_STATUS[status_code]
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url="https://statsapi.mlb.com/api/v1/sports",
    )
    adapter = MlbDataAdapter(session=session)

    result = adapter.get(endpoint="sports")

    assert result.status_code == status_code
    assert result.data == {}


# --- Endpoint-specific 404 return shapes via public Mlb methods ---


def test_mlb_get_person_404_returns_none():
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url="https://statsapi.mlb.com/api/v1/people/999999",
    )
    mlb = Mlb(session=session)

    assert mlb.get_person(999999) is None


def test_mlb_get_teams_404_returns_empty_list():
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url="https://statsapi.mlb.com/api/v1/teams",
    )
    mlb = Mlb(session=session)

    assert mlb.get_teams() == []


def test_mlb_get_player_stats_404_returns_empty_mapping():
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url="https://statsapi.mlb.com/api/v1/people/999999/stats",
    )
    mlb = Mlb(session=session)

    assert mlb.get_player_stats(999999, ["season"], ["hitting"]) == {}


def test_mlb_endpoint_404_does_not_raise_mlb_http_error():
    session = MagicMock()
    session.get.return_value = _response(
        status_code=NOT_FOUND_STATUS,
        reason=HTTP_REASON_BY_STATUS[NOT_FOUND_STATUS],
        url="https://statsapi.mlb.com/api/v1/people/999999",
    )
    mlb = Mlb(session=session)

    assert mlb.get_person(999999) is None
    assert mlb.get_teams() == []
    assert mlb.get_player_stats(999999, ["season"], ["hitting"]) == {}


# --- Final 5xx raises MlbHttpError with existing attributes ---


@pytest.mark.parametrize("status_code", SERVER_ERRORS)
def test_mlb_server_errors_raise_mlb_http_error_with_existing_attributes(status_code):
    reason = HTTP_REASON_BY_STATUS[status_code]
    url = "https://statsapi.mlb.com/api/v1/people/664034"
    session = MagicMock()
    session.get.return_value = _response(
        status_code=status_code,
        reason=reason,
        url=url,
    )
    mlb = Mlb(session=session)

    with pytest.raises(MlbHttpError, match=rf"^{status_code}: {reason}$") as exc_info:
        mlb.get_person(664034)

    exc = exc_info.value
    assert isinstance(exc, TheMlbStatsApiException)
    assert exc.status_code == status_code
    assert exc.reason == reason
    assert exc.url == url
    # Richer error context belongs to a later issue; protect the current shape.
    assert not hasattr(exc, "response_data")
    assert not hasattr(exc, "body_excerpt")


# --- Library-created retry policy (contract-level guard) ---


def test_library_created_mlb_session_retains_retry_policy_contract():
    mlb = Mlb()
    try:
        for scheme in ("https://", "http://"):
            assert_library_retry_policy(mlb._session.get_adapter(scheme).max_retries)
    finally:
        mlb.close()


# --- Constructor compatibility / positional argument order ---


def test_mlb_constructors_remain_compatible():
    mlb_default = Mlb()
    try:
        assert isinstance(mlb_default._session, requests.Session)
        assert mlb_default._timeout == DEFAULT_TIMEOUT
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


def test_adapter_positional_construction_remains_compatible():
    logger = MagicMock()
    session = RecordingSession()
    adapter = MlbDataAdapter("statsapi.mlb.com", "v1.1", logger, (5.0, 60.0), session)

    assert adapter.url == "https://statsapi.mlb.com/api/v1.1/"
    assert adapter._logger is logger
    assert adapter._timeout == (5.0, 60.0)
    assert adapter._session is session

    adapter.get(endpoint="game")
    assert session.calls[0]["timeout"] == (5.0, 60.0)


# --- Timeout forwarding at the Mlb client level ---


def test_mlb_timeout_constructors_forward_to_both_adapters():
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
