"""Offline tests for bounded HTTP retries and retry adapter configuration."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Iterable

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import mlbstatsapi
from mlbstatsapi import Mlb, MlbDataAdapter, MlbHttpError, MlbResult, create_retry_policy

from http_contract_support import (
    NON_RETRYABLE_CLIENT_ERRORS,
    RETRYABLE_STATUS_CODES,
    SERVER_ERRORS,
    assert_library_retry_policy,
)


def test_create_retry_policy_is_publicly_importable():
    """create_retry_policy is available through the package public API."""
    assert callable(mlbstatsapi.create_retry_policy)
    assert create_retry_policy is mlbstatsapi.create_retry_policy


def test_create_retry_policy_returns_retry_instance():
    """create_retry_policy returns an urllib3 Retry with the library policy."""
    policy = create_retry_policy()
    assert isinstance(policy, Retry)
    assert_library_retry_policy(policy)


def test_create_retry_policy_returns_independent_instances():
    """Each call returns a distinct Retry instance with the same configuration."""
    first = create_retry_policy()
    second = create_retry_policy()
    assert first is not second
    assert_library_retry_policy(first)
    assert_library_retry_policy(second)


def test_library_created_mlb_session_has_retry_policy():
    """Library-created Mlb Sessions mount the default retry policy on http/https."""
    mlb = Mlb()
    try:
        https_adapter = mlb._session.get_adapter("https://")
        http_adapter = mlb._session.get_adapter("http://")
        assert_library_retry_policy(https_adapter.max_retries)
        assert_library_retry_policy(http_adapter.max_retries)
        assert https_adapter.max_retries is not http_adapter.max_retries
    finally:
        mlb.close()


def test_library_created_adapter_session_has_retry_policy():
    """Library-created MlbDataAdapter Sessions mount the default retry policy."""
    adapter = MlbDataAdapter()
    try:
        https_adapter = adapter._session.get_adapter("https://")
        http_adapter = adapter._session.get_adapter("http://")
        assert_library_retry_policy(https_adapter.max_retries)
        assert_library_retry_policy(http_adapter.max_retries)
        assert https_adapter.max_retries is not http_adapter.max_retries
    finally:
        adapter.close()


def test_injected_session_adapters_are_not_replaced():
    """Mlb must not replace adapters or retry config on an injected Session."""
    session = requests.Session()
    custom_adapter = HTTPAdapter(max_retries=0)
    session.mount("https://", custom_adapter)

    mlb = Mlb(session=session)
    try:
        assert session.get_adapter("https://") is custom_adapter
        assert session.get_adapter("https://").max_retries.total == 0
    finally:
        mlb.close()
        session.close()


def test_injected_adapter_session_adapters_are_not_replaced():
    """Standalone adapters must not replace adapters on an injected Session."""
    session = requests.Session()
    custom_adapter = HTTPAdapter(max_retries=0)
    session.mount("http://", custom_adapter)

    adapter = MlbDataAdapter(session=session)
    try:
        assert session.get_adapter("http://") is custom_adapter
        assert session.get_adapter("http://").max_retries.total == 0
    finally:
        adapter.close()
        session.close()


def test_caller_can_opt_in_to_public_retry_policy():
    """Callers may mount create_retry_policy() on their own Session."""
    session = requests.Session()
    https_adapter = HTTPAdapter(max_retries=create_retry_policy())
    http_adapter = HTTPAdapter(max_retries=create_retry_policy())
    session.mount("https://", https_adapter)
    session.mount("http://", http_adapter)

    mlb = Mlb(session=session)
    try:
        assert mlb._session is session
        assert mlb._owns_session is False
        assert session.get_adapter("https://") is https_adapter
        assert session.get_adapter("http://") is http_adapter
        assert_library_retry_policy(https_adapter.max_retries)
        assert_library_retry_policy(http_adapter.max_retries)
        assert https_adapter.max_retries is not http_adapter.max_retries
    finally:
        mlb.close()
        # Injected Sessions remain caller-owned after Mlb.close().
        assert session.get_adapter("https://") is https_adapter
        assert session.get_adapter("http://") is http_adapter
        session.close()


class _ScriptedHandler(BaseHTTPRequestHandler):
    """Serve a scripted sequence of HTTP status codes for retry tests."""

    statuses: list[int] = []
    request_count = 0
    lock = threading.Lock()

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        with self.lock:
            index = self.request_count
            self.__class__.request_count += 1

        if index < len(self.statuses):
            status = self.statuses[index]
        else:
            status = self.statuses[-1] if self.statuses else 500

        body = b""
        if status == 200:
            body = json.dumps({"sports": [{"id": 1}]}).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


@pytest.fixture
def scripted_http_server():
    """Start a local HTTP server that returns a caller-provided status sequence."""

    server = ThreadingHTTPServer(("127.0.0.1", 0), _ScriptedHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]

    def configure(statuses: Iterable[int]) -> None:
        _ScriptedHandler.statuses = list(statuses)
        _ScriptedHandler.request_count = 0

    try:
        yield configure, port
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture
def no_retry_sleep(monkeypatch):
    monkeypatch.setattr(Retry, "sleep", lambda self, response=None: None)


def _adapter_against_local_server(port: int) -> MlbDataAdapter:
    adapter = MlbDataAdapter()
    adapter.url = f"http://127.0.0.1:{port}/api/v1/"
    return adapter


def test_retries_recover_from_two_500_responses(
    scripted_http_server,
    no_retry_sleep,
):
    """Transient 500s are retried and a later 200 succeeds."""
    configure, port = scripted_http_server
    configure([500, 500, 200])
    adapter = _adapter_against_local_server(port)

    try:
        result = adapter.get(endpoint="sports")
    finally:
        adapter.close()

    assert isinstance(result, MlbResult)
    assert result.status_code == 200
    assert result.data == {"sports": [{"id": 1}]}
    assert _ScriptedHandler.request_count == 3


@pytest.mark.parametrize("retryable_status", RETRYABLE_STATUS_CODES)
def test_retries_retryable_statuses_then_succeed(
    retryable_status,
    scripted_http_server,
    no_retry_sleep,
):
    """Each retryable status is retried once and can recover on success."""
    configure, port = scripted_http_server
    configure([retryable_status, 200])
    adapter = _adapter_against_local_server(port)

    try:
        result = adapter.get(endpoint="sports")
    finally:
        adapter.close()

    assert result.status_code == 200
    assert result.data == {"sports": [{"id": 1}]}
    assert _ScriptedHandler.request_count == 2


@pytest.mark.parametrize("status_code", NON_RETRYABLE_CLIENT_ERRORS)
def test_non_retryable_client_errors_are_not_retried(
    status_code,
    scripted_http_server,
    no_retry_sleep,
):
    """Ordinary client errors are returned immediately without retries."""
    configure, port = scripted_http_server
    configure([status_code, 200])
    adapter = _adapter_against_local_server(port)

    try:
        result = adapter.get(endpoint="sports")
    finally:
        adapter.close()

    assert result.status_code == status_code
    assert result.data == {}
    assert _ScriptedHandler.request_count == 1


@pytest.mark.parametrize("status_code", SERVER_ERRORS)
def test_bounded_persistent_server_errors_raise_after_four_attempts(
    status_code,
    scripted_http_server,
    no_retry_sleep,
):
    """Persistent server errors raise MlbHttpError after initial try plus 3 retries."""
    configure, port = scripted_http_server
    configure([status_code] * 6)
    adapter = _adapter_against_local_server(port)

    try:
        with pytest.raises(MlbHttpError) as exc_info:
            adapter.get(endpoint="sports")
    finally:
        adapter.close()

    assert exc_info.value.status_code == status_code
    assert _ScriptedHandler.request_count == 4


def test_final_429_returns_empty_mlb_result(
    scripted_http_server,
    no_retry_sleep,
):
    """After retry exhaustion, a final 429 still returns an empty MlbResult."""
    configure, port = scripted_http_server
    configure([429, 429, 429, 429, 429, 429])
    adapter = _adapter_against_local_server(port)

    try:
        result = adapter.get(endpoint="sports")
    finally:
        adapter.close()

    assert isinstance(result, MlbResult)
    assert result.status_code == 429
    assert result.data == {}
    assert _ScriptedHandler.request_count == 4


def test_invalid_json_is_not_retried(no_retry_sleep):
    """JSON decode failures are not treated as retryable transport errors."""
    class BadJsonHandler(_ScriptedHandler):
        def do_GET(self) -> None:  # noqa: N802
            with self.lock:
                self.__class__.request_count += 1
            body = b'{"bad": json'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(("127.0.0.1", 0), BadJsonHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    BadJsonHandler.request_count = 0
    adapter = MlbDataAdapter()
    adapter.url = f"http://127.0.0.1:{server.server_address[1]}/api/v1/"

    try:
        from mlbstatsapi import MlbDecodeError

        with pytest.raises(MlbDecodeError, match=r"^Bad JSON in response$"):
            adapter.get(endpoint="sports")
        assert BadJsonHandler.request_count == 1
    finally:
        adapter.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
