"""Offline tests for shared HTTP sessions, timeouts, and the package User-Agent.

These tests cover session injection, ownership, cleanup, sharing, header
handling, and timeout forwarding without calling the live MLB API.
"""

from importlib.metadata import PackageNotFoundError
from unittest.mock import MagicMock, patch

import pytest
import requests

from mlbstatsapi import Mlb, MlbDataAdapter, MlbHttpError, TheMlbStatsApiException
from mlbstatsapi.mlb_dataadapter import (
    DEFAULT_TIMEOUT,
    PACKAGE_DISTRIBUTION_NAME,
    _configure_library_session,
)

from http_contract_support import assert_library_retry_policy


MOCKED_PACKAGE_VERSION = "9.8.7"
MOCKED_USER_AGENT = f"python-mlb-statsapi/{MOCKED_PACKAGE_VERSION}"


class RecordingSession:
    """Minimal session stand-in that records get() and close() calls."""

    def __init__(self):
        self.calls = []
        self.close_calls = 0

    def get(self, url, params=None, timeout=None, **kwargs):
        self.calls.append(
            {
                "url": url,
                "params": params,
                "timeout": timeout,
                "kwargs": kwargs,
            }
        )
        response = MagicMock()
        response.status_code = 200
        response.reason = "OK"
        response.url = url
        response.content = b'{"sports": []}'
        response.json.return_value = {"sports": []}
        return response

    def close(self):
        self.close_calls += 1


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


# --- Adapter transport ---


def test_adapter_calls_configured_session_get():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session)

    result = adapter.get(endpoint="sports")

    assert result.status_code == 200
    assert result.data == {"sports": []}
    assert len(session.calls) == 1
    assert session.calls[0]["url"] == "https://statsapi.mlb.com/api/v1/sports"


def test_adapter_does_not_use_module_level_requests_get():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session)

    with patch("mlbstatsapi.mlb_dataadapter.requests.get") as module_get:
        adapter.get(endpoint="sports")

    module_get.assert_not_called()
    assert len(session.calls) == 1


def test_adapter_forwards_query_parameters():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session)
    params = {"stats": "season", "group": "hitting", "season": 2022}

    adapter.get(endpoint="teams/133/stats", ep_params=params)

    assert session.calls[0]["params"] == params


def test_adapter_successful_response_behavior_with_session():
    session = MagicMock()
    session.get.return_value = _response(
        status_code=200,
        reason="OK",
        url="https://statsapi.mlb.com/api/v1/sports",
        content=b'{"sports":[{"id":1}]}',
        payload={"sports": [{"id": 1}]},
    )
    adapter = MlbDataAdapter(session=session)

    result = adapter.get(endpoint="sports")

    assert result.status_code == 200
    assert result.message == "OK"
    assert result.data == {"sports": [{"id": 1}]}


def test_adapter_404_behavior_with_session():
    session = MagicMock()
    session.get.return_value = _response(
        status_code=404,
        reason="Not Found",
        url="https://statsapi.mlb.com/api/v1/teams/19990",
        content=b'{"message":"Object not found"}',
        payload={"message": "Object not found"},
    )
    adapter = MlbDataAdapter(session=session)

    result = adapter.get(endpoint="teams/19990")

    assert result.status_code == 404
    assert result.message == "Not Found"
    assert result.data == {}


def test_adapter_500_behavior_with_session():
    session = MagicMock()
    session.get.return_value = _response(
        status_code=500,
        reason="Internal Server Error",
        url="https://statsapi.mlb.com/api/v1/sports",
        content=b'{"message":"Internal error occurred"}',
        payload={"message": "Internal error occurred"},
    )
    adapter = MlbDataAdapter(session=session)

    with pytest.raises(MlbHttpError, match=r"^500: Internal Server Error$") as exc_info:
        adapter.get(endpoint="sports")

    assert isinstance(exc_info.value, TheMlbStatsApiException)
    assert exc_info.value.status_code == 500
    assert exc_info.value.reason == "Internal Server Error"
    assert exc_info.value.url == "https://statsapi.mlb.com/api/v1/sports"


# --- Timeouts ---


