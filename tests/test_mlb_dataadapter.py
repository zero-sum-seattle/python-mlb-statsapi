"""Offline regression tests for MlbDataAdapter.

These tests protect HTTP adapter response-handling behavior for version 0.8.0,
including successful 2xx handling, status classification before JSON decoding,
and empty successful bodies.
"""

import logging

import requests
import pytest

from mlbstatsapi import (
    MlbDataAdapter,
    MlbDecodeError,
    MlbHttpError,
    MlbResult,
    MlbTransportError,
    TheMlbStatsApiException,
)


BASE_URL = "https://statsapi.mlb.com/api/v1/"


@pytest.fixture
def adapter() -> MlbDataAdapter:
    return MlbDataAdapter()


def test_successful_json_response_returns_exact_values(adapter, requests_mock):
    payload = {
        "copyright": "Copyright 2026 MLB Advanced Media, L.P.",
        "sports": [{"id": 1, "name": "Major League Baseball"}],
    }
    requests_mock.get(
        f"{BASE_URL}sports",
        json=payload,
        status_code=200,
        reason="OK",
    )

    result = adapter.get(endpoint="sports")

    assert result.status_code == 200
    assert result.message == "OK"
    assert result.data == {"sports": [{"id": 1, "name": "Major League Baseball"}]}


@pytest.mark.parametrize(
    ("status_code", "reason", "payload"),
    [
        (201, "Created", {"id": 42, "name": "created"}),
        (299, "Custom Success", {"ok": True}),
    ],
)
def test_other_successful_json_statuses_return_exact_values(
    adapter,
    requests_mock,
    status_code,
    reason,
    payload,
):
    requests_mock.get(
        f"{BASE_URL}sports",
        json=payload,
        status_code=status_code,
        reason=reason,
    )

    result = adapter.get(endpoint="sports")

    assert result.status_code == status_code
    assert result.message == reason
    assert result.data == payload


def test_empty_successful_response_returns_empty_data(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        text="",
        status_code=204,
        reason="No Content",
    )

    result = adapter.get(endpoint="sports")

    assert result.status_code == 204
    assert result.message == "No Content"
    assert result.data == {}


def test_ep_params_are_sent_as_query_parameters(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}teams/133/stats",
        json={"stats": []},
        status_code=200,
        reason="OK",
    )

    result = adapter.get(
        endpoint="teams/133/stats",
        ep_params={"stats": "season", "group": "hitting", "season": 2022},
    )

    assert result.status_code == 200
    assert requests_mock.called
    assert requests_mock.last_request.qs == {
        "stats": ["season"],
        "group": ["hitting"],
        "season": ["2022"],
    }


def test_status_code_and_reason_are_preserved_on_result(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        json={"sports": []},
        status_code=200,
        reason="OK",
    )

    result = adapter.get(endpoint="sports")

    assert result.status_code == 200
    assert result.message == "OK"


def test_copyright_is_removed_from_result_data(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        json={
            "copyright": "Copyright 2026 MLB Advanced Media, L.P.",
            "sports": [],
        },
        status_code=200,
        reason="OK",
    )

    result = adapter.get(endpoint="sports")

    assert "copyright" not in result.data
    assert result.data == {"sports": []}


def test_json_404_returns_empty_data(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}teams/19990",
        json={
            "messageNumber": 10,
            "message": "Object not found",
            "timestamp": "2022-10-13T18:16:41.886604Z",
            "traceId": None,
        },
        status_code=404,
        reason="Not Found",
    )

    result = adapter.get(endpoint="teams/19990")

    assert result.status_code == 404
    assert result.message == "Not Found"
    assert result.data == {}


def test_non_json_404_returns_empty_data(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}teams/19990",
        text="<html><body>Not Found</body></html>",
        status_code=404,
        reason="Not Found",
        headers={"Content-Type": "text/html"},
    )

    result = adapter.get(endpoint="teams/19990")

    assert result.status_code == 404
    assert result.message == "Not Found"
    assert result.data == {}


def test_json_500_raises_mlb_http_error(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}teams/133/stats",
        json={
            "messageNumber": 1,
            "message": "Internal error occurred",
            "timestamp": "2022-10-13T18:37:47.600274Z",
            "traceId": "9318607c0b50f493e9056648614a5cea",
        },
        status_code=500,
        reason="Internal Server Error",
    )

    with pytest.raises(MlbHttpError, match=r"^500: Internal Server Error$") as exc_info:
        adapter.get(
            endpoint="teams/133/stats",
            ep_params={"stats": "standard", "group": "hitting"},
        )

    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert str(exc_info.value) == "500: Internal Server Error"
    assert exc_info.value.status_code == 500
    assert exc_info.value.reason == "Internal Server Error"


def test_html_502_raises_mlb_http_error(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        text="<html><body>Bad Gateway</body></html>",
        status_code=502,
        reason="Bad Gateway",
        headers={"Content-Type": "text/html"},
    )

    with pytest.raises(MlbHttpError, match=r"^502: Bad Gateway$") as exc_info:
        adapter.get(endpoint="sports")

    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert str(exc_info.value) == "502: Bad Gateway"
    assert exc_info.value.status_code == 502
    assert exc_info.value.reason == "Bad Gateway"


def test_connection_failure_raises_mlb_transport_error(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        exc=requests.exceptions.ConnectionError("connection refused"),
    )

    with pytest.raises(MlbTransportError, match=r"^Request failed$") as exc_info:
        adapter.get(endpoint="sports")

    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert str(exc_info.value) == "Request failed"
    assert isinstance(exc_info.value.__cause__, requests.exceptions.ConnectionError)


def test_invalid_json_on_successful_response_raises_mlb_decode_error(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}teams/133/stats",
        text='{"some bad json": sdfsd',
        status_code=200,
        reason="OK",
        headers={"Content-Type": "application/json"},
    )

    with pytest.raises(MlbDecodeError, match=r"^Bad JSON in response$") as exc_info:
        adapter.get(
            endpoint="teams/133/stats",
            ep_params={"stats": "season", "group": "hitting"},
        )

    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert str(exc_info.value) == "Bad JSON in response"
    assert isinstance(exc_info.value.__cause__, ValueError)


def test_constructor_does_not_change_logger_level():
    logger = logging.Logger(
        "mlbstatsapi-test",
        level=logging.WARNING,
    )

    MlbDataAdapter(logger=logger)

    assert logger.level == logging.WARNING


def test_mlb_result_optional_data_argument_omitted():
    result = MlbResult(200, "OK")

    assert result.status_code == 200
    assert result.message == "OK"
    assert result.data == {}


def test_mlb_result_optional_data_argument_explicit_dict():
    result = MlbResult(404, "Not Found", {"ignored": True})

    assert result.status_code == 404
    assert result.message == "Not Found"
    assert result.data == {"ignored": True}


def test_mlb_result_type_coercion():
    result = MlbResult("200", 123, {"value": True})

    assert result.status_code == 200
    assert result.message == "123"
