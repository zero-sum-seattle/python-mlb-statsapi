from typing import Dict
from .exceptions import TheMlbStatsApiException
import requests
import logging


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

    def __init__(self, hostname: str = 'statsapi.mlb.com', ver: str = 'v1', logger: logging.Logger = None):
        self.url = f'https://{hostname}/api/{ver}/'
        self._logger = logger or logging.getLogger(__name__)

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
            response = requests.get(url=full_url, params=ep_params)

        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise TheMlbStatsApiException('Request failed') from e

        status_code = response.status_code

        if 400 <= status_code <= 499:
            self._logger.error(msg=logline_post.format(
                'Invalid Request',
                status_code,
                response.reason,
                response.url,
            ))
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
            raise TheMlbStatsApiException(
                f"{status_code}: {response.reason}"
            )

        if not 200 <= status_code <= 299:
            raise TheMlbStatsApiException(
                f"{status_code}: {response.reason}"
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
                raise TheMlbStatsApiException(
                    "Bad JSON in response"
                ) from exc

        return MlbResult(
            status_code,
            message=response.reason,
            data=response_data,
        )
