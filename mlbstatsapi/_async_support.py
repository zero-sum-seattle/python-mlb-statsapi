"""Private optional-dependency boundary for async support.

HTTPX ships only with the ``async`` extra, so a sync-only install must be able
to ``import mlbstatsapi`` and use ``Mlb`` / ``MlbDataAdapter`` without it. Every
async entry point routes its HTTPX import through :func:`import_httpx`, so a
missing optional dependency produces one actionable install message instead of a
bare ``ModuleNotFoundError`` naming a library the user never asked for. Import
failures that are not a missing ``httpx`` are left alone.

HTTPX itself stays an implementation detail: nothing here re-exports it.
"""

from types import ModuleType

ASYNC_EXTRA_REQUIREMENT = 'python-mlb-statsapi[async]'

MISSING_HTTPX_MESSAGE = (
    "Async support requires the optional HTTPX dependency, which is not "
    "installed. Install it with:\n\n"
    f'    pip install "{ASYNC_EXTRA_REQUIREMENT}"\n'
)


def import_httpx() -> ModuleType:
    """Return the ``httpx`` module, or raise an actionable ``ImportError``.

    Only a genuinely missing top-level ``httpx`` is translated into the install
    message. An installed-but-broken HTTPX fails on some other module (a
    missing transitive dependency, for example), and telling that user to
    install the extra would send them chasing the wrong problem, so those
    failures propagate unchanged.

    The original failure is preserved as the exception cause so a broken async
    install stays diagnosable.
    """
    try:
        import httpx
    except ModuleNotFoundError as exc:
        if exc.name != "httpx":
            raise
        raise ImportError(MISSING_HTTPX_MESSAGE) from exc

    return httpx