def test_default_timeout_constant():
    assert DEFAULT_TIMEOUT == (3.05, 30.0)


def test_adapter_passes_default_timeout_to_session():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session)

    adapter.get(endpoint="sports")

    assert session.calls[0]["timeout"] == (3.05, 30.0)


def test_adapter_passes_scalar_timeout_unchanged():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session, timeout=10)

    adapter.get(endpoint="sports")

    assert session.calls[0]["timeout"] == 10


def test_adapter_passes_tuple_timeout_unchanged():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session, timeout=(5.0, 60.0))

    adapter.get(endpoint="sports")

    assert session.calls[0]["timeout"] == (5.0, 60.0)


def test_mlb_configured_timeout_reaches_both_adapters():
    session = RecordingSession()
    mlb = Mlb(session=session, timeout=(1.5, 20.0))

    mlb._mlb_adapter_v1.get(endpoint="sports")
    mlb._mlb_adapter_v1_1.get(endpoint="game")

    assert session.calls[0]["timeout"] == (1.5, 20.0)
    assert session.calls[1]["timeout"] == (1.5, 20.0)
    assert session.calls[0]["url"].endswith("/api/v1/sports")
    assert session.calls[1]["url"].endswith("/api/v1.1/game")


def test_mlb_scalar_timeout_reaches_both_adapters():
    """Scalar Mlb(timeout=...) values are forwarded unchanged to both adapters."""
    session = RecordingSession()
    mlb = Mlb(session=session, timeout=10)

    mlb._mlb_adapter_v1.get(endpoint="sports")
    mlb._mlb_adapter_v1_1.get(endpoint="game")

    assert session.calls[0]["timeout"] == 10
    assert session.calls[1]["timeout"] == 10


def test_mlb_default_timeout_passed_to_session():
    session = RecordingSession()
    mlb = Mlb(session=session)

    mlb._mlb_adapter_v1.get(endpoint="sports")

    assert session.calls[0]["timeout"] == DEFAULT_TIMEOUT


# --- Shared session ---


def test_injected_session_is_shared_by_both_adapters():
    session = RecordingSession()
    mlb = Mlb(session=session)

    assert mlb._session is session
    assert mlb._mlb_adapter_v1._session is session
    assert mlb._mlb_adapter_v1_1._session is session
    assert mlb._mlb_adapter_v1._session is mlb._mlb_adapter_v1_1._session


def test_injected_session_is_not_replaced_with_library_session():
    """Caller-injected Sessions are used as-is; the library creates no replacement."""
    session = requests.Session()
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        mlb = Mlb(session=session)

        session_cls.assert_not_called()
        assert mlb._session is session
        assert mlb._mlb_adapter_v1._session is session
        assert mlb._mlb_adapter_v1_1._session is session
        assert mlb._owns_session is False

    mlb.close()
    session.close()


def test_injected_session_headers_and_user_agent_are_not_modified():
    """Injected Session headers, including User-Agent, stay under caller control."""
    session = requests.Session()
    session.headers["User-Agent"] = "caller-agent/1.0"
    session.headers["X-Caller-Header"] = "keep-me"
    headers_before = dict(session.headers)

    mlb = Mlb(session=session)
    try:
        assert dict(session.headers) == headers_before
        assert session.headers["User-Agent"] == "caller-agent/1.0"
        assert session.headers["X-Caller-Header"] == "keep-me"
    finally:
        mlb.close()
        session.close()


def test_library_created_session_is_shared_by_both_adapters():
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        mlb = Mlb()

        assert session_cls.call_count == 1
        assert mlb._mlb_adapter_v1._session is session
        assert mlb._mlb_adapter_v1_1._session is session


def test_mlb_creates_exactly_one_session():
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        Mlb()
        assert session_cls.call_count == 1


# --- Mlb ownership ---


def test_mlb_close_closes_library_created_session_once():
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        mlb = Mlb()
        mlb.close()
        mlb.close()
        mlb.close()

        session.close.assert_called_once()


def test_mlb_close_does_not_close_injected_session():
    session = RecordingSession()
    mlb = Mlb(session=session)

    mlb.close()
    mlb.close()

    assert session.close_calls == 0


