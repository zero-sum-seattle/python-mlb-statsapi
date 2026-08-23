"""Retry-aware HTTPX transport for the async client.

The synchronous side does not implement retries. It *configures* them: ``Mlb``
mounts an ``HTTPAdapter`` carrying the library ``Retry`` policy onto the
Session it creates, and from that point on every ``session.get()`` retries
without any caller — ``MlbDataAdapter`` included — knowing retries exist.

HTTPX has the same seam. ``AsyncClient(transport=...)`` accepts any
``AsyncBaseTransport``, which is the position ``HTTPAdapter`` occupies in
Requests. Putting the retry loop there instead of inside
``AsyncMlbDataAdapter`` gives the async side the sync structure:

* Adapters call ``client.get()`` and are unaware of retries.
* The retry policy travels with the client, so two adapters sharing one client
  share one policy by construction. Neither adapter holds retry state, so
  neither can disagree with the other about it.
* A caller-injected client keeps whatever transport its caller mounted, so
  "the library does not touch an injected client" needs no flag to enforce.

A caller who wants library retry behavior on a client they own mounts this
transport themselves, mirroring the documented sync recipe for
``create_retry_policy()``.
"""

import asyncio

from ._async_support import import_httpx
from .mlb_dataadapter import _build_user_agent, create_retry_policy

httpx = import_httpx()


class MlbAsyncRetryTransport(httpx.AsyncBaseTransport):
    """Wrap an HTTPX transport with the library's bounded retry policy.

    Failures spend the same retry budget the sync policy spends:

        ReadTimeout             -> read budget
        ConnectTimeout          -> connect budget
        ConnectError            -> connect budget
        other TimeoutException  -> total budget
        other RequestError      -> total budget
        retryable HTTP status   -> status budget

    Exhausting a budget re-raises the underlying HTTPX exception. Translating
    those into the library's public exception types stays with the adapter, so
    this class satisfies the transport contract HTTPX documents: transports
    raise HTTPX errors.
    """

    def __init__(
        self,
        inner: httpx.AsyncBaseTransport | None = None,
        *,
        retry_policy=None,
    ):
        self._inner = inner if inner is not None else httpx.AsyncHTTPTransport()
        self._retry_policy = (
            retry_policy if retry_policy is not None else create_retry_policy()
        )

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        policy = self._retry_policy

        attempt = 0
        while True:
            attempt += 1
            try:
                response = await self._inner.handle_async_request(request)

            except httpx.ReadTimeout:
                if attempt > policy.read:
                    raise
                await self._backoff(attempt=attempt, response=None)
                continue

            except httpx.ConnectTimeout:
                # Caught before httpx.TimeoutException: a connect timeout is a
                # timeout for the caller, but it spends the connect budget so
                # the retry accounting matches the sync policy.
                if attempt > policy.connect:
                    raise
                await self._backoff(attempt=attempt, response=None)
                continue

            except httpx.ConnectError:
                if attempt > policy.connect:
                    raise
                await self._backoff(attempt=attempt, response=None)
                continue

            except httpx.TimeoutException:
                if attempt > policy.total:
                    raise
                await self._backoff(attempt=attempt, response=None)
                continue

            except httpx.RequestError:
                if attempt > policy.total:
                    raise
                await self._backoff(attempt=attempt, response=None)
                continue

            if (
                response.status_code not in policy.status_forcelist
                or attempt > policy.status
            ):
                return response

            # The response is discarded, so release it before another attempt
            # rather than leaving a connection checked out of the pool.
            delay = self._delay_for(attempt=attempt, response=response)
            await response.aclose()
            if delay > 0:
                await asyncio.sleep(delay)

    async def _backoff(
        self,
        *,
        attempt: int,
        response: httpx.Response | None,
    ) -> None:
        delay = self._delay_for(attempt=attempt, response=response)
        if delay > 0:
            await asyncio.sleep(delay)

    def _delay_for(
        self,
        *,
        attempt: int,
        response: httpx.Response | None,
    ) -> float:
        policy = self._retry_policy

        if policy.respect_retry_after_header and response is not None:
            retry_after = policy.get_retry_after(response)
            if retry_after:
                return retry_after

        # Mirrors urllib3's Retry.get_backoff_time(): no delay before the
        # first retry, exponential thereafter, capped at backoff_max.
        if attempt <= 1:
            return 0.0

        return min(
            policy.backoff_factor * (2 ** (attempt - 1)),
            policy.backoff_max,
        )

    async def aclose(self) -> None:
        await self._inner.aclose()


def create_library_async_client() -> httpx.AsyncClient:
    """Build the async client the library creates and owns.

    The counterpart of ``_configure_library_session()`` on the sync side:
    library defaults are applied here, at creation, and only to clients the
    library creates. Passing headers to the constructor replaces just the
    User-Agent, so HTTPX's other default headers survive.
    """
    return httpx.AsyncClient(
        headers={"User-Agent": _build_user_agent()},
        transport=MlbAsyncRetryTransport(),
    )
