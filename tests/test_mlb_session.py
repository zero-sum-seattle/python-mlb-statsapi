"""Offline tests for shared HTTP sessions and configurable timeouts.

These tests cover session injection, ownership, cleanup, and timeout
forwarding without calling the live MLB API.
"""

from unittest.mock import MagicMock, patch

import requests

from mlbstatsapi import Mlb, MlbDataAdapter
from mlbstatsapi.mlb_dataadapter import DEFAULT_TIMEOUT


class RecordingSession:
    """Minimal session stand-in that records get() calls and close()."""

    def __init__(self):
        self.closed = False
        self.calls = []

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
        self.closed = True


def test_adapter_uses_configured_session():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session)

    result = adapter.get(endpoint="sports")

    assert result.status_code == 200
    assert len(session.calls) == 1
    assert session.calls[0]["url"].endswith("/sports")


def test_adapter_forwards_default_timeout():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session)

    adapter.get(endpoint="sports")

    assert session.calls[0]["timeout"] == DEFAULT_TIMEOUT
    assert session.calls[0]["timeout"] == (3.05, 30.0)


def test_adapter_forwards_custom_scalar_timeout():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session, timeout=10)

    adapter.get(endpoint="sports")

    assert session.calls[0]["timeout"] == 10


def test_adapter_forwards_custom_tuple_timeout():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session, timeout=(5.0, 60.0))

    adapter.get(endpoint="sports")

    assert session.calls[0]["timeout"] == (5.0, 60.0)


def test_mlb_forwards_timeout_to_adapters():
    session = RecordingSession()
    mlb = Mlb(session=session, timeout=(1.5, 20.0))

    mlb._mlb_adapter_v1.get(endpoint="sports")
    mlb._mlb_adapter_v1_1.get(endpoint="game")

    assert mlb._mlb_adapter_v1._timeout == (1.5, 20.0)
    assert mlb._mlb_adapter_v1_1._timeout == (1.5, 20.0)
    assert session.calls[0]["timeout"] == (1.5, 20.0)
    assert session.calls[1]["timeout"] == (1.5, 20.0)


def test_mlb_uses_default_timeout_when_none_supplied():
    session = RecordingSession()
    mlb = Mlb(session=session)

    mlb._mlb_adapter_v1.get(endpoint="sports")

    assert mlb._timeout == DEFAULT_TIMEOUT
    assert session.calls[0]["timeout"] == DEFAULT_TIMEOUT


def test_v1_and_v1_1_adapters_share_the_same_session():
    session = RecordingSession()
    mlb = Mlb(session=session)

    assert mlb._mlb_adapter_v1._session is session
    assert mlb._mlb_adapter_v1_1._session is session
    assert mlb._mlb_adapter_v1._session is mlb._mlb_adapter_v1_1._session


def test_library_created_session_is_shared_between_adapters():
    mlb = Mlb()

    assert mlb._mlb_adapter_v1._session is mlb._session
    assert mlb._mlb_adapter_v1_1._session is mlb._session
    assert mlb._mlb_adapter_v1._session is mlb._mlb_adapter_v1_1._session


def test_library_created_session_is_closed_by_mlb_close():
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        mlb = Mlb()
        mlb.close()

        session.close.assert_called_once()


def test_injected_session_is_not_closed_by_mlb_close():
    session = RecordingSession()
    mlb = Mlb(session=session)

    mlb.close()

    assert session.closed is False


def test_context_manager_closes_library_owned_session():
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        with Mlb() as mlb:
            assert mlb is not None

        session.close.assert_called_once()


def test_context_manager_does_not_close_injected_session():
    session = RecordingSession()

    with Mlb(session=session) as mlb:
        assert mlb._session is session

    assert session.closed is False


def test_context_manager_enter_returns_client():
    session = RecordingSession()

    with Mlb(session=session) as mlb:
        assert isinstance(mlb, Mlb)


def test_close_multiple_times_is_safe_for_library_owned_session():
    with patch("mlbstatsapi.mlb_api.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        mlb = Mlb()
        mlb.close()
        mlb.close()
        mlb.close()

        session.close.assert_called_once()


def test_close_multiple_times_is_safe_for_injected_session():
    session = RecordingSession()
    mlb = Mlb(session=session)

    mlb.close()
    mlb.close()

    assert session.closed is False


def test_adapter_close_closes_library_owned_session():
    with patch("mlbstatsapi.mlb_dataadapter.requests.Session") as session_cls:
        session = MagicMock()
        session_cls.return_value = session

        adapter = MlbDataAdapter()
        adapter.close()
        adapter.close()

        session.close.assert_called_once()


def test_adapter_close_does_not_close_injected_session():
    session = RecordingSession()
    adapter = MlbDataAdapter(session=session)

    adapter.close()
    adapter.close()

    assert session.closed is False


def test_existing_mlb_constructor_usage_remains_valid():
    mlb = Mlb()

    assert isinstance(mlb, Mlb)
    assert isinstance(mlb._session, requests.Session)
    assert mlb._timeout == DEFAULT_TIMEOUT
    mlb.close()


def test_existing_adapter_constructor_usage_remains_valid():
    adapter = MlbDataAdapter()

    assert isinstance(adapter, MlbDataAdapter)
    assert isinstance(adapter._session, requests.Session)
    assert adapter._timeout == DEFAULT_TIMEOUT
    adapter.close()


def test_positional_mlb_constructor_args_remain_valid():
    logger = MagicMock()
    logger.level = 0

    mlb = Mlb("statsapi.mlb.com", logger)

    assert mlb._mlb_adapter_v1.url.startswith("https://statsapi.mlb.com/api/v1/")
    assert mlb._logger is logger
    mlb.close()


def test_adapter_response_behavior_unchanged_with_session(requests_mock):
    adapter = MlbDataAdapter()
    requests_mock.get(
        "https://statsapi.mlb.com/api/v1/teams/19990",
        json={"message": "Object not found"},
        status_code=404,
        reason="Not Found",
    )

    result = adapter.get(endpoint="teams/19990")

    assert result.status_code == 404
    assert result.message == "Not Found"
    assert result.data == {}
    adapter.close()
