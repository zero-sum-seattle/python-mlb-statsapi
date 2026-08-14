import logging

import httpx

from typing import Dict

from .exceptions import (
    MlbDecodeError,
    MlbTimeoutError,
    MlbTransportError,
)
from .mlb_dataadapter import (
    DEFAULT_TIMEOUT,
    MlbResult,
    TimeoutType,
)

from ._http import (
    _build_http_error,
    _warn_http_compatibility,
)


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

        if client is None:
            self._client = httpx.AsyncClient()
        else:
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

        try:
            self._logger.debug(logline_post)

            response = await self._client.get(
                url=full_url,
                params=ep_params,
                timeout=self._translate_timeout(self._timeout),
            )

        except httpx.TimeoutException as exc:
            self._logger.error(msg=str(exc))
            raise MlbTimeoutError("Request failed") from exc

        except httpx.RequestError as exc:
            self._logger.error(msg=str(exc))
            raise MlbTransportError("Request failed") from exc  

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