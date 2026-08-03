"""Offline tests for the structured MLB Stats API exception hierarchy."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from mlbstatsapi import (
    Mlb,
    MlbDataAdapter,
    MlbDecodeError,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
    TheMlbStatsApiException,
)
from mlbstatsapi.mlb_dataadapter import (
    HTTP_ERROR_BODY_EXCERPT_LIMIT,
    _build_http_error,
)


BASE_URL = "https://statsapi.mlb.com/api/v1/"


def test_exception_hierarchy():
    assert issubclass(MlbTransportError, TheMlbStatsApiException)
    assert issubclass(MlbTimeoutError, MlbTransportError)
    assert issubclass(MlbHttpError, TheMlbStatsApiException)
    assert issubclass(MlbDecodeError, TheMlbStatsApiException)


@pytest.mark.parametrize(
    "exc_type",
    [
        MlbTransportError,
        MlbTimeoutError,
        MlbHttpError,
        MlbDecodeError,
    ],
)
def test_new_exceptions_are_catchable_as_base(exc_type):
    if exc_type is MlbHttpError:
        raised = MlbHttpError(500, "Internal Server Error", "https://example.test")
    else:
        raised = exc_type("failure")

    with pytest.raises(TheMlbStatsApiException):
        raise raised


def test_mlb_http_error_attributes_and_message():
    exc = MlbHttpError(
        status_code=500,
        reason="Internal Server Error",
        url="https://statsapi.mlb.com/api/v1/sports",
    )

    assert exc.status_code == 500
    assert exc.reason == "Internal Server Error"
    assert exc.url == "https://statsapi.mlb.com/api/v1/sports"
    assert str(exc) == "500: Internal Server Error"


def test_mlb_http_error_positional_construction_preserves_compat():
    exc = MlbHttpError(
        500,
        "Internal Server Error",
        "https://example.test",
    )

    assert exc.status_code == 500
    assert exc.reason == "Internal Server Error"
    assert exc.url == "https://example.test"
    assert exc.method is None
    assert exc.response_data is None
    assert exc.body_excerpt is None
    assert isinstance(exc, TheMlbStatsApiException)
    assert str(exc) == "500: Internal Server Error"


def test_mlb_http_error_method_normalized_to_uppercase():
    exc = MlbHttpError(
        500,
        "Internal Server Error",
        method="get",
    )

    assert exc.method == "GET"


def test_timeout_raises_mlb_timeout_error():
    original = requests.exceptions.Timeout("timed out")
    session = requests.Session()
    session.get = lambda *args, **kwargs: (_ for _ in ()).throw(original)
    adapter = MlbDataAdapter(session=session)

    with pytest.raises(MlbTimeoutError, match=r"^Request failed$") as exc_info:
        adapter.get(endpoint="sports")

    assert isinstance(exc_info.value, MlbTransportError)
    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert str(exc_info.value) == "Request failed"
    assert exc_info.value.__cause__ is original
    session.close()


@pytest.mark.parametrize(
    "timeout_exc",
    [
        requests.exceptions.ConnectTimeout("connect timed out"),
        requests.exceptions.ReadTimeout("read timed out"),
    ],
)
def test_concrete_timeout_subclasses_raise_mlb_timeout_error(timeout_exc):
    session = requests.Session()
    session.get = lambda *args, **kwargs: (_ for _ in ()).throw(timeout_exc)
    adapter = MlbDataAdapter(session=session)

    with pytest.raises(MlbTimeoutError, match=r"^Request failed$") as exc_info:
        adapter.get(endpoint="sports")

    assert isinstance(exc_info.value, MlbTransportError)
    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert exc_info.value.__cause__ is timeout_exc
    session.close()


def test_connection_error_raises_mlb_transport_error():
    original = requests.exceptions.ConnectionError("connection refused")
    session = requests.Session()
    session.get = lambda *args, **kwargs: (_ for _ in ()).throw(original)
    adapter = MlbDataAdapter(session=session)

    with pytest.raises(MlbTransportError, match=r"^Request failed$") as exc_info:
        adapter.get(endpoint="sports")

    assert not isinstance(exc_info.value, MlbTimeoutError)
    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert str(exc_info.value) == "Request failed"
    assert exc_info.value.__cause__ is original
    session.close()


def test_invalid_json_raises_mlb_decode_error(requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        text=\'{"some bad json": sdfsd\',
        status_code=200,
        reason="OK",
        headers={"Content-Type": "application/json"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbDecodeError, match=r"^Bad JSON in response$") as exc_info:
        adapter.get(endpoint="sports")

    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert str(exc_info.value) == "Bad JSON in response"
    assert isinstance(exc_info.value.__cause__, ValueError)
    adapter.close()


@pytest.mark.parametrize(
    ("status_code", "reason"),
    [
        (500, "Internal Server Error"),
        (502, "Bad Gateway"),
    ],
)
def test_server_error_raises_mlb_http_error(status_code, reason, requests_mock):
    url = f"{BASE_URL}sports"
    requests_mock.get(
        url,
        text="<html><body>error</body></html>",
        status_code=status_code,
        reason=reason,
        headers={"Content-Type": "text/html"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError, match=rf"^{status_code}: {reason}$") as exc_info:
        adapter.get(endpoint="sports")

    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert exc_info.value.status_code == status_code
    assert exc_info.value.reason == reason
    assert exc_info.value.url == url
    assert exc_info.value.method == "GET"
    assert str(exc_info.value) == f"{status_code}: {reason}"
    adapter.close()


def test_json_object_error_populates_response_data(requests_mock):
    payload = {
        "message": "Internal error occurred",
        "code": "SERVICE_FAILURE",
    }
    url = f"{BASE_URL}sports"
    requests_mock.get(
        url,
        json=payload,
        status_code=500,
        reason="Internal Server Error",
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.method == "GET"
    assert exc.response_data == payload
    assert exc.body_excerpt is not None
    assert len(exc.body_excerpt) <= HTTP_ERROR_BODY_EXCERPT_LIMIT
    assert "Internal error occurred" in exc.body_excerpt
    assert str(exc) == "500: Internal Server Error"
    adapter.close()


def test_json_list_error_populates_response_data(requests_mock):
    payload = [{"message": "error"}, {"message": "another"}]
    requests_mock.get(
        f"{BASE_URL}sports",
        json=payload,
        status_code=500,
        reason="Internal Server Error",
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    assert exc_info.value.response_data == payload
    assert exc_info.value.method == "GET"
    adapter.close()


def test_invalid_json_error_keeps_mlb_http_error(requests_mock):
    malformed = \'{"message": broken\'
    requests_mock.get(
        f"{BASE_URL}sports",
        text=malformed,
        status_code=500,
        reason="Internal Server Error",
        headers={"Content-Type": "application/json"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert not isinstance(exc, MlbDecodeError)
    assert exc.response_data is None
    assert exc.body_excerpt == malformed
    assert str(exc) == "500: Internal Server Error"
    adapter.close()


def test_html_error_response_context(requests_mock):
    html = "<html><body>Internal Server Error</body></html>"
    requests_mock.get(
        f"{BASE_URL}sports",
        text=html,
        status_code=500,
        reason="Internal Server Error",
        headers={"Content-Type": "text/html"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.response_data is None
    assert html in (exc.body_excerpt or "")
    adapter.close()


def test_plain_text_error_response_context(requests_mock):
    text = "temporary failure, try again later"
    requests_mock.get(
        f"{BASE_URL}sports",
        text=text,
        status_code=503,
        reason="Service Unavailable",
        headers={"Content-Type": "text/plain"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.response_data is None
    assert text in (exc.body_excerpt or "")
    adapter.close()


def test_empty_error_response_context(requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        text="",
        status_code=500,
        reason="Internal Server Error",
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.response_data is None
    assert exc.body_excerpt is None
    adapter.close()


def test_large_error_body_excerpt_is_bounded(requests_mock):
    body = "x" * (HTTP_ERROR_BODY_EXCERPT_LIMIT + 250)
    requests_mock.get(
        f"{BASE_URL}sports",
        text=body,
        status_code=500,
        reason="Internal Server Error",
        headers={"Content-Type": "text/plain"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert len(exc.body_excerpt) <= HTTP_ERROR_BODY_EXCERPT_LIMIT
    assert exc.body_excerpt == body[:HTTP_ERROR_BODY_EXCERPT_LIMIT]
    assert body not in str(exc)
    assert str(exc) == "500: Internal Server Error"
    adapter.close()


def test_json_scalar_error_response_data_is_none(requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        text=\'"server unavailable"\',
        status_code=500,
        reason="Internal Server Error",
        headers={"Content-Type": "application/json"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.response_data is None
    assert "server unavailable" in (exc.body_excerpt or "")
    adapter.close()


def test_non_ascii_error_body_excerpt(requests_mock):
    text = "エラー: サーバー障害 — café"
    requests_mock.get(
        f"{BASE_URL}sports",
        text=text,
        status_code=500,
        reason="Internal Server Error",
        headers={"Content-Type": "text/plain; charset=utf-8"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    assert text in (exc_info.value.body_excerpt or "")
    adapter.close()


def test_unexpected_status_raises_mlb_http_error_with_context(requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        text="redirect loop",
        status_code=308,
        reason="Permanent Redirect",
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.status_code == 308
    assert exc.method == "GET"
    assert exc.response_data is None
    assert "redirect loop" in (exc.body_excerpt or "")
    adapter.close()


def test_url_fallback_when_response_url_missing():
    response = MagicMock()
    response.status_code = 500
    response.reason = "Internal Server Error"
    response.url = ""
    response.content = b\'{"message": "boom"}\'
    response.json.return_value = {"message": "boom"}
    response.text = \'{"message": "boom"}\'

    exc = _build_http_error(
        response,
        method="GET",
        fallback_url=f"{BASE_URL}sports",
    )

    assert exc.url == f"{BASE_URL}sports"
    assert exc.method == "GET"
    assert exc.response_data == {"message": "boom"}


def test_best_effort_extraction_failure_still_raises_mlb_http_error(requests_mock):
    requests_mock.get(
        f"{BASE_URL}sports",
        text="failure body",
        status_code=500,
        reason="Internal Server Error",
    )
    adapter = MlbDataAdapter()

    with (
        patch(
            "mlbstatsapi.mlb_dataadapter._extract_error_response_data",
            side_effect=RuntimeError("unexpected json failure"),
        ),
        patch(
            "mlbstatsapi.mlb_dataadapter._extract_error_body_excerpt",
            side_effect=RuntimeError("unexpected text failure"),
        ),
        pytest.raises(MlbHttpError) as exc_info,
    ):
        adapter.get(endpoint="sports")

    exc = exc_info.value
    assert exc.status_code == 500
    assert exc.reason == "Internal Server Error"
    assert exc.url == f"{BASE_URL}sports"
    assert exc.method == "GET"
    assert exc.response_data is None
    assert exc.body_excerpt is None
    assert str(exc) == "500: Internal Server Error"
    adapter.close()


def test_error_response_body_is_not_logged(requests_mock, caplog):
    secret = "DO-NOT-LOG-THIS-BODY"
    requests_mock.get(
        f"{BASE_URL}sports",
        text=secret,
        status_code=500,
        reason="Internal Server Error",
        headers={"Content-Type": "text/plain"},
    )
    adapter = MlbDataAdapter()

    with pytest.raises(MlbHttpError) as exc_info:
        adapter.get(endpoint="sports")

    assert secret in (exc_info.value.body_excerpt or "")
    logged = " ".join(record.getMessage() for record in caplog.records)
    assert secret not in logged
    adapter.close()


def test_injected_session_exception_wrapping_still_works():
    original = requests.exceptions.Timeout("timed out")
    session = requests.Session()
    session.get = lambda *args, **kwargs: (_ for _ in ()).throw(original)
    mlb = Mlb(session=session)

    with pytest.raises(MlbTimeoutError, match=r"^Request failed$") as exc_info:
        mlb._mlb_adapter_v1.get(endpoint="sports")

    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert exc_info.value.__cause__ is original
    session.close()
