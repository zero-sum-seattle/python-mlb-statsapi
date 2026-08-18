"""Offline tests for the async optional-dependency boundary (issue #301).

HTTPX ships only with the ``python-mlb-statsapi[async]`` extra, so three things
have to hold at once:

* ``from mlbstatsapi import AsyncMlbDataAdapter`` works when the extra is
  installed
* ``import mlbstatsapi`` and the whole sync surface keep working when it is not
* reaching for async functionality without it produces actionable install
  guidance instead of a bare ``ModuleNotFoundError``

That guidance is reserved for a genuinely missing HTTPX: an installed but broken
HTTPX must keep reporting its own failure.

Optional-import behavior is easy to test misleadingly, because ``httpx`` and
``mlbstatsapi`` are already in ``sys.modules`` by the time this file runs. Every
"HTTPX is missing" case therefore runs in a child interpreter that blocks the
import at ``sys.meta_path`` before ``mlbstatsapi`` is imported at all, which
also means the developer environment never has to uninstall anything.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

import mlbstatsapi
from mlbstatsapi.async_mlb_dataadapter import AsyncMlbDataAdapter

from test_public_api import (
    OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS,
    SUPPORTED_PACKAGE_ROOT_SYMBOLS,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# The guidance callers must be able to act on. Asserted as a substring so the
# surrounding sentence can be reworded without breaking these tests.
ASYNC_EXTRA_REQUIREMENT = "python-mlb-statsapi[async]"

# Prepended to a child program to simulate a sync-only install. The finder
# rejects httpx before any path-based finder can satisfy it, so an installed
# HTTPX in this environment is invisible to the child.
BLOCK_HTTPX = """
import sys


class _HttpxBlocker:
    # Makes httpx look uninstalled, exactly as ModuleNotFoundError would.
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "httpx" or fullname.startswith("httpx."):
            raise ModuleNotFoundError(
                f"No module named {fullname!r}", name=fullname
            )
        return None


sys.meta_path.insert(0, _HttpxBlocker())
assert "httpx" not in sys.modules, "child started with httpx already imported"
assert "mlbstatsapi" not in sys.modules, "child started with mlbstatsapi imported"
"""

# Prepended to a child program to simulate an installed but broken HTTPX: the
# httpx import fails, yet httpx itself is present. The user's problem is a
# broken dependency tree, not a missing extra, so the boundary must not rewrite
# it into install guidance.
BREAK_HTTPX_DEPENDENCY = """
import sys


class _BrokenHttpxDependency:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "httpx":
            raise ModuleNotFoundError(
                "No module named 'httpcore'", name="httpcore"
            )
        return None


