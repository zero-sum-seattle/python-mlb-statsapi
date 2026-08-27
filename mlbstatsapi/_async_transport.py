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
from ._env_proxies import environment_proxy_map
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

    HTTPX only builds its own environment-proxy mounts when the caller leaves
    ``transport=None`` (``allow_env_proxies = trust_env and transport is
    None`` in ``httpx.Client.__init__``). Passing ``transport=`` here, which
    is required to install the retry transport, would otherwise silently
    disable ``HTTP_PROXY`` / ``HTTPS_PROXY`` / ``ALL_PROXY`` / ``NO_PROXY``
    support for every library-created async client (issue #324). This
    rebuilds that discovery from the stdlib (see ``_env_proxies.py``) and
    passes it through HTTPX's public ``mounts=`` argument instead, wrapping
    every proxy transport in the same retry transport the direct path uses,
    so a request routed through a proxy still gets library retries.

    Environment discovery always runs here, matching the ``trust_env=True``
    default a caller gets from a plain ``httpx.AsyncClient()``. Neither
    ``AsyncMlb`` nor ``AsyncMlbDataAdapter`` exposes a ``trust_env`` toggle;
    a caller who needs one injects their own client instead, the same way
    they would opt into any other HTTPX-level setting this factory does not
    surface.

    One retry policy instance is shared by the direct transport and every
    proxy transport, mirroring the sync side sharing one Session across the
    v1 and v1.1 adapters: retries are a property of the client, not of any
    one transport within it.
    """
    retry_policy = create_retry_policy()
    direct = MlbAsyncRetryTransport(
        httpx.AsyncHTTPTransport(), retry_policy=retry_policy
    )

    mounts: dict[str, httpx.AsyncBaseTransport | None] = {}
    for pattern, proxy in environment_proxy_map().items():
        if proxy is None:
            # None tells HTTPX to fall back to client._transport for this
            # pattern (see AsyncClient._transport_for_url), i.e. bypass the
            # proxy rather than route through a second transport instance.
            # aclose() also skips a None mount, so this never gets closed
            # twice via both the direct transport and a mount entry.
            mounts[pattern] = None
        else:
            mounts[pattern] = MlbAsyncRetryTransport(
                httpx.AsyncHTTPTransport(proxy=proxy), retry_policy=retry_policy
            )

    return httpx.AsyncClient(
        headers={"User-Agent": _build_user_agent()},
        transport=direct,
        mounts=mounts,
    )
