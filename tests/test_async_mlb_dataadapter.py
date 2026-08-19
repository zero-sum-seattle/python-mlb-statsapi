"""Focused offline tests for the AsyncMlbDataAdapter implementation.

Covers the behavior delivered in issue #301: successful GETs, the HTTP status
contract, exception mapping, lifecycle and ownership, timeout translation,
User-Agent, bounded retry-with-backoff, cancellation, and concurrency. The
exhaustive async transport-contract matrix belongs to #302.

The retry assertions mirror the contract asserted for the sync adapter in
tests/test_mlb_retries.py, adapted to httpx.MockTransport instead of a real
threaded HTTP server, since the async retry loop here is hand-rolled Python
rather than logic buried inside urllib3/requests internals.

HTTPX ships only with the ``async`` extra, so the whole module skips when it is
absent. See the import section below.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import warnings
from importlib.metadata import PackageNotFoundError
from unittest.mock import AsyncMock, patch

import pytest

# Every test below drives the real HTTPX-backed adapter, so a sync-only install
# has nothing here to run. Skipping at collection keeps ``pytest tests/``
# working without the ``async`` extra instead of erroring on the import. The
# optional-dependency contract itself is asserted in
# tests/test_async_optional_dependency.py, which runs with or without HTTPX.
httpx = pytest.importorskip("httpx", reason="requires the async extra (HTTPX)")

from mlbstatsapi import (  # noqa: E402
    MlbDecodeError,
    MlbHttpCompatibilityWarning,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
)
from mlbstatsapi.async_mlb_dataadapter import AsyncMlbDataAdapter  # noqa: E402
from mlbstatsapi.mlb_dataadapter import PACKAGE_DISTRIBUTION_NAME  # noqa: E402

from http_contract_support import (  # noqa: E402
    HTTP_REASON_BY_STATUS,
    RETRYABLE_STATUS_CODES,
    SERVER_ERRORS,
    assert_library_retry_policy,
)


BASE_URL = "https://statsapi.mlb.com/api/v1/"

SLEEP_TARGET = "mlbstatsapi.async_mlb_dataadapter.asyncio.sleep"

# Patched only while a test adapter is constructed, so the adapter creates its
# own library-owned client the way production does, over a MockTransport.
CLIENT_TARGET = "mlbstatsapi.async_mlb_dataadapter.httpx.AsyncClient"

# Matches tests/test_mlb_session.py, so both adapters assert the same contract.
MOCKED_PACKAGE_VERSION = "9.8.7"
MOCKED_USER_AGENT = f"python-mlb-statsapi/{MOCKED_PACKAGE_VERSION}"

# Obvious sentinels, so a leak into a compatibility warning is unmistakable.
SECRET_BODY_MARKER = "SUPER_SECRET_RESPONSE"
SECRET_HEADER_MARKER = "SUPER_SECRET_HEADER"

# Failure guard for the concurrency tests: a request that should never wait is
# bounded so a serializing regression fails fast instead of hanging CI.
BLOCKED_REQUEST_TIMEOUT = 10


# Adapters built by _owned_adapter(); run_async() closes them inside the same
# event loop that used them, so no AsyncClient is left open by a test.
_ADAPTERS_TO_CLOSE: list[AsyncMlbDataAdapter] = []


def run_async(coro):
    async def runner():
        try:
            return await coro
        finally:
            while _ADAPTERS_TO_CLOSE:
                await _ADAPTERS_TO_CLOSE.pop().aclose()

    return asyncio.run(runner())


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
    """Build an adapter that owns its client, so retries are active.

    The adapter still builds its own client through the production path — only
    the transport is swapped for a MockTransport — so ownership, headers, and
    retry behavior are exactly what the library does at runtime, and no client
    is constructed and then discarded. Call this from inside a run_async()
    scenario; run_async() closes what it creates.
    """
    real_async_client = httpx.AsyncClient

    def mock_transport_client(**client_kwargs) -> httpx.AsyncClient:
        return real_async_client(
            transport=httpx.MockTransport(handler),
            **client_kwargs,
        )

    with patch(CLIENT_TARGET, mock_transport_client):
        adapter = AsyncMlbDataAdapter(**kwargs)

    _ADAPTERS_TO_CLOSE.append(adapter)
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


def test_injected_client_timeout_configuration_is_not_mutated():
    """The library's timeout is applied per request, not written to the client."""
    handler = _ScriptedHandler(_response(200))

    async def scenario():
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(handler),
            timeout=httpx.Timeout(11.0),
        )
        try:
            adapter = AsyncMlbDataAdapter(client=client, timeout=(1.0, 2.0))
            await adapter.get(endpoint="sports")
            return client.timeout
        finally:
            await client.aclose()

    timeout = run_async(scenario())
    assert timeout.connect == 11.0
    assert timeout.read == 11.0
    assert timeout.write == 11.0
    assert timeout.pool == 11.0


