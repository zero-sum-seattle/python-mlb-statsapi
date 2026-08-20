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

# Async symbols are resolved lazily. HTTPX is an optional dependency installed
# with the ``async`` extra, so importing the async adapter eagerly here would
# make ``import mlbstatsapi`` fail for every sync-only install. Resolving on
# first access keeps async functionality discoverable from the package root
# while the missing-dependency error surfaces only when async is actually
# requested. See docs/public-api.md.
_LAZY_ASYNC_EXPORTS = (
    "AsyncMlb",
    "AsyncMlbDataAdapter",
)


def __getattr__(name: str):
    if name == "AsyncMlb":
        from .async_mlb import AsyncMlb

        globals()["AsyncMlb"] = AsyncMlb
        return AsyncMlb

    if name == "AsyncMlbDataAdapter":
        from .async_mlb_dataadapter import AsyncMlbDataAdapter

        globals()["AsyncMlbDataAdapter"] = AsyncMlbDataAdapter
        return AsyncMlbDataAdapter

    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY_ASYNC_EXPORTS))
    )
