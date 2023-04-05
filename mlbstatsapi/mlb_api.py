import logging
import datetime

from typing import List, Union

from .mlb_dataadapter import MlbDataAdapter



class Mlb:
    """
    A class used to retrive MLB Stats API objects

    ...

    Attributes
    ----------
    hostname: str
        hostname of statsapi.mlb.com
    logger: logging.Loger
        logger
    """
    def __init__(self, hostname: str = 'statsapi.mlb.com', logger: logging.Logger = None):
        self._mlb_adapter_v1 = MlbDataAdapter(hostname, 'v1', logger)
        self._mlb_adapter_v1_1 = MlbDataAdapter(hostname, 'v1.1', logger)
        self._logger = logger or logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