# --- Explicit cleanup after the adapter has been used ---
#
# test_library_owned_client_closes covers an adapter that never issued a
# request. These cover the states a request can leave behind: success, a
# public failure, and caller cancellation. In each case explicit cleanup must
# still close the library-owned client without altering what the caller
# already observed.


def test_owned_client_closes_after_a_successful_request():
    """A used adapter is still safely closable."""
    handler = _ScriptedHandler(httpx.Response(200, json={"id": "sports"}))

    async def scenario():
        adapter = _owned_adapter(handler)
        result = await adapter.get(endpoint="sports")
        await adapter.aclose()
        return result, adapter._client.is_closed

    result, is_closed = run_async(scenario())
    assert result.status_code == 200
    assert result.data == {"id": "sports"}
    assert is_closed is True


def test_owned_client_closes_after_a_failed_request():
    """A failed request leaves the adapter closable, and the error intact."""
    handler = _ScriptedHandler(_response(503))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbHttpError) as exc_info:
                await adapter.get(endpoint="sports")

        error = exc_info.value
        await adapter.aclose()
        return error, adapter._client.is_closed

    error, is_closed = run_async(scenario())
    assert error.status_code == 503
    assert error.reason == HTTP_REASON_BY_STATUS[503]
    assert error.method == "GET"
    assert error.url == f"{BASE_URL}sports"
    assert is_closed is True


def test_owned_client_closes_after_a_cancelled_request():
    """Cancelling an in-flight request still leaves the adapter closable.

    The cancellation itself stays the caller's outcome: aclose() runs after
    CancelledError has already propagated, and does not replace it.
    """
    async def scenario():
        request_started = asyncio.Event()

        async def hanging_handler(request: httpx.Request) -> httpx.Response:
            request_started.set()
            await asyncio.sleep(10)
            raise AssertionError("handler should have been cancelled before returning")

        adapter = _owned_adapter(hanging_handler)
        task = asyncio.ensure_future(adapter.get(endpoint="sports"))
        # Cancel only once the request is genuinely in flight.
        await asyncio.wait_for(request_started.wait(), BLOCKED_REQUEST_TIMEOUT)

        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        await adapter.aclose()
        return adapter._client.is_closed

    is_closed = run_async(scenario())
    assert is_closed is True


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
    """Concurrent requests keep their own params and their own response.

    Each request carries different ep_params, so neither the query sent to the
    transport nor the returned data may pick up the other request's values.
    """
    responses = {
        "sports": httpx.Response(200, json={"id": "sports"}),
        "teams": httpx.Response(200, json={"id": "teams"}),
    }
    observed_params: dict[str, dict[str, str]] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        endpoint = request.url.path.rsplit("/", 1)[-1]
        observed_params[endpoint] = dict(request.url.params)
        return responses[endpoint]

    async def scenario():
        adapter = _owned_adapter(handler)
        return await asyncio.gather(
            adapter.get(endpoint="sports", ep_params={"sportId": 1}),
            adapter.get(endpoint="teams", ep_params={"season": 2026}),
        )

    sports_result, teams_result = run_async(scenario())
    assert sports_result.data == {"id": "sports"}
    assert teams_result.data == {"id": "teams"}
    # Query values arrive as strings; each endpoint sees only its own params.
    assert observed_params == {
        "sports": {"sportId": "1"},
        "teams": {"season": "2026"},
    }


