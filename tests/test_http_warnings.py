"""Offline tests for the compatibility-mode HTTP warning added in version 0.9.0.

Kept separate from the strict/compatibility contract module so warning behavior
stays readable. These tests must not contact the live MLB API.
"""

from __future__ import annotations

import contextlib
import json
import warnings
from unittest.mock import MagicMock

import pytest
import requests

import mlbstatsapi
from mlbstatsapi import (
    Mlb,
    MlbDataAdapter,
    MlbDecodeError,
    MlbHttpCompatibilityWarning,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
)

from http_contract_support import (
    COMPATIBILITY_CLIENT_ERRORS,
    HTTP_REASON_BY_STATUS,
    NOT_FOUND_STATUS,
    SERVER_ERRORS,
)

# Final 429 is retried first, so it is covered in tests/test_mlb_retries.py.
WARNING_CLIENT_ERRORS = tuple(
    code for code in COMPATIBILITY_CLIENT_ERRORS if code != 429
)

SPORTS_URL = "https://statsapi.mlb.com/api/v1/sports"


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


def _session_returning(response) -> MagicMock:
    session = MagicMock()
    session.get.return_value = response
    return session


def _session_for_status(
    status_code: int,
    *,
    url: str = SPORTS_URL,
    payload=None,
) -> MagicMock:
    content = b"" if payload is None else json.dumps(payload).encode("utf-8")
    return _session_returning(
        _response(
            status_code=status_code,
            reason=HTTP_REASON_BY_STATUS[status_code],
            url=url,
            content=content,
            payload=payload,
        )
    )