# --- Adapter ownership ---


def test_standalone_adapter_closes_library_created_session_once():
    with patch("mlbstatsapi.mlb_dataadapter.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        adapter = MlbDataAdapter()
        adapter.close()
        adapter.close()

        session.close.assert_called_once()


def test_standalone_adapter_does_not_close_injected_session():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session)

    adapter.close()
    adapter.close()

    assert session.close_calls == 0


# --- Context manager ---


def test_context_manager_enter_returns_same_instance():
    session = RecordingSession()
    mlb = Mlb(session=session)

    with mlb as entered:
        assert entered is mlb


def test_context_manager_closes_library_owned_session():
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        with Mlb() as mlb:
            assert isinstance(mlb, Mlb)

        session.close.assert_called_once()


def test_context_manager_does_not_close_injected_session():
    session = RecordingSession()

    with Mlb(session=session) as mlb:
        assert mlb._session is session

    assert session.close_calls == 0


def test_context_manager_closes_library_session_on_exception():
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        with pytest.raises(RuntimeError, match="boom"):
            with Mlb() as mlb:
                assert isinstance(mlb, Mlb)
                raise RuntimeError("boom")

        session.close.assert_called_once()


def test_context_manager_does_not_suppress_exception_with_injected_session():
    session = RecordingSession()

    with pytest.raises(RuntimeError, match="boom"):
        with Mlb(session=session):
            raise RuntimeError("boom")

    assert session.close_calls == 0


# --- Constructor compatibility ---


def test_mlb_default_constructor():
    mlb = Mlb()
    assert isinstance(mlb._session, requests.Session)
    mlb.close()


def test_mlb_positional_hostname():
    mlb = Mlb("statsapi.mlb.com")
    assert mlb._mlb_adapter_v1.url.startswith("https://statsapi.mlb.com/api/v1/")
    mlb.close()


def test_mlb_positional_hostname_and_logger():
    logger = MagicMock()
    logger.level = 0
    mlb = Mlb("statsapi.mlb.com", logger)
    assert mlb._logger is logger
    mlb.close()


def test_adapter_default_constructor():
    adapter = MlbDataAdapter()
    assert isinstance(adapter._session, requests.Session)
    adapter.close()


def test_adapter_positional_hostname():
    adapter = MlbDataAdapter("statsapi.mlb.com")
    assert adapter.url == "https://statsapi.mlb.com/api/v1/"
    adapter.close()


def test_adapter_positional_hostname_and_version():
    adapter = MlbDataAdapter("statsapi.mlb.com", "v1.1")
    assert adapter.url == "https://statsapi.mlb.com/api/v1.1/"
    adapter.close()


def test_adapter_positional_hostname_version_and_logger():
    logger = MagicMock()
    adapter = MlbDataAdapter("statsapi.mlb.com", "v1.1", logger)
    assert adapter._logger is logger
    adapter.close()


# --- Versioned User-Agent ---


@pytest.fixture
def mocked_package_version():
    """Patch the metadata lookup the production User-Agent helper uses."""
    with patch(
        "mlbstatsapi.mlb_dataadapter.package_version",
        return_value=MOCKED_PACKAGE_VERSION,
    ) as lookup:
        yield lookup


def test_user_agent_version_comes_from_package_metadata(mocked_package_version):
    """The User-Agent version is read from installed distribution metadata."""
    session = requests.Session()
    try:
        _configure_library_session(session)

        assert session.headers["User-Agent"] == MOCKED_USER_AGENT
    finally:
        session.close()

    mocked_package_version.assert_called_with(PACKAGE_DISTRIBUTION_NAME)


def test_mlb_library_created_session_has_versioned_user_agent(mocked_package_version):
    """Library-created Mlb Sessions send the package and version User-Agent."""
    mlb = Mlb()
    try:
        user_agent = mlb._session.headers["User-Agent"]

        assert "python-mlb-statsapi" in user_agent
        assert user_agent == MOCKED_USER_AGENT
    finally:
        mlb.close()