def test_failure_of_one_concurrent_request_does_not_affect_another():
    """A failing request must not disturb an unrelated concurrent request.

    Request A exhausts the status retry budget and raises MlbHttpError while
    request B, sharing the same adapter and client, still completes normally
    on its single attempt.
    """
    attempts: dict[str, int] = {"sports": 0, "teams": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        endpoint = request.url.path.rsplit("/", 1)[-1]
        attempts[endpoint] += 1
        if endpoint == "sports":
            return _response(503)
        return httpx.Response(200, json={"id": "teams"})

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            # Caller-controlled orchestration: gather is the caller's choice,
            # so a failure in A is reported without cancelling B.
            return await asyncio.gather(
                adapter.get(endpoint="sports"),
                adapter.get(endpoint="teams"),
                return_exceptions=True,
            )

    failure, success = run_async(scenario())
    assert isinstance(failure, MlbHttpError)
    assert failure.status_code == 503
    assert success.status_code == 200
    assert success.data == {"id": "teams"}
    # A spent its full status budget; B was never retried on A's behalf.
    assert attempts == {"sports": 4, "teams": 1}


def test_backoff_in_one_request_does_not_block_another():
    """Another request makes progress while one is waiting out its backoff.

    test_retry_sleep_is_async_and_non_blocking proves an unrelated task keeps
    running during backoff; this proves the same for a second request on the
    same adapter, without depending on wall-clock timing: B's result exists
    before b_completed is set, so A cannot have left its backoff first.
    """
    attempts: dict[str, int] = {"sports": 0, "teams": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        endpoint = request.url.path.rsplit("/", 1)[-1]
        attempts[endpoint] += 1
        # The first retry has no delay, so A must fail twice to reach a real
        # backoff wait; the third attempt succeeds once the test releases it.
        if endpoint == "sports" and attempts["sports"] <= 2:
            return _response(503)
        return httpx.Response(200, json={"id": endpoint})

    async def scenario():
        a_in_backoff = asyncio.Event()
        b_completed = asyncio.Event()

        async def parked_backoff(delay):
            a_in_backoff.set()
            await b_completed.wait()

        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, parked_backoff):
            a_task = asyncio.ensure_future(adapter.get(endpoint="sports"))
            await asyncio.wait_for(a_in_backoff.wait(), BLOCKED_REQUEST_TIMEOUT)

            # Not a timing assertion: on the passing path nothing waits. The
            # bound only turns a regression that serializes requests into a
            # fast failure instead of a hung test run.
            b_result = await asyncio.wait_for(
                adapter.get(endpoint="teams"),
                BLOCKED_REQUEST_TIMEOUT,
            )

            b_completed.set()
            a_result = await a_task

        return a_result, b_result

    a_result, b_result = run_async(scenario())
    assert b_result.status_code == 200
    assert b_result.data == {"id": "teams"}
    assert a_result.status_code == 200
    assert attempts == {"sports": 3, "teams": 1}


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


def test_persistent_server_error_raises_despite_compatibility_mode():
    """A final 5xx raises MlbHttpError regardless of strict_http.

    Compatibility mode suppresses non-404 4xx only. A server error is never
    downgraded to a warned empty MlbResult, so strict_http=False must not
    change either the exception or the retry behavior here.
    """
    handler = _ScriptedHandler(_response(503))

    async def scenario():
        adapter = _owned_adapter(handler, strict_http=False)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always", MlbHttpCompatibilityWarning)
                with pytest.raises(MlbHttpError) as exc_info:
                    await adapter.get(endpoint="sports")

        return exc_info.value.status_code, caught

    status_code, caught = run_async(scenario())
    assert status_code == 503
    # One initial attempt plus the status retry budget.
    assert handler.call_count == 4
    compatibility = [
        warning
        for warning in caught
        if issubclass(warning.category, MlbHttpCompatibilityWarning)
    ]
    assert compatibility == []


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


def test_other_non_2xx_status_raises_http_error():
    """A final non-2xx outside the 4xx/5xx ranges still raises MlbHttpError."""
    handler = _ScriptedHandler(
        _response(302, headers={"Location": "https://example.test/moved"}),
    )

    async def scenario():
        # Redirects are not followed, so the 302 reaches the status contract.
        adapter = _owned_adapter(handler)
        with pytest.raises(MlbHttpError) as exc_info:
            await adapter.get(endpoint="sports")
        return exc_info.value

    error = run_async(scenario())
    assert error.status_code == 302
    assert error.method == "GET"
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


def test_connect_timeout_exhausts_retries_and_raises_mlb_timeout_error():
    """A connect timeout stays a timeout for the caller.

    httpx.ConnectTimeout subclasses httpx.TimeoutException, so it needs its
    own branch to spend the connect budget while still raising
    MlbTimeoutError rather than MlbTransportError.
    """
    handler = _ScriptedHandler(httpx.ConnectTimeout("connect timed out"))

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbTimeoutError) as exc_info:
                await adapter.get(endpoint="sports")
            return exc_info.value

    error = run_async(scenario())
    assert handler.call_count == 4
    # MlbTimeoutError subclasses MlbTransportError, so only the exact type
    # distinguishes a timeout from a plain transport failure.
    assert type(error) is MlbTimeoutError
    assert isinstance(error.__cause__, httpx.ConnectTimeout)