sys.meta_path.insert(0, _BrokenHttpxDependency())
assert "httpx" not in sys.modules, "child started with httpx already imported"
"""


def _run_child(
    body: str,
    *,
    block_httpx: bool = False,
    break_httpx: bool = False,
) -> str:
    """Run ``body`` in a fresh interpreter against this working tree.

    ``block_httpx`` makes HTTPX look uninstalled; ``break_httpx`` makes it look
    installed but unimportable. They describe different environments, so a test
    picks exactly one.
    """
    assert not (block_httpx and break_httpx), "pick one HTTPX environment"

    program = textwrap.dedent(body)
    if block_httpx:
        program = BLOCK_HTTPX + program
    elif break_httpx:
        program = BREAK_HTTPX_DEPENDENCY + program

    completed = subprocess.run(
        [sys.executable, "-c", program],
        cwd=PROJECT_ROOT,
        # Import the working tree rather than any installed copy of the package.
        env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        capture_output=True,
        text=True,
        timeout=120,
    )

    assert completed.returncode == 0, (
        "child interpreter failed\n"
        f"--- stdout ---\n{completed.stdout}\n"
        f"--- stderr ---\n{completed.stderr}"
    )
    return completed.stdout


# ---------------------------------------------------------------------------
# With HTTPX installed
# ---------------------------------------------------------------------------


def test_async_adapter_is_exported_from_the_package_root() -> None:
    from mlbstatsapi import AsyncMlbDataAdapter as exported

    assert exported is AsyncMlbDataAdapter
    assert mlbstatsapi.AsyncMlbDataAdapter is AsyncMlbDataAdapter
    assert exported.__module__ == "mlbstatsapi.async_mlb_dataadapter"


def test_async_adapter_is_discoverable_from_the_package_root() -> None:
    assert "AsyncMlbDataAdapter" in dir(mlbstatsapi)


def test_package_root_does_not_expose_httpx() -> None:
    """HTTPX stays an implementation detail of the async adapter."""
    assert not hasattr(mlbstatsapi, "httpx")


def test_unknown_package_root_attribute_still_raises_attribute_error() -> None:
    with pytest.raises(AttributeError):
        mlbstatsapi.NotARealPublicSymbol  # noqa: B018


def test_importing_the_package_does_not_import_httpx() -> None:
    """The boundary is lazy: a sync-only caller never pays for HTTPX."""
    _run_child(
        """
        import sys

        import mlbstatsapi
        from mlbstatsapi import Mlb, MlbDataAdapter

        imported = sorted(name for name in sys.modules if name.startswith("httpx"))
        assert not imported, imported
        assert "mlbstatsapi.async_mlb_dataadapter" not in sys.modules
        """,
        block_httpx=False,
    )


def test_async_access_imports_httpx_on_demand() -> None:
    _run_child(
        """
        import sys

        import mlbstatsapi

        assert "httpx" not in sys.modules
        adapter_class = mlbstatsapi.AsyncMlbDataAdapter
        assert "httpx" in sys.modules
        assert adapter_class.__module__ == "mlbstatsapi.async_mlb_dataadapter"

        # Resolved once, then cached as an ordinary module attribute.
        assert mlbstatsapi.AsyncMlbDataAdapter is adapter_class
        """,
        block_httpx=False,
    )


# ---------------------------------------------------------------------------
# Without HTTPX installed
# ---------------------------------------------------------------------------


def test_sync_only_install_can_import_the_package() -> None:
    _run_child(
        """
        import sys

        import mlbstatsapi
        from mlbstatsapi import Mlb
        from mlbstatsapi import MlbDataAdapter

        assert "httpx" not in sys.modules
        """,
        block_httpx=True,
    )


def test_sync_only_install_keeps_every_supported_package_root_symbol() -> None:
    """Every always-available public symbol must resolve without the extra.

    ``SUPPORTED_PACKAGE_ROOT_SYMBOLS`` is the always-available half of the 1.x
    package-root API. The async half is covered separately below; both halves
    are public API.
    """
    _run_child(
        f"""
        import mlbstatsapi

        for name in {list(SUPPORTED_PACKAGE_ROOT_SYMBOLS)!r}:
            assert getattr(mlbstatsapi, name) is not None, name
        """,
        block_httpx=True,
    )


def test_sync_only_install_reports_the_extra_for_every_async_symbol() -> None:
    """The optional async manifest is exactly what the extra unlocks."""
    _run_child(
        f"""
        import mlbstatsapi

        for name in {list(OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS)!r}:
            try:
                getattr(mlbstatsapi, name)
            except ImportError as exc:
                assert "python-mlb-statsapi[async]" in str(exc), str(exc)
            else:
                raise AssertionError(f"expected an ImportError for {{name}}")
        """,
        block_httpx=True,
    )


def test_sync_only_install_can_still_use_the_sync_adapter() -> None:
    """The boundary changes no sync behavior, including Session ownership."""
    _run_child(
        """
        import sys

        from mlbstatsapi import Mlb, MlbDataAdapter, MlbResult

        adapter = MlbDataAdapter()
        try:
            assert adapter.url == "https://statsapi.mlb.com/api/v1/"
            assert adapter._owns_session is True
            assert "python-mlb-statsapi/" in adapter._session.headers["User-Agent"]
        finally:
            adapter.close()
        assert adapter._closed is True

        with Mlb() as mlb:
            assert mlb._owns_session is True

        result = MlbResult(404, "Not Found")
        assert result.data == {}

        assert "httpx" not in sys.modules
        """,
        block_httpx=True,
    )


def test_missing_httpx_reports_the_async_extra_from_the_package_root() -> None:
    stdout = _run_child(
        """
        import mlbstatsapi

        try:
            from mlbstatsapi import AsyncMlbDataAdapter
        except ImportError as exc:
            message = str(exc)
            cause = exc.__cause__
        else:
            raise AssertionError("expected an ImportError without httpx")

        assert "python-mlb-statsapi[async]" in message, message
        assert "pip install" in message, message
        # The real failure stays diagnosable behind the friendly message.
        assert isinstance(cause, ModuleNotFoundError), cause
        assert cause.name == "httpx", cause.name

        print(message)
        """,
        block_httpx=True,
    )

    assert ASYNC_EXTRA_REQUIREMENT in stdout


def test_missing_httpx_reports_the_async_extra_from_attribute_access() -> None:
    _run_child(
        """
        import mlbstatsapi

        try:
            mlbstatsapi.AsyncMlbDataAdapter
        except ImportError as exc:
            message = str(exc)
        else:
            raise AssertionError("expected an ImportError without httpx")

        assert "python-mlb-statsapi[async]" in message, message
        """,
        block_httpx=True,
    )


def test_missing_httpx_reports_the_async_extra_from_the_async_module() -> None:
    """Importing the module directly hits the same boundary, not a raw httpx error."""
    _run_child(
        """
        try:
            import mlbstatsapi.async_mlb_dataadapter  # noqa: F401
        except ImportError as exc:
            message = str(exc)
        else:
            raise AssertionError("expected an ImportError without httpx")

        assert "python-mlb-statsapi[async]" in message, message
        assert "pip install" in message, message
        """,
        block_httpx=True,
    )


def test_async_name_stays_discoverable_without_httpx() -> None:
    """Discoverability must not require the optional dependency."""
    _run_child(
        f"""
        import sys

        import mlbstatsapi

        for name in {list(OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS)!r}:
            assert name in dir(mlbstatsapi), name
        assert "httpx" not in sys.modules
        """,
        block_httpx=True,
    )


def test_failed_async_access_leaves_the_sync_api_usable() -> None:
    _run_child(
        """
        import mlbstatsapi

        for _ in range(2):
            try:
                mlbstatsapi.AsyncMlbDataAdapter
            except ImportError as exc:
                assert "python-mlb-statsapi[async]" in str(exc), str(exc)
            else:
                raise AssertionError("expected an ImportError without httpx")

        adapter = mlbstatsapi.MlbDataAdapter()
        try:
            assert adapter.url == "https://statsapi.mlb.com/api/v1/"
        finally:
            adapter.close()
        """,
        block_httpx=True,
    )


# ---------------------------------------------------------------------------
# With HTTPX installed but broken
# ---------------------------------------------------------------------------


def test_broken_httpx_install_is_not_reported_as_a_missing_extra() -> None:
    """Installing the extra would not fix a broken HTTPX, so do not suggest it."""
    _run_child(
        """
        try:
            import mlbstatsapi.async_mlb_dataadapter  # noqa: F401
        except ModuleNotFoundError as exc:
            assert exc.name == "httpcore", exc.name
            assert "python-mlb-statsapi[async]" not in str(exc), str(exc)
        else:
            raise AssertionError("expected the underlying import failure")
        """,
        break_httpx=True,
    )


def test_broken_httpx_install_surfaces_from_the_package_root_too() -> None:
    _run_child(
        """
        import mlbstatsapi

        try:
            mlbstatsapi.AsyncMlbDataAdapter
        except ModuleNotFoundError as exc:
            assert exc.name == "httpcore", exc.name
            assert "python-mlb-statsapi[async]" not in str(exc), str(exc)
        else:
            raise AssertionError("expected the underlying import failure")
        """,
        break_httpx=True,
    )