def test_standalone_adapter_session_has_versioned_user_agent(mocked_package_version):
    """Library-created standalone adapter Sessions use the same User-Agent."""
    adapter = MlbDataAdapter()
    try:
        assert adapter._session.headers["User-Agent"] == MOCKED_USER_AGENT
    finally:
        adapter.close()


def test_prepared_request_carries_versioned_user_agent(mocked_package_version):
    """The versioned User-Agent reaches the outgoing prepared request."""
    mlb = Mlb()
    try:
        prepared = mlb._session.prepare_request(
            requests.Request("GET", "https://example.test"),
        )

        assert prepared.headers["User-Agent"] == MOCKED_USER_AGENT
    finally:
        mlb.close()


def test_library_created_session_preserves_requests_default_headers():
    """Only User-Agent changes; other Requests default headers are untouched."""
    baseline = requests.Session()
    mlb = Mlb()
    try:
        for header, value in baseline.headers.items():
            if header.lower() == "user-agent":
                continue
            assert mlb._session.headers[header] == value

        for header in ("Accept-Encoding", "Accept", "Connection"):
            assert mlb._session.headers[header] == baseline.headers[header]

        assert mlb._session.headers["User-Agent"] != baseline.headers["User-Agent"]
    finally:
        mlb.close()
        baseline.close()


def test_injected_session_user_agent_is_preserved():
    """A caller-provided User-Agent is never overwritten by the library."""
    session = requests.Session()
    session.headers["User-Agent"] = "my-baseball-project/1.0"

    mlb = Mlb(session=session)
    try:
        assert session.headers["User-Agent"] == "my-baseball-project/1.0"
        assert mlb._session.headers["User-Agent"] == "my-baseball-project/1.0"
    finally:
        mlb.close()

    assert session.headers["User-Agent"] == "my-baseball-project/1.0"
    session.close()


def test_injected_session_custom_headers_are_preserved():
    """Custom headers on an injected Session survive construction and close()."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "my-baseball-project/1.0",
            "X-Application": "scoreboard",
        }
    )
    headers_before = dict(session.headers)

    mlb = Mlb(session=session)
    mlb.close()

    assert dict(session.headers) == headers_before
    assert session.headers["User-Agent"] == "my-baseball-project/1.0"
    assert session.headers["X-Application"] == "scoreboard"
    session.close()


def test_standalone_adapter_injected_session_headers_are_preserved():
    """A Session injected into MlbDataAdapter keeps all caller headers."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "my-baseball-project/1.0",
            "X-Application": "scoreboard",
        }
    )
    headers_before = dict(session.headers)

    adapter = MlbDataAdapter(session=session)
    try:
        assert dict(session.headers) == headers_before
        assert session.headers["User-Agent"] == "my-baseball-project/1.0"
        assert session.headers["X-Application"] == "scoreboard"
    finally:
        adapter.close()
        session.close()


def test_user_agent_falls_back_when_package_metadata_is_missing():
    """Missing distribution metadata yields a safe value instead of raising."""
    with patch(
        "mlbstatsapi.mlb_dataadapter.package_version",
        side_effect=PackageNotFoundError(PACKAGE_DISTRIBUTION_NAME),
    ):
        session = requests.Session()
        try:
            _configure_library_session(session)

            assert session.headers["User-Agent"] == "python-mlb-statsapi/unknown"
        finally:
            session.close()


def test_mlb_construction_succeeds_without_package_metadata():
    """Client construction still works in source-only environments."""
    with patch(
        "mlbstatsapi.mlb_dataadapter.package_version",
        side_effect=PackageNotFoundError(PACKAGE_DISTRIBUTION_NAME),
    ):
        mlb = Mlb()
        try:
            assert mlb._session.headers["User-Agent"] == "python-mlb-statsapi/unknown"
        finally:
            mlb.close()


def test_user_agent_does_not_change_library_retry_adapters(mocked_package_version):
    """Setting the User-Agent leaves the mounted retry adapters intact."""
    mlb = Mlb()
    try:
        assert mlb._session.headers["User-Agent"] == MOCKED_USER_AGENT
        assert_library_retry_policy(mlb._session.get_adapter("https://").max_retries)
        assert_library_retry_policy(mlb._session.get_adapter("http://").max_retries)
    finally:
        mlb.close()
