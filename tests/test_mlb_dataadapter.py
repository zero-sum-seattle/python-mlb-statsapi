"""Offline characterization tests for MlbDataAdapter.

These tests document current HTTP adapter behavior with requests-mock before
the transport is refactored in version 0.8.0. Known defects use strict xfail
markers so a future fix causes XPASS until the marker is removed.
"""

import requests
import pytest

from mlbstatsapi import MlbDataAdapter, MlbResult, TheMlbStatsApiException


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
    assert result.data == {}


def test_json_500_raises_the_mlb_stats_api_exception(adapter, requests_mock):
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

    with pytest.raises(TheMlbStatsApiException, match=r"^500: Internal Server Error$") as exc_info:
        adapter.get(
            endpoint="teams/133/stats",
            ep_params={"stats": "standard", "group": "hitting"},
        )

    assert str(exc_info.value) == "500: Internal Server Error"


def test_connection_failure_raises_request_failed(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        exc=requests.exceptions.ConnectionError("connection refused"),
    )

    with pytest.raises(TheMlbStatsApiException, match=r"^Request failed$") as exc_info:
        adapter.get(endpoint="sports")

    assert str(exc_info.value) == "Request failed"
    assert isinstance(exc_info.value.__cause__, requests.exceptions.ConnectionError)


def test_invalid_json_on_successful_response_raises_bad_json(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}teams/133/stats",
        text='{"some bad json": sdfsd',
        status_code=200,
        reason="OK",
        headers={"Content-Type": "application/json"},
    )

    with pytest.raises(TheMlbStatsApiException, match=r"^Bad JSON in response$") as exc_info:
        adapter.get(
            endpoint="teams/133/stats",
            ep_params={"stats": "season", "group": "hitting"},
        )

    assert str(exc_info.value) == "Bad JSON in response"


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


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Adapter always JSON-decodes before status handling; "
        "fix/http-adapter-correctness should return empty data for empty successful bodies"
    ),
)
def test_empty_successful_response_returns_empty_data(adapter, requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        text="",
        status_code=204,
        reason="No Content",
    )

    result = adapter.get(endpoint="sports")

    assert result.status_code == 204
    assert result.data == {}


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Adapter JSON-decodes before HTTP status handling; "
        "fix/http-adapter-correctness should return empty data for non-JSON 404 bodies"
    ),
)
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
    assert result.data == {}
