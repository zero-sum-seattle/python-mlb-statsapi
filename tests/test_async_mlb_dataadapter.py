"""Offline tests for AsyncMlbDataAdapter's bounded retry-with-backoff behavior.

Mirrors the retry contract asserted for the sync adapter in
tests/test_mlb_retries.py, adapted to httpx.MockTransport instead of a real
threaded HTTP server, since the async retry loop here is hand-rolled Python
rather than logic buried inside urllib3/requests internals.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import asyncio
import contextlib
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from mlbstatsapi import (
    MlbDecodeError,
    MlbHttpCompatibilityWarning,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
)
from mlbstatsapi.async_mlb_dataadapter import AsyncMlbDataAdapter

from http_contract_support import (
    RETRYABLE_STATUS_CODES,
    SERVER_ERRORS,
    assert_library_retry_policy,
)


BASE_URL = "https://statsapi.mlb.com/api/v1/"

SLEEP_TARGET = "mlbstatsapi.async_mlb_dataadapter.asyncio.sleep"


def run_async(coro):
    return asyncio.run(coro)


class _ScriptedHandler:
    """Serve a scripted sequence of httpx Responses/exceptions.

    The last entry repeats for any call beyond the script's length, so a
    single-item script models a persistent failure.
    """

    def __init__(self, *script: httpx.Response | Exception):
        self._script = list(script)
        self.call_count = 0

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.call_count += 1
        index = min(self.call_count - 1, len(self._script) - 1)
        item = self._script[index]
        if isinstance(item, Exception):
            raise item
        return item


def _response(status_code: int, *, headers: dict | None = None, text: str | None = None) -> httpx.Response:
    return httpx.Response(status_code, headers=headers or {}, text=text)


def _owned_adapter(handler, **kwargs) -> AsyncMlbDataAdapter:
    """Build an adapter that owns its client, so retries are active."""
    adapter = AsyncMlbDataAdapter(**kwargs)
    adapter._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return adapter


def _injected_adapter(handler, **kwargs) -> AsyncMlbDataAdapter:
    """Build an adapter with a caller-supplied client, so retries are bypassed."""
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return AsyncMlbDataAdapter(client=client, **kwargs)


def test_retry_policy_matches_library_default():
    adapter = AsyncMlbDataAdapter()
    assert_library_retry_policy(adapter._retry_policy)


def test_200_succeeds_with_no_retry():
    handler = _ScriptedHandler(_response(200))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock) as sleep_mock:
            result = await adapter.get(endpoint="sports")
            return result, sleep_mock

    result, sleep_mock = run_async(scenario())
    assert result.status_code == 200
    assert handler.call_count == 1
    sleep_mock.assert_not_awaited()


def test_200_response_returns_actual_json_data():
    payload = {"sports": [{"id": 1, "name": "Major League Baseball"}]}
    handler = _ScriptedHandler(httpx.Response(200, json=payload))

    async def scenario():
        adapter = _owned_adapter(handler)
        return await adapter.get(endpoint="sports")

    result = run_async(scenario())
    assert result.status_code == 200
    assert result.data == payload


def test_explicit_empty_successful_response_returns_empty_data():
    handler = _ScriptedHandler(_response(204, text=""))

    async def scenario():
        adapter = _owned_adapter(handler)
        return await adapter.get(endpoint="sports")

    result = run_async(scenario())
    assert result.status_code == 204
    assert result.data == {}


def test_mlb_http_error_has_structured_context():
    payload = {"messageNumber": 1, "message": "Internal error occurred"}
    handler = _ScriptedHandler(httpx.Response(500, json=payload))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbHttpError) as exc_info:
                await adapter.get(endpoint="sports")
            return exc_info.value

    error = run_async(scenario())
    assert error.status_code == 500
    assert error.reason == "Internal Server Error"
    assert error.method == "GET"
    assert error.url == f"{BASE_URL}sports"
    assert error.response_data == payload
    assert error.body_excerpt is not None
    assert "Internal error occurred" in error.body_excerpt


def test_library_owned_client_closes():
    async def scenario():
        adapter = AsyncMlbDataAdapter()
        was_open = not adapter._client.is_closed
        await adapter.aclose()
        return was_open, adapter._client.is_closed

    was_open, is_closed = run_async(scenario())
    assert was_open is True
    assert is_closed is True


def test_aclose_is_idempotent():
    async def scenario():
        adapter = AsyncMlbDataAdapter()
        await adapter.aclose()
        with patch.object(adapter._client, "aclose", new_callable=AsyncMock) as aclose_mock:
            await adapter.aclose()
            return aclose_mock

    aclose_mock = run_async(scenario())
    aclose_mock.assert_not_awaited()


def test_injected_client_is_not_closed():
    async def scenario():
        client = httpx.AsyncClient()
        adapter = AsyncMlbDataAdapter(client=client)
        await adapter.aclose()
        was_closed = client.is_closed
        await client.aclose()
        return was_closed

    was_closed = run_async(scenario())
    assert was_closed is False


def test_scalar_timeout_translation():
    result = AsyncMlbDataAdapter._translate_timeout(5)
    assert result.connect == 5
    assert result.read == 5
    assert result.write == 5
    assert result.pool == 5


def test_tuple_timeout_translation():
    result = AsyncMlbDataAdapter._translate_timeout((3.05, 30.0))
    assert result.connect == 3.05
    assert result.pool == 3.05
    assert result.read == 30.0
    assert result.write == 30.0


def test_multiple_concurrent_requests_on_one_adapter():
    responses = {
        "sports": httpx.Response(200, json={"id": "sports"}),
        "teams": httpx.Response(200, json={"id": "teams"}),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        endpoint = request.url.path.rsplit("/", 1)[-1]
        return responses[endpoint]

    async def scenario():
        adapter = _owned_adapter(handler)
        return await asyncio.gather(
            adapter.get(endpoint="sports"),
            adapter.get(endpoint="teams"),
        )

    sports_result, teams_result = run_async(scenario())
    assert sports_result.data == {"id": "sports"}
    assert teams_result.data == {"id": "teams"}


def test_cancelling_one_request_does_not_cancel_another():
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("hang"):
            await asyncio.sleep(10)
            raise AssertionError("handler should have been cancelled before returning")
        return _response(200)

    async def scenario():
        adapter = _owned_adapter(handler)

        hanging_task = asyncio.ensure_future(adapter.get(endpoint="hang"))
        await asyncio.sleep(0)

        other_task = asyncio.ensure_future(adapter.get(endpoint="sports"))

        hanging_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await hanging_task

        return await other_task

    result = run_async(scenario())
    assert result.status_code == 200


def test_injected_client_persistent_server_error_is_not_retried():
    handler = _ScriptedHandler(_response(500))

    async def scenario():
        adapter = _injected_adapter(handler)
        with pytest.raises(MlbHttpError) as exc_info:
            await adapter.get(endpoint="sports")
        return exc_info.value.status_code

    status_code = run_async(scenario())
    assert status_code == 500
    assert handler.call_count == 1


def test_injected_client_does_not_consume_a_second_scripted_response():
    handler = _ScriptedHandler(_response(500), _response(200))

    async def scenario():
        adapter = _injected_adapter(handler)
        with pytest.raises(MlbHttpError):
            await adapter.get(endpoint="sports")

    run_async(scenario())
    assert handler.call_count == 1


@pytest.mark.parametrize("status_code", RETRYABLE_STATUS_CODES)
def test_owned_client_retries_retryable_status_then_succeeds(status_code):
    handler = _ScriptedHandler(_response(status_code), _response(200))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            return await adapter.get(endpoint="sports")

    result = run_async(scenario())
    assert result.status_code == 200
    assert handler.call_count == 2


@pytest.mark.parametrize("status_code", SERVER_ERRORS)
def test_owned_client_exhausts_retries_on_persistent_server_error(status_code):
    handler = _ScriptedHandler(_response(status_code))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbHttpError) as exc_info:
                await adapter.get(endpoint="sports")
            return exc_info.value.status_code

    returned_status = run_async(scenario())
    assert returned_status == status_code
    assert handler.call_count == 4


def test_owned_client_final_429_raises_under_strict_http():
    handler = _ScriptedHandler(_response(429))

    async def scenario():
        adapter = _owned_adapter(handler, strict_http=True)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbHttpError) as exc_info:
                await adapter.get(endpoint="sports")
            return exc_info.value.status_code

    status_code = run_async(scenario())
    assert status_code == 429
    assert handler.call_count == 4


def test_owned_client_final_429_returns_empty_result_under_compatibility_mode():
    handler = _ScriptedHandler(_response(429))

    async def scenario():
        adapter = _owned_adapter(handler, strict_http=False)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
                result = await adapter.get(endpoint="sports")
            return result, warning_info

    result, warning_info = run_async(scenario())
    assert result.status_code == 429
    assert result.data == {}
    assert len(warning_info) == 1
    assert handler.call_count == 4


def test_400_is_not_retried():
    handler = _ScriptedHandler(_response(400), _response(200))

    async def scenario():
        adapter = _owned_adapter(handler)
        with pytest.raises(MlbHttpError):
            await adapter.get(endpoint="sports")

    run_async(scenario())
    assert handler.call_count == 1


def test_404_is_not_retried():
    handler = _ScriptedHandler(_response(404), _response(200))

    async def scenario():
        adapter = _owned_adapter(handler)
        return await adapter.get(endpoint="sports")

    result = run_async(scenario())
    assert result.status_code == 404
    assert result.data == {}
    assert handler.call_count == 1


def test_timeout_retried_then_succeeds():
    handler = _ScriptedHandler(httpx.ReadTimeout("timed out"), _response(200))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            return await adapter.get(endpoint="sports")

    result = run_async(scenario())
    assert result.status_code == 200
    assert handler.call_count == 2


def test_timeout_exhausts_retries_and_raises_mlb_timeout_error():
    handler = _ScriptedHandler(httpx.ReadTimeout("timed out"))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbTimeoutError):
                await adapter.get(endpoint="sports")

    run_async(scenario())
    assert handler.call_count == 3


def test_transport_error_retried_then_succeeds():
    handler = _ScriptedHandler(httpx.ConnectError("connection refused"), _response(200))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            return await adapter.get(endpoint="sports")

    result = run_async(scenario())
    assert result.status_code == 200
    assert handler.call_count == 2


def test_transport_error_exhausts_retries_and_raises_mlb_transport_error():
    handler = _ScriptedHandler(httpx.ConnectError("connection refused"))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbTransportError):
                await adapter.get(endpoint="sports")

    run_async(scenario())
    assert handler.call_count == 4


def test_retry_after_header_drives_sleep_duration():
    handler = _ScriptedHandler(
        _response(429, headers={"Retry-After": "7"}),
        _response(200),
    )

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock) as sleep_mock:
            await adapter.get(endpoint="sports")
            return sleep_mock

    sleep_mock = run_async(scenario())
    sleep_mock.assert_awaited_once_with(7)


def test_no_delay_before_first_retry():
    handler = _ScriptedHandler(_response(500), _response(200))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock) as sleep_mock:
            await adapter.get(endpoint="sports")
            return sleep_mock

    sleep_mock = run_async(scenario())
    sleep_mock.assert_not_awaited()


def test_backoff_grows_exponentially_between_retries():
    handler = _ScriptedHandler(_response(500))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock) as sleep_mock:
            with pytest.raises(MlbHttpError):
                await adapter.get(endpoint="sports")
            return sleep_mock

    sleep_mock = run_async(scenario())
    assert [call.args[0] for call in sleep_mock.await_args_list] == [1.0, 2.0]


def test_retry_sleep_is_async_and_non_blocking():
    """A real (unmocked) backoff wait must yield the event loop.

    If _sleep_before_retry ever used a blocking call (e.g. time.sleep)
    instead of `await asyncio.sleep(...)`, the whole event loop would
    freeze for the wait's duration and the concurrently running marker
    task below would make zero progress during it.
    """
    handler = _ScriptedHandler(_response(500), _response(500), _response(200))

    async def scenario():
        adapter = _owned_adapter(handler)
        # Small but real backoff so the test stays fast without mocking sleep.
        adapter._retry_policy.backoff_factor = 0.05

        marker_ticks = 0

        async def marker():
            nonlocal marker_ticks
            for _ in range(50):
                await asyncio.sleep(0.005)
                marker_ticks += 1

        marker_task = asyncio.ensure_future(marker())
        try:
            result = await adapter.get(endpoint="sports")
        finally:
            marker_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await marker_task

        return result, marker_ticks

    result, marker_ticks = run_async(scenario())
    assert result.status_code == 200
    assert marker_ticks > 0


def test_cancelled_error_propagates_without_retry_during_network_call():
    call_count = 0

    async def hanging_handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(10)
        raise AssertionError("handler should have been cancelled before returning")

    async def scenario():
        adapter = _owned_adapter(hanging_handler)
        task = asyncio.ensure_future(adapter.get(endpoint="sports"))
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    run_async(scenario())
    assert call_count == 1


def test_cancelled_error_propagates_without_retry_during_backoff_sleep():
    handler = _ScriptedHandler(_response(500), _response(500), _response(200))

    async def cancelling_sleep(delay):
        raise asyncio.CancelledError()

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, side_effect=cancelling_sleep):
            with pytest.raises(asyncio.CancelledError):
                await adapter.get(endpoint="sports")

    run_async(scenario())
    assert handler.call_count == 2


def test_json_decode_failure_is_not_retried():
    handler = _ScriptedHandler(_response(200, text="not json"))

    async def scenario():
        adapter = _owned_adapter(handler)
        with pytest.raises(MlbDecodeError):
            await adapter.get(endpoint="sports")

    run_async(scenario())
    assert handler.call_count == 1
