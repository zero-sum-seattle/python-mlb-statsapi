from importlib.metadata import PackageNotFoundError, version as package_version
from typing import Dict

from .exceptions import (
    MlbDecodeError,
    MlbTimeoutError,
    MlbTransportError,
)
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ._http import (
    _build_http_error,
    _warn_http_compatibility,
)

# Connect timeout, then read timeout. Callers may override with a scalar or tuple.
DEFAULT_TIMEOUT = (3.05, 30.0)
TimeoutType = int | float | tuple[float, float]

# Distribution name published on PyPI; the User-Agent version is read from its
# installed metadata so no release version is duplicated in source.
PACKAGE_DISTRIBUTION_NAME = "python-mlb-statsapi"
UNKNOWN_PACKAGE_VERSION = "unknown"


def create_retry_policy() -> Retry:
    """Create a new instance of the default MLB HTTP retry policy."""
    return Retry(
        total=3,
        connect=3,
        read=2,
        status=3,
        backoff_factor=0.5,
        status_forcelist=(
            429,
            500,
            502,
            503,
            504,
        ),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
        raise_on_status=False,
    )


def _configure_retry_adapters(
    session: requests.Session,
) -> None:
    """Mount default retry adapters on a library-created Session.

    Caller-injected Sessions must not be passed here; their adapters stay
    under the caller's control.
    """
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=create_retry_policy(),
        ),
    )
    session.mount(
        "http://",
        HTTPAdapter(
            max_retries=create_retry_policy(),
        ),
    )


def _build_user_agent() -> str:
    """Build the package User-Agent from installed distribution metadata.

    Falls back to an "unknown" version for source-only environments where the
    distribution metadata is not installed. This must never raise, because it
    runs while a library-created Session is being constructed.
    """
    try:
        installed_version = package_version(PACKAGE_DISTRIBUTION_NAME)
    except PackageNotFoundError:
        installed_version = UNKNOWN_PACKAGE_VERSION
    return f"{PACKAGE_DISTRIBUTION_NAME}/{installed_version}"


def _configure_library_session(
    session: requests.Session,
) -> None:
    """Apply library defaults to a Session the library created and owns.

    Caller-injected Sessions must not be passed here; their headers and
    adapters stay under the caller's control.
    """
    # Only the User-Agent is replaced so the remaining Requests default
    # headers (Accept-Encoding, Accept, Connection) are preserved.
    session.headers["User-Agent"] = _build_user_agent()
    _configure_retry_adapters(session)


class MlbResult:
    """
    A class that holds data, status_code, and message returned from statsapi.mlb.com

    Attributes
    ----------
    status_code : int
        HTTP Return Code
    message : str
        Message returned from REST Endpoint
    data : dict
        JSON Data received from request
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        data: Dict | None = None,
    ):
        self.status_code = int(status_code)
        self.message = str(message)

        # Copy so caller-owned dictionaries are not mutated when copyright is removed.
        self.data = dict(data) if data is not None else {}
        self.data.pop("copyright", None)


class MlbDataAdapter:
    """
    Adapter for calling the mlb statsapi endpoint

    Attributes
    ----------
    hostname : str
        rest endpoint for data
    ver : str
        api version
    logger : logging.Logger
        instance of logger class
    """

    def __init__(
        self,
        hostname: str = 'statsapi.mlb.com',
        ver: str = 'v1',
        logger: logging.Logger | None = None,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
        session: requests.Session | None = None,
        *,
        strict_http: bool = True,
    ):
        # strict_http defaults to True in version 1.0; pass False for the
        # historical empty-result compatibility path on final non-404 4xx.
        self.url = f'https://{hostname}/api/{ver}/'
        self._logger = logger or logging.getLogger(__name__)
        self._timeout = timeout
        self._strict_http = strict_http
        self._owns_session = session is None
        if session is None:
            self._session = requests.Session()
            _configure_library_session(self._session)
        else:
            self._session = session
        self._closed = False

    def get(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> MlbResult:
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
        logline_post = " ,".join((logline_pre, 'success={}, status_code={}, message={}, url={}'))

        try:
            self._logger.debug(logline_post)
            response = self._session.get(
                url=full_url,
                params=ep_params,
                timeout=self._timeout,
            )

        except requests.exceptions.Timeout as exc:
            self._logger.error(msg=(str(exc)))
            raise MlbTimeoutError("Request failed") from exc
        except requests.exceptions.RequestException as exc:
            self._logger.error(msg=(str(exc)))
            raise MlbTransportError("Request failed") from exc

        status_code = response.status_code

        if 400 <= status_code <= 499:
            self._logger.error(msg=logline_post.format(
                'Invalid Request',
                status_code,
                response.reason,
                response.url,
            ))
            # Strict mode raises for final non-404 4xx after retries are exhausted.
            # 404 stays an empty MlbResult so endpoints keep None / [] / {} behavior.
            if self._strict_http and status_code != 404:
                raise _build_http_error(
                    response,
                    status_code=response.status_code,
                    reason=response.reason,
                    url=response.url or full_url,
                    method="GET",
                )
            if status_code != 404:
                _warn_http_compatibility(
                    status_code=status_code,
                    url=response.url or full_url,
                )
            return MlbResult(
                status_code=status_code,
                message=response.reason,
                data={},
            )

        if 500 <= status_code <= 599:
            self._logger.error(msg=logline_post.format(
                'Internal error occurred',
                status_code,
                response.reason,
                response.url,
            ))
            raise _build_http_error(
                response,
                status_code=response.status_code,
                reason=response.reason,
                url=response.url or full_url,
                method="GET",
            )

        if not 200 <= status_code <= 299:
            raise _build_http_error(
                response,
                status_code=response.status_code,
                reason=response.reason,
                url=response.url or full_url,
                method="GET",
            )

        self._logger.debug(msg=logline_post.format(
            'success',
            status_code,
            response.reason,
            response.url,
        ))

        if not response.content:
            response_data = {}
        else:
            try:
                response_data = response.json()
            except (ValueError, requests.JSONDecodeError) as exc:
                self._logger.error(msg=(str(exc)))
                raise MlbDecodeError(
                    "Bad JSON in response"
                ) from exc

        return MlbResult(
            status_code,
            message=response.reason,
            data=response_data,
        )

    def close(self) -> None:
        """Close the HTTP session when this adapter owns it.

        Safe to call more than once. Caller-injected sessions are left alone.
        """
        if self._owns_session and not self._closed:
            self._session.close()
            self._closed = True
