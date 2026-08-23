import asyncio
import logging

from typing import Dict

from ._async_support import import_httpx
from .exceptions import (
    MlbDecodeError,
    MlbTimeoutError,
    MlbTransportError,
)
from .mlb_dataadapter import (
    DEFAULT_TIMEOUT,
    MlbResult,
    TimeoutType,
    _build_user_agent,
    create_retry_policy,
)

from ._http import (
    _build_http_error,
    _warn_http_compatibility,
)

# HTTPX is optional; it ships with the ``async`` extra. Importing it through
# the shared boundary means a sync-only install that reaches for async
# functionality gets install guidance instead of a bare ModuleNotFoundError
# naming a library it never asked for. Binding the module here keeps every
# ``httpx.`` reference below unchanged.
httpx = import_httpx()


class AsyncMlbDataAdapter:
    """Async data adapter for MLB API."""


    def __init__(
        self,
        hostname: str = "statsapi.mlb.com",
        ver: str = "v1",
        logger: logging.Logger | None = None,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
        client: httpx.AsyncClient | None = None,
        *,
        strict_http: bool = True,
    ):
        self.url = f"https://{hostname}/api/{ver}/"
        self._logger = logger or logging.getLogger(__name__)
        self._timeout = timeout
        self._strict_http = strict_http
        self._owns_client = client is None
        # Retry eligibility follows client ownership by default, like the
        # sync adapter (retries are mounted on the Session, not per
        # MlbDataAdapter version). This is not a constructor knob: a caller
        # that owns this adapter's transport (AsyncMlb, for its v1.1 adapter
        # sharing v1's client) may call _set_retries_enabled() after
        # construction, since it — not this adapter — is the one that knows
        # whether the shared client is actually library-owned.
        self._retries_enabled = self._owns_client
        self._retry_policy = create_retry_policy()

        if client is None:
            # Only a library-owned client gets the package User-Agent. Passing
            # it to the constructor replaces just that header, so httpx's other
            # default headers (Accept, Accept-Encoding, Connection) survive.
            self._client = httpx.AsyncClient(
                headers={"User-Agent": _build_user_agent()},
            )
        else:
            # An injected client stays exactly as the caller configured it.
            self._client = client

        self._closed = False

    async def get(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> MlbResult:
        """Get data from the MLB API."""
        """
        return a MlbResult from endpoint

        Parameters
        ----------
        endpoint : str
            rest api endpoint
        ep_params : dict
            params
        data : dict
            data to send with requests (we aren't using this)

        Returns
        -------
        MlbResult
        """

        full_url = self.url + endpoint
        logline_pre = f'url={full_url}'
        logline_post = " ,".join(
            (
                logline_pre,
                'success={}, status_code={}, message={}, url={}'
            )
        )

        self._logger.debug(logline_post)
        response = await self._request_with_retries(full_url, ep_params)

        status_code = response.status_code

        if 400 <= status_code <= 499:
            self._logger.error(msg=logline_post.format(
                'Invalid Request',
                status_code,
                response.reason_phrase,
                str(response.url),
            ))
            # Strict mode raises for final non-404 4xx after retries are exhausted.
            # 404 stays an empty MlbResult so endpoints keep None / [] / {} behavior.
            if self._strict_http and status_code != 404:
                raise _build_http_error(
                    response,
                    status_code=response.status_code,
                    reason=response.reason_phrase,
                    url=str(response.url) if response.url else full_url,
                    method="GET",
                )
            if status_code != 404:
                _warn_http_compatibility(
                    status_code=status_code,
                    url=str(response.url) if response.url else full_url,
                )
            return MlbResult(
                status_code=status_code,
                message=response.reason_phrase,
                data={},
            )

        if 500 <= status_code <= 599:
            self._logger.error(msg=logline_post.format(
                'Internal error occurred',
                status_code,
                response.reason_phrase,
                str(response.url),
            ))
            raise _build_http_error(
                response,
                status_code=response.status_code,
                reason=response.reason_phrase,
                url=str(response.url) if response.url else full_url,
                method="GET",
            )

        if not 200 <= status_code <= 299:
            raise _build_http_error(
                response,
                status_code=response.status_code,
                reason=response.reason_phrase,
                url=str(response.url) if response.url else full_url,
                method="GET",
            )

        self._logger.debug(msg=logline_post.format(
            'success',
            status_code,
            response.reason_phrase,
            str(response.url),
        ))

        if not response.content:
            response_data = {}
        else:
            try:
                response_data = response.json()
            except ValueError as exc:
                self._logger.error(msg=(str(exc)))
                raise MlbDecodeError(
                    "Bad JSON in response"
                ) from exc

        return MlbResult(
            status_code,
            message=response.reason_phrase,
            data=response_data,
        )

    async def _request_with_retries(
        self,
        full_url: str,
        ep_params: Dict,
    ) -> httpx.Response:
        """Issue the GET call, retrying with bounded backoff when this
        adapter owns its httpx.AsyncClient.

        An injected client is called exactly once; its retry behavior stays
        under caller control, matching the sync adapter's session-ownership
        rule.

        Failures spend the retry budget the sync policy would spend, and
        surface the public exception the sync adapter raises:

            ReadTimeout             -> read budget    -> MlbTimeoutError
            ConnectTimeout          -> connect budget -> MlbTimeoutError
            ConnectError            -> connect budget -> MlbTransportError
            other TimeoutException  -> total budget   -> MlbTimeoutError
            other RequestError      -> total budget   -> MlbTransportError
            retryable HTTP status   -> status budget
        """
        policy = self._retry_policy

        attempt = 0
        while True:
            attempt += 1
            try:
                response = await self._client.get(
                    url=full_url,
                    params=ep_params,
                    timeout=self._translate_timeout(self._timeout),
                )

            except httpx.ReadTimeout as exc:
                max_attempts = policy.read + 1 if self._retries_enabled else 1

                if attempt >= max_attempts:
                    self._logger.error(msg=str(exc))
                    raise MlbTimeoutError("Request failed") from exc

                await self._sleep_before_retry(attempt=attempt, response=None)
                continue

            except httpx.ConnectTimeout as exc:
                # Caught before httpx.TimeoutException: a connect timeout is a
                # timeout for the caller, but it spends the connect budget so
                # the retry accounting matches the sync policy.
                max_attempts = policy.connect + 1 if self._retries_enabled else 1

                if attempt >= max_attempts:
                    self._logger.error(msg=str(exc))
                    raise MlbTimeoutError("Request failed") from exc

                await self._sleep_before_retry(attempt=attempt, response=None)
                continue

            except httpx.ConnectError as exc:
                max_attempts = policy.connect + 1 if self._retries_enabled else 1

                if attempt >= max_attempts:
                    self._logger.error(msg=str(exc))
                    raise MlbTransportError("Request failed") from exc

                await self._sleep_before_retry(
                    attempt=attempt,
                    response=None,
                )
                continue

            except httpx.TimeoutException as exc:
                max_attempts = policy.total + 1 if self._retries_enabled else 1

                if attempt >= max_attempts:
                    raise MlbTimeoutError("Request failed") from exc

                await self._sleep_before_retry(
                    attempt=attempt,
                    response=None,
                )
                continue

            except httpx.RequestError as exc:
                max_attempts = policy.total + 1 if self._retries_enabled else 1

                if attempt >= max_attempts:
                    self._logger.error(msg=str(exc))
                    raise MlbTransportError("Request failed") from exc

                await self._sleep_before_retry(attempt=attempt, response=None)
                continue

            max_attempts = policy.status + 1 if self._retries_enabled else 1

            if response.status_code not in policy.status_forcelist or attempt >= max_attempts:
                return response

            await self._sleep_before_retry(attempt=attempt, response=response)

    async def _sleep_before_retry(
        self,
        *,
        attempt: int,
        response: httpx.Response | None,
    ) -> None:
        policy = self._retry_policy

        if policy.respect_retry_after_header and response is not None:
            retry_after = policy.get_retry_after(response)
            if retry_after:
                await asyncio.sleep(retry_after)
                return

        # Mirrors urllib3's Retry.get_backoff_time(): no delay before the
        # first retry, exponential thereafter, capped at backoff_max.
        delay = 0.0 if attempt <= 1 else min(
            policy.backoff_factor * (2 ** (attempt - 1)),
            policy.backoff_max,
        )

        if delay > 0:
            await asyncio.sleep(delay)

    @staticmethod
    def _translate_timeout(timeout: TimeoutType) -> httpx.Timeout:
        if isinstance(timeout, tuple):
            connect_timeout, read_timeout = timeout

            return httpx.Timeout(
                connect=connect_timeout,
                read=read_timeout,
                write=read_timeout,
                pool=connect_timeout,
            )

        return httpx.Timeout(timeout)

    async def aclose(self) -> None:
        if self._owns_client and not self._closed:
            await self._client.aclose()
            self._closed = True

    def _set_retries_enabled(self, enabled: bool) -> None:
        """Override retry eligibility for a borrowed, non-owned client.

        Internal coordination hook, not public API: only a caller that
        actually owns this adapter's transport (AsyncMlb, wiring up its v1.1
        adapter to share the v1 adapter's client) should call this. Standalone
        use never needs it; retry eligibility already follows client
        ownership by default.
        """
        self._retries_enabled = enabled
