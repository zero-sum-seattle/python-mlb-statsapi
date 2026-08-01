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

from mlbstatsapi import Mlb, MlbDataAdapter, MlbHttpError, MlbResult


def _assert_retry_policy(retry: Retry) -> None:
    assert retry.total == 3
    assert retry.connect == 3
    assert retry.read == 2
    assert retry.status == 3
    assert retry.backoff_factor == 0.5
    assert set(retry.status_forcelist) == {429, 500, 502, 503, 504}
    assert retry.allowed_methods == frozenset({"GET"})
    assert retry.respect_retry_after_header is True
    assert retry.raise_on_status is False
    assert "POST" not in retry.allowed_methods
    assert "PATCH" not in retry.allowed_methods
    assert "DELETE" not in retry.allowed_methods


def test_library_created_mlb_session_has_retry_policy():
    mlb = Mlb()
    try:
        for scheme in ("https://", "http://"):
            adapter = mlb._session.get_adapter(scheme)
            _assert_retry_policy(adapter.max_retries)
    finally:
        mlb.close()


def test_library_created_adapter_session_has_retry_policy():
    adapter = MlbDataAdapter()
    try:
        for scheme in ("https://", "http://"):
            http_adapter = adapter._session.get_adapter(scheme)
            _assert_retry_policy(http_adapter.max_retries)
    finally:
        adapter.close()


def test_injected_session_adapters_are_not_replaced():
    session = requests.Session()
    custom_adapter = HTTPAdapter(max_retries=0)
    session.mount("https://", custom_adapter)

    mlb = Mlb(session=session)
    try:
        assert session.get_adapter("https://") is custom_adapter
    finally:
        mlb.close()
        session.close()


def test_injected_adapter_session_adapters_are_not_replaced():
    session = requests.Session()
    custom_adapter = HTTPAdapter(max_retries=0)
    session.mount("http://", custom_adapter)

    adapter = MlbDataAdapter(session=session)
    try:
        assert session.get_adapter("http://") is custom_adapter
    finally:
        adapter.close()
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


@pytest.mark.parametrize(
    "retryable_status",
    [429, 500, 502, 503, 504],
)
def test_retries_retryable_statuses_then_succeed(
    retryable_status,
    scripted_http_server,
    no_retry_sleep,
):
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


@pytest.mark.parametrize(
    "status_code",
    [400, 401, 403, 404],
)
def test_non_retryable_client_errors_are_not_retried(
    status_code,
    scripted_http_server,
    no_retry_sleep,
):
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


def test_bounded_persistent_500_raises_after_four_attempts(
    scripted_http_server,
    no_retry_sleep,
):
    configure, port = scripted_http_server
    configure([500, 500, 500, 500, 500, 500])
    adapter = _adapter_against_local_server(port)

    try:
        with pytest.raises(MlbHttpError) as exc_info:
            adapter.get(endpoint="sports")
    finally:
        adapter.close()

    assert exc_info.value.status_code == 500
    assert exc_info.value.reason == "Internal Server Error"
    assert _ScriptedHandler.request_count == 4


def test_final_429_returns_empty_mlb_result(
    scripted_http_server,
    no_retry_sleep,
):
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