def test_connect_timeout_spends_the_connect_retry_budget():
    """The connect budget bounds a connect timeout, not the total or read one.

    The default policy uses total=3 and connect=3, so attempt counts alone
    cannot tell those two budgets apart. Narrowing connect makes the
    difference observable: falling through to the generic timeout branch
    would still allow four attempts here.
    """
    handler = _ScriptedHandler(httpx.ConnectTimeout("connect timed out"))

    async def scenario():
        adapter = _owned_adapter(handler)
        adapter._retry_policy.connect = 1
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbTimeoutError):
                await adapter.get(endpoint="sports")

    run_async(scenario())
    assert handler.call_count == 2


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


# --- Retry budget independence ---
#
# The default policy uses total=3, connect=3 and status=3, so an attempt count
# of four cannot tell those budgets apart. Each test below narrows the single
# budget it is about, which makes the observed attempt count uniquely
# attributable to that budget while the public failure stays unchanged.


@pytest.mark.parametrize(
    "failure, expected_exception",
    ((httpx.PoolTimeout("pool timed out"), MlbTimeoutError),),
    ids=("timeout",),
)
def test_generic_failures_spend_the_total_retry_budget(failure, expected_exception):
    """A generic timeout is bounded by the total budget.

    A pool timeout is neither a connect nor a read timeout, so it falls
    through to the generic timeout handling. Narrowing total to one retry
    makes that budget observable: spending connect (3) or read (2) instead
    would allow four or three attempts here.
    """
    handler = _ScriptedHandler(failure)

    async def scenario():
        adapter = _owned_adapter(handler)
        adapter._retry_policy.total = 1
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(expected_exception) as exc_info:
                await adapter.get(endpoint="sports")
            return exc_info.value

    error = run_async(scenario())
    assert handler.call_count == 2
    # MlbTimeoutError subclasses MlbTransportError, so only the exact type
    # separates a timeout from a plain transport failure.
    assert type(error) is expected_exception
    assert isinstance(error.__cause__, type(failure))


def test_connect_error_spends_the_connect_retry_budget():
    """A connection failure is bounded by the connect budget, not the total one.

    test_transport_error_exhausts_retries_and_raises_mlb_transport_error shows
    four attempts under the default policy, which total=3 would also produce.
    """
    handler = _ScriptedHandler(httpx.ConnectError("connection refused"))

    async def scenario():
        adapter = _owned_adapter(handler)
        adapter._retry_policy.connect = 1
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbTransportError):
                await adapter.get(endpoint="sports")

    run_async(scenario())
    assert handler.call_count == 2


