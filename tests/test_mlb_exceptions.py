"""Offline tests for the structured MLB Stats API exception hierarchy."""

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
        text='{"some bad json": sdfsd',
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
    assert str(exc_info.value) == f"{status_code}: {reason}"
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
