from typing import Dict
from urllib import response
from .exceptions import TheMlbStatsApiException
import requests
import logging

class MlbResult:
    def __init__(self, status_code: int, message: str, data: Dict = {}):
        self.status_code = int(status_code)
        self.message = str(message)

        # if data is not NoneType and if copyright key is in data
        # then if copyright key revemoved set data
        self.data = data
        if 'copyright' in data:
            del data['copyright']


class MlbDataAdapter:
    """Adapter for calling the mlb statsapi endpoint"""

    def __init__(self, hostname: str = 'statsapi.mlb.com', ver: str = 'v1', logger: logging.Logger = None):
        self.url = f"https://{hostname}/api/{ver}/" # we'll figure out the v1.1 endpoint later
        self._logger = logger or logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

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
        MlbResult or None
        """     
        full_url = self.url + endpoint # pass endpoint from inhertited classes
        logline_pre = f"url={full_url}"
        logline_post = f" ,".join((logline_pre, "success={}, status_code={}, message={}"))

        try:
            self._logger.debug(logline_post)
            response = requests.get(url=full_url, params=ep_params) # mlbstats API only uses get calls

        except requests.exceptions.RequestException as e: # catch a response error
            self._logger.error(msg=(str(e))) # log error
            raise TheMlbStatsApiException("Request failed") from e

        try:
            data = response.json()

        except (ValueError, requests.JSONDecodeError) as e: # catch a JSON error
            self._logger.error(msg=(str(e))) # log error JSON
            raise TheMlbStatsApiException("Bad JSON in response") from e

        if response.status_code <= 200 and response.status_code <= 299: # catch HTTP errors
            self._logger.debug(msg=logline_post.format("success", response.status_code, response.reason)) # log success
            data = _transform_keys_in_response()
            return MlbResult(response.status_code, message=response.reason, data=data) # return result

        elif response.status_code >= 400 and response.status_code <= 499:  # catch HTTP error
            self._logger.error(msg=logline_post.format("Invalid Request", response.status_code, response.reason)) # log failure
            return MlbResult(response.status_code, message=response.reason, data={})

        elif response.status_code >= 500 and response.status_code <= 599:
            self._logger.error(msg=logline_post.format("Internal error occurred", response.status_code, response.reason))
            raise TheMlbStatsApiException(f"{response.status_code}: {response.reason}") # raise exception 

        else:
            raise TheMlbStatsApiException(f"{response.status_code}: {response.reason}") # raise exception 