def test_retryable_status_spends_the_status_retry_budget():
    """Retryable statuses are bounded by the status budget, not the total one."""
    handler = _ScriptedHandler(_response(503))

    async def scenario():
        adapter = _owned_adapter(handler)
        adapter._retry_policy.status = 1
        with patch(SLEEP_TARGET, new_callable=AsyncMock):
            with pytest.raises(MlbHttpError) as exc_info:
                await adapter.get(endpoint="sports")
            return exc_info.value.status_code

    status_code = run_async(scenario())
    assert status_code == 503
    assert handler.call_count == 2


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
        with pytest.raises(MlbDecodeError) as exc_info:
            await adapter.get(endpoint="sports")
        return exc_info.value

    error = run_async(scenario())
    # Matches the sync adapter: the underlying decode failure stays the cause.
    assert isinstance(error.__cause__, ValueError)
    assert handler.call_count == 1


# --- Final non-404 4xx contract ---


def test_final_non_404_client_error_raises_under_strict_http():
    """Strict mode raises MlbHttpError with the sync structured context.

    test_400_is_not_retried already proves a 4xx is final on the first
    response; this asserts the #298 decision-table outcome for an explicit
    strict_http=True adapter, including the structured error context.
    """
    handler = _ScriptedHandler(_response(403))

    async def scenario():
        adapter = _owned_adapter(handler, strict_http=True)
        with pytest.raises(MlbHttpError) as exc_info:
            await adapter.get(endpoint="sports")
        return exc_info.value

    error = run_async(scenario())
    assert error.status_code == 403
    assert error.reason == HTTP_REASON_BY_STATUS[403]
    assert error.method == "GET"
    assert error.url == f"{BASE_URL}sports"
    assert handler.call_count == 1


def test_final_non_404_client_error_returns_empty_result_in_compatibility_mode():
    """strict_http=False suppresses a non-404 4xx into a warned empty result."""
    handler = _ScriptedHandler(_response(403, text='{"message": "denied"}'))

    async def scenario():
        adapter = _owned_adapter(handler, strict_http=False)
        with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
            result = await adapter.get(endpoint="sports")
        return result, [str(warning.message) for warning in warning_info]

    result, messages = run_async(scenario())
    assert result.status_code == 403
    assert result.message == HTTP_REASON_BY_STATUS[403]
    assert result.data == {}
    assert len(messages) == 1
    assert "403" in messages[0]
    assert f"{BASE_URL}sports" in messages[0]
    assert handler.call_count == 1


# --- Compatibility warning safety ---


def test_compatibility_warning_does_not_leak_response_body_or_headers():
    """Response bodies and headers must never reach the warning message."""
    handler = _ScriptedHandler(
        _response(
            403,
            headers={"X-Debug-Token": SECRET_HEADER_MARKER},
            text=f'{{"message": "{SECRET_BODY_MARKER}"}}',
        ),
    )

    async def scenario():
        adapter = _owned_adapter(handler, strict_http=False)
        with pytest.warns(MlbHttpCompatibilityWarning) as warning_info:
            await adapter.get(endpoint="sports")
        return [str(warning.message) for warning in warning_info]

    messages = run_async(scenario())
    assert len(messages) == 1
    assert SECRET_BODY_MARKER not in messages[0]
    assert SECRET_HEADER_MARKER not in messages[0]
    assert "X-Debug-Token" not in messages[0]


def test_compatibility_warning_points_to_awaiting_caller_line():
    """The warning is attributed to the awaiting caller, not package internals.

    Mirrors test_http_warnings.test_compatibility_warning_points_to_direct_
    adapter_caller_line for an awaited call.
    """
    handler = _ScriptedHandler(_response(403))

    async def scenario():
        adapter = _owned_adapter(handler, strict_http=False)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", MlbHttpCompatibilityWarning)
            expected_lineno = inspect.currentframe().f_lineno + 1
            await adapter.get(endpoint="sports")
        return caught, expected_lineno

    caught, expected_lineno = run_async(scenario())
    compatibility = [
        warning
        for warning in caught
        if issubclass(warning.category, MlbHttpCompatibilityWarning)
    ]
    assert len(compatibility) == 1
    assert compatibility[0].filename == __file__
    assert compatibility[0].lineno == expected_lineno


# --- Structured MlbHttpError context ---