@contextlib.contextmanager
def _recorded_compatibility_warnings():
    """Record every MlbHttpCompatibilityWarning raised inside the block."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", MlbHttpCompatibilityWarning)
        yield caught


def _compatibility_warnings(caught) -> list:
    return [
        item
        for item in caught
        if issubclass(item.category, MlbHttpCompatibilityWarning)
    ]


# --- Public warning class ---


def test_compatibility_warning_is_publicly_importable():
    """The warning category is reachable from the package namespace."""
    assert (
        mlbstatsapi.MlbHttpCompatibilityWarning
        is MlbHttpCompatibilityWarning
    )


def test_compatibility_warning_inherits_future_warning():
    """FutureWarning keeps this migration notice visible by default."""
    assert issubclass(MlbHttpCompatibilityWarning, FutureWarning)
    assert issubclass(MlbHttpCompatibilityWarning, Warning)
    assert not issubclass(MlbHttpCompatibilityWarning, DeprecationWarning)


# --- Compatibility-mode non-404 4xx warns exactly once ---


@pytest.mark.parametrize("status_code", WARNING_CLIENT_ERRORS)
def test_compatibility_client_errors_warn_once_and_return_empty_result(status_code):
    """Non-404 4xx warns once while preserving the historical empty result."""
    session = _session_for_status(status_code)
    adapter = MlbDataAdapter(session=session)

    with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
        result = adapter.get(endpoint="sports")

    assert result.status_code == status_code
    assert result.message == HTTP_REASON_BY_STATUS[status_code]
    assert result.data == {}
    assert len(warning_info) == 1


@pytest.mark.parametrize("status_code", WARNING_CLIENT_ERRORS)
def test_compatibility_warning_message_contains_migration_guidance(status_code):
    """The message carries status, URL, mode, migration, and version guidance."""
    session = _session_for_status(status_code)
    adapter = MlbDataAdapter(session=session)

    with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
        adapter.get(endpoint="sports")

    message = str(warning_info[0].message)
    assert str(status_code) in message
    assert SPORTS_URL in message
    assert "compatibility mode" in message
    assert "strict_http=True" in message
    assert "MlbHttpError" in message
    assert "version 1.0" in message


def test_compatibility_warning_excludes_response_body():
    """Response bodies must never leak into the warning message."""
    payload = {"message": "secret client error detail"}
    session = _session_for_status(403, payload=payload)
    adapter = MlbDataAdapter(session=session)

    with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
        adapter.get(endpoint="sports")

    message = str(warning_info[0].message)
    assert "secret client error detail" not in message
    assert json.dumps(payload) not in message


def test_compatibility_warning_falls_back_to_request_url():
    """A response without a URL still reports the requested endpoint."""
    response = _response(
        status_code=403,
        reason=HTTP_REASON_BY_STATUS[403],
        url=None,
    )
    adapter = MlbDataAdapter(session=_session_returning(response))

    with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
        adapter.get(endpoint="sports")

    assert SPORTS_URL in str(warning_info[0].message)


# --- Client wiring: default and explicit compatibility mode ---


@pytest.mark.parametrize("status_code", WARNING_CLIENT_ERRORS)
def test_default_mlb_client_warns_for_non_404_client_errors(status_code):
    """Mlb() stays in compatibility mode and receives the migration notice."""
    session = _session_for_status(status_code)
    mlb = Mlb(session=session)

    with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
        result = mlb._mlb_adapter_v1.get(endpoint="sports")

    assert result.status_code == status_code
    assert result.data == {}
    assert len(warning_info) == 1


def test_default_mlb_client_public_endpoint_warns_and_keeps_return_shape():
    """A public endpoint keeps returning None for 4xx while warning once."""
    session = _session_for_status(
        403,
        url="https://statsapi.mlb.com/api/v1/people/664034",
    )
    mlb = Mlb(session=session)

    with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
        person = mlb.get_person(664034)

    assert person is None
    assert len(warning_info) == 1


@pytest.mark.parametrize("status_code", WARNING_CLIENT_ERRORS)
def test_explicit_compatibility_mode_warns_and_preserves_result(status_code):
    """Mlb(strict_http=False) warns without changing the compatibility result."""
    session = _session_for_status(status_code)
    mlb = Mlb(session=session, strict_http=False)

    with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
        result = mlb._mlb_adapter_v1.get(endpoint="sports")

    assert result.status_code == status_code
    assert result.message == HTTP_REASON_BY_STATUS[status_code]
    assert result.data == {}
    assert len(warning_info) == 1


# --- Strict mode raises instead of warning ---


@pytest.mark.parametrize("status_code", WARNING_CLIENT_ERRORS)
def test_strict_mode_raises_without_compatibility_warning(status_code):
    """Strict mode raises MlbHttpError and emits no compatibility warning."""
    payload = {"error": HTTP_REASON_BY_STATUS[status_code]}
    session = _session_for_status(status_code, payload=payload)
    mlb = Mlb(session=session, strict_http=True)

    with _recorded_compatibility_warnings() as caught:
        with pytest.raises(MlbHttpError) as exc_info:
            mlb._mlb_adapter_v1.get(endpoint="sports")

    exc = exc_info.value
    assert exc.status_code == status_code
    assert exc.reason == HTTP_REASON_BY_STATUS[status_code]
    assert exc.url == SPORTS_URL
    assert exc.method == "GET"
    assert exc.response_data == payload
    assert _compatibility_warnings(caught) == []


# --- 404 stays warning-free in both modes ---


@pytest.mark.parametrize("strict_http", [False, True])
def test_adapter_404_does_not_warn(strict_http):
    """A final 404 returns an MlbResult without warning in either mode."""
    session = _session_for_status(
        NOT_FOUND_STATUS,
        url="https://statsapi.mlb.com/api/v1/people/999999",
    )
    adapter = MlbDataAdapter(session=session, strict_http=strict_http)

    with _recorded_compatibility_warnings() as caught:
        result = adapter.get(endpoint="people/999999")

    assert result.status_code == NOT_FOUND_STATUS
    assert result.data == {}
    assert _compatibility_warnings(caught) == []


@pytest.mark.parametrize("strict_http", [False, True])
def test_public_404_return_shapes_do_not_warn(strict_http):
    """404 keeps None / [] / {} endpoint shapes without emitting a warning."""
    session = _session_for_status(
        NOT_FOUND_STATUS,
        url="https://statsapi.mlb.com/api/v1/people/999999",
    )
    mlb = Mlb(session=session, strict_http=strict_http)

    with _recorded_compatibility_warnings() as caught:
        assert mlb.get_person(999999) is None
        assert mlb.get_teams() == []
        assert mlb.get_player_stats(999999, ["season"], ["hitting"]) == {}

    assert _compatibility_warnings(caught) == []


# --- Successful responses stay warning-free ---


@pytest.mark.parametrize("strict_http", [False, True])
def test_successful_response_does_not_warn(strict_http):
    """A 200 response parses normally and emits no compatibility warning."""
    payload = {"sports": [{"id": 1}]}
    session = _session_returning(
        _response(
            status_code=200,
            reason="OK",
            url=SPORTS_URL,
            content=json.dumps(payload).encode("utf-8"),
            payload=payload,
        )
    )
    adapter = MlbDataAdapter(session=session, strict_http=strict_http)

    with _recorded_compatibility_warnings() as caught:
        result = adapter.get(endpoint="sports")

    assert result.status_code == 200
    assert result.data == payload
    assert _compatibility_warnings(caught) == []


# --- Final 5xx already raises, so it is not compatibility-suppressed ---


@pytest.mark.parametrize("status_code", SERVER_ERRORS)
@pytest.mark.parametrize("strict_http", [False, True])
def test_final_server_errors_do_not_warn(status_code, strict_http):
    """Final 5xx raises MlbHttpError in both modes without a compatibility warning."""
    session = _session_for_status(status_code)
    adapter = MlbDataAdapter(session=session, strict_http=strict_http)

    with _recorded_compatibility_warnings() as caught:
        with pytest.raises(MlbHttpError) as exc_info:
            adapter.get(endpoint="sports")

    assert exc_info.value.status_code == status_code
    assert _compatibility_warnings(caught) == []


# --- Transport, timeout, and decode failures stay warning-free ---


@pytest.mark.parametrize("strict_http", [False, True])
def test_timeout_does_not_warn(strict_http):
    """Timeouts raise MlbTimeoutError without a compatibility warning."""
    session = MagicMock()
    session.get.side_effect = requests.exceptions.Timeout("timed out")
    adapter = MlbDataAdapter(session=session, strict_http=strict_http)

    with _recorded_compatibility_warnings() as caught:
        with pytest.raises(MlbTimeoutError):
            adapter.get(endpoint="sports")

    assert _compatibility_warnings(caught) == []


@pytest.mark.parametrize("strict_http", [False, True])
def test_connection_failure_does_not_warn(strict_http):
    """Connection failures raise MlbTransportError without a compatibility warning."""
    session = MagicMock()
    session.get.side_effect = requests.exceptions.ConnectionError("refused")
    adapter = MlbDataAdapter(session=session, strict_http=strict_http)

    with _recorded_compatibility_warnings() as caught:
        with pytest.raises(MlbTransportError):
            adapter.get(endpoint="sports")

    assert _compatibility_warnings(caught) == []


@pytest.mark.parametrize("strict_http", [False, True])
def test_decode_failure_does_not_warn(strict_http):
    """Malformed JSON on a 200 raises MlbDecodeError without warning."""
    response = _response(
        status_code=200,
        reason="OK",
        url=SPORTS_URL,
        content=b'{"bad": json',
        text='{"bad": json',
    )
    response.json.side_effect = ValueError("Expecting value")
    adapter = MlbDataAdapter(
        session=_session_returning(response),
        strict_http=strict_http,
    )

    with _recorded_compatibility_warnings() as caught:
        with pytest.raises(MlbDecodeError):
            adapter.get(endpoint="sports")

    assert _compatibility_warnings(caught) == []


# --- Caller-controlled warning filters ---


def test_caller_can_turn_the_warning_into_an_exception():
    """A caller may promote only this category to an error."""
    session = _session_for_status(403)
    adapter = MlbDataAdapter(session=session)

    with warnings.catch_warnings():
        warnings.simplefilter("error", MlbHttpCompatibilityWarning)
        with pytest.raises(MlbHttpCompatibilityWarning):
            adapter.get(endpoint="sports")


def test_caller_can_ignore_only_this_warning_category():
    """Ignoring the category keeps the historical compatibility result."""
    session = _session_for_status(403)
    adapter = MlbDataAdapter(session=session)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warnings.simplefilter("ignore", MlbHttpCompatibilityWarning)
        result = adapter.get(endpoint="sports")

    assert result.status_code == 403
    assert result.data == {}
    assert _compatibility_warnings(caught) == []


def test_each_request_emits_its_own_warning():
    """Every final non-404 4xx warns; deduplication is left to warning filters."""
    session = _session_for_status(429)
    adapter = MlbDataAdapter(session=session)

    with _recorded_compatibility_warnings() as caught:
        adapter.get(endpoint="sports")
        adapter.get(endpoint="sports")

    assert len(_compatibility_warnings(caught)) == 2
