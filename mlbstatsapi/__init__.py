"""python-mlb-statsapi public package root.

Supported package-root symbols for the 1.x series are documented in
``docs/public-api.md``.

``__all__`` is intentionally omitted in version 1.0. Adding it today would
change ``from mlbstatsapi import *`` by excluding submodule names that appear
in the package namespace as an import side effect. Those submodules are not
part of the supported public API; cleaning them up requires a separate
focused issue. See ``docs/public-api.md``.
"""

from .mlb_api import Mlb
from .mlb_dataadapter import MlbDataAdapter, MlbResult, create_retry_policy
from .exceptions import (
    MlbDecodeError,
    MlbHttpError,
    MlbTimeoutError,
    MlbTransportError,
    TheMlbStatsApiException,
)
from .warnings import MlbHttpCompatibilityWarning

from .mlb_module import (
    return_splits,
    get_stat_attributes
    )