def test_error_context_extraction_failure_does_not_replace_http_error():
    """A broken optional-context extraction must not hide the HTTP failure.

    The best-effort response context is a debugging aid, so a failure while
    collecting it degrades that one field instead of raising something other
    than the original MlbHttpError.
    """
    handler = _ScriptedHandler(
        _response(500, text='{"message": "Internal error occurred"}'),
    )

    async def scenario():
        adapter = _owned_adapter(handler)
        with patch(
            "mlbstatsapi._http._extract_error_response_data",
            side_effect=RuntimeError("error-context extraction failed"),
        ):
            with patch(SLEEP_TARGET, new_callable=AsyncMock):
                with pytest.raises(MlbHttpError) as exc_info:
                    await adapter.get(endpoint="sports")
        return exc_info.value

    error = run_async(scenario())
    assert error.status_code == 500
    assert error.reason == HTTP_REASON_BY_STATUS[500]
    assert error.method == "GET"
    assert error.url == f"{BASE_URL}sports"
    assert error.response_data is None
    # The independent excerpt extraction still succeeds.
    assert "Internal error occurred" in (error.body_excerpt or "")


# --- Versioned User-Agent ---


def test_library_owned_client_has_versioned_user_agent():
    """A library-created AsyncClient sends the package and version User-Agent."""
    with patch(
        "mlbstatsapi.mlb_dataadapter.package_version",
        return_value=MOCKED_PACKAGE_VERSION,
    ) as lookup:
        adapter = AsyncMlbDataAdapter()
        try:
            assert adapter._client.headers["User-Agent"] == MOCKED_USER_AGENT
        finally:
            run_async(adapter.aclose())

    lookup.assert_called_with(PACKAGE_DISTRIBUTION_NAME)


def test_library_owned_client_user_agent_uses_installed_version():
    """Without patching, the User-Agent still names this package."""
    adapter = AsyncMlbDataAdapter()
    try:
        assert adapter._client.headers["User-Agent"].startswith(
            f"{PACKAGE_DISTRIBUTION_NAME}/",
        )
    finally:
        run_async(adapter.aclose())


def test_library_owned_client_user_agent_falls_back_when_metadata_missing():
    """Missing distribution metadata yields the "unknown" fallback, not an error."""
    with patch(
        "mlbstatsapi.mlb_dataadapter.package_version",
        side_effect=PackageNotFoundError(PACKAGE_DISTRIBUTION_NAME),
    ):
        adapter = AsyncMlbDataAdapter()
        try:
            assert adapter._client.headers["User-Agent"] == "python-mlb-statsapi/unknown"
        finally:
            run_async(adapter.aclose())


def test_library_owned_client_preserves_httpx_default_headers():
    """Only User-Agent changes; HTTPX's other default headers are untouched.

    Mirrors test_mlb_session.test_library_created_session_preserves_requests_
    default_headers for the async client.
    """
    baseline = httpx.AsyncClient()
    adapter = AsyncMlbDataAdapter()
    try:
        for header, value in baseline.headers.items():
            if header.lower() == "user-agent":
                continue
            assert adapter._client.headers[header] == value

        for header in ("Accept", "Accept-Encoding", "Connection"):
            assert adapter._client.headers[header] == baseline.headers[header]

        assert adapter._client.headers["User-Agent"] != baseline.headers["User-Agent"]
    finally:
        run_async(adapter.aclose())
        run_async(baseline.aclose())


def test_injected_client_headers_are_unchanged():
    """Headers on a caller-supplied client survive adapter construction."""
    async def scenario():
        client = httpx.AsyncClient(
            headers={
                "User-Agent": "my-baseball-project/1.0",
                "X-Application": "scoreboard",
            },
        )
        headers_before = dict(client.headers)
        try:
            adapter = AsyncMlbDataAdapter(client=client)

            assert adapter._client is client
            assert dict(client.headers) == headers_before
            assert client.headers["User-Agent"] == "my-baseball-project/1.0"
            assert client.headers["X-Application"] == "scoreboard"
        finally:
            await client.aclose()

    run_async(scenario())
