"""Validate the built python-mlb-statsapi distributions before a release.

Checks the artifacts in ``dist/``, then clean-installs each distribution
artifact into throwaway virtual environments and runs synchronous and async
public-API smoke tests against the *installed* package.

Both the wheel and the source distribution are installed separately so a
broken sdist build, a missing runtime dependency, or an omitted package file
cannot hide behind a working wheel.

The smoke test deliberately runs from a temporary directory so the repository
checkout cannot shadow the installed distribution artifact.

Nothing here contacts the MLB API. Every HTTP response exercised by the smoke
tests is produced by an injected fake Session or HTTPX MockTransport.

Usage::

    python scripts/validate_release.py
    python scripts/validate_release.py --expected-version 1.1.0
    python scripts/validate_release.py --dist dist

Without ``--expected-version`` the expected artifact version is read from the
version declared in ``pyproject.toml``, so the same validator follows the
project through a version bump without being edited.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tarfile
import tempfile
import venv
import zipfile
from email.parser import Parser
from pathlib import Path

DISTRIBUTION_NAME = "python-mlb-statsapi"
NORMALIZED_DISTRIBUTION_NAME = "python_mlb_statsapi"
EXPECTED_REQUIRES_PYTHON = ">=3.10"

WHEEL_LABEL = "wheel"
SDIST_LABEL = "source distribution"

# Paths every source distribution must carry so the project can be rebuilt,
# installed, and read from the sdist alone. Each entry was confirmed present in
# the archive Poetry actually generates; tests, docs, and scripts are
# intentionally excluded from the sdist and must not be listed here.
REQUIRED_SDIST_PATHS = (
    "PKG-INFO",
    "LICENSE",
    "README.md",
    "pyproject.toml",
    "mlbstatsapi/__init__.py",
    "mlbstatsapi/exceptions.py",
    "mlbstatsapi/warnings.py",
    "mlbstatsapi/_async_support.py",
    "mlbstatsapi/_async_transport.py",
    "mlbstatsapi/_env_proxies.py",
    "mlbstatsapi/_http.py",
    "mlbstatsapi/async_mlb.py",
    "mlbstatsapi/async_mlb_dataadapter.py",
    "mlbstatsapi/mlb_api.py",
    "mlbstatsapi/mlb_dataadapter.py",
    "mlbstatsapi/mlb_module.py",
    "mlbstatsapi/models/__init__.py",
)

# Explicit failure messages for the version 1.0 strict defaults. They are
# module-level constants so the offline validator tests can assert that the
# smoke-test contract still reports a reverted default in an understandable way.
MLB_STRICT_DEFAULT_MESSAGE = "Mlb.strict_http must default to True for the 1.0 contract"
ADAPTER_STRICT_DEFAULT_MESSAGE = (
    "MlbDataAdapter.strict_http must default to True for the 1.0 contract"
)
ASYNC_MLB_STRICT_DEFAULT_MESSAGE = (
    "AsyncMlb.strict_http must default to True for the 1.1 contract"
)
ASYNC_ADAPTER_STRICT_DEFAULT_MESSAGE = (
    "AsyncMlbDataAdapter.strict_http must default to True for the 1.1 contract"
)

SMOKE_TEST_SOURCE = '''
"""Public API smoke test for an installed python-mlb-statsapi artifact.

Runs inside a throwaway virtual environment against the installed
distribution, never against a repository checkout.

Every HTTP response comes from an injected fake Session, so this test performs
no network I/O and never reaches the MLB API.
"""

import importlib.metadata
import inspect
import json
import logging
import sys
import sysconfig
import warnings
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import mlbstatsapi
from mlbstatsapi import (
    Mlb,
    MlbDataAdapter,
    MlbDecodeError,
    MlbHttpCompatibilityWarning,
    MlbHttpError,
    MlbResult,
    MlbTimeoutError,
    MlbTransportError,
    TheMlbStatsApiException,
    create_retry_policy,
    get_stat_attributes,
    return_splits,
)

expected_version = sys.argv[1]

# The adapter logs an error for every fake 403, which is expected here. Silence
# it from the consumer side so the smoke-test output stays readable; the library
# itself must never configure logging for its callers.
package_logger = logging.getLogger("mlbstatsapi")
package_logger.addHandler(logging.NullHandler())
package_logger.propagate = False

MLB_STRICT_DEFAULT_MESSAGE = (
    "Mlb.strict_http must default to True for the 1.0 contract"
)
ADAPTER_STRICT_DEFAULT_MESSAGE = (
    "MlbDataAdapter.strict_http must default to True for the 1.0 contract"
)

# Small deterministic error payload; MlbHttpError must expose it unchanged.
FORBIDDEN_PAYLOAD = {"messageNumber": 403, "message": "Forbidden"}
V1_SPORTS_URL = "https://statsapi.mlb.com/api/v1/sports"
V1_1_SPORTS_URL = "https://statsapi.mlb.com/api/v1.1/sports"
DOCUMENTED_RETRY_STATUSES = {429, 500, 502, 503, 504}


# --- The installed artifact, not the repository checkout ---

assert sys.prefix != sys.base_prefix, (
    "the smoke test must run inside the throwaway virtual environment"
)

site_packages = Path(sysconfig.get_paths()["purelib"]).resolve()
package_file = Path(mlbstatsapi.__file__).resolve()
assert package_file.is_relative_to(site_packages), (
    f"mlbstatsapi was imported from {package_file}, not from the installed "
    f"distribution artifact under {site_packages}"
)

installed_version = importlib.metadata.version("python-mlb-statsapi")
assert installed_version == expected_version, (
    f"installed metadata reports {installed_version}, expected {expected_version}"
)


# --- Supported package-root surface ---

supported_symbols = (
    "Mlb",
    "MlbDataAdapter",
    "MlbDecodeError",
    "MlbHttpCompatibilityWarning",
    "MlbHttpError",
    "MlbResult",
    "MlbTimeoutError",
    "MlbTransportError",
    "TheMlbStatsApiException",
    "create_retry_policy",
    "get_stat_attributes",
    "return_splits",
)
for name in supported_symbols:
    assert hasattr(mlbstatsapi, name), f"mlbstatsapi.{name} is not importable"
    assert getattr(mlbstatsapi, name) is not None, f"mlbstatsapi.{name} is None"

# Version 1.0 intentionally omits __all__; adding it would narrow star imports.
assert getattr(mlbstatsapi, "__all__", None) is None, (
    "version 1.0 must not define mlbstatsapi.__all__"
)


def assert_documented_retry_policy(retry, *, label):
    """Assert the documented retry values without freezing Requests internals."""
    assert isinstance(retry, Retry), f"{label}: {type(retry)!r} is not a Retry"
    assert retry.total == 3, f"{label}: total={retry.total}"
    assert retry.connect == 3, f"{label}: connect={retry.connect}"
    assert retry.read == 2, f"{label}: read={retry.read}"
    assert retry.status == 3, f"{label}: status={retry.status}"
    assert retry.backoff_factor == 0.5, f"{label}: backoff_factor={retry.backoff_factor}"
    assert set(retry.status_forcelist) == DOCUMENTED_RETRY_STATUSES, (
        f"{label}: status_forcelist={sorted(retry.status_forcelist)}"
    )
    assert retry.allowed_methods == frozenset({"GET"}), (
        f"{label}: allowed_methods={retry.allowed_methods}"
    )
    assert retry.respect_retry_after_header is True, label
    assert retry.raise_on_status is False, label


assert callable(create_retry_policy)
assert inspect.signature(create_retry_policy).parameters == {}
retry_policy = create_retry_policy()
assert_documented_retry_policy(retry_policy, label="create_retry_policy()")
assert create_retry_policy() is not retry_policy, (
    "create_retry_policy() must return a new Retry instance per call"
)

assert issubclass(MlbHttpCompatibilityWarning, FutureWarning)
assert issubclass(TheMlbStatsApiException, Exception)
assert issubclass(MlbHttpError, TheMlbStatsApiException)
assert issubclass(MlbTimeoutError, MlbTransportError)
assert issubclass(MlbTransportError, TheMlbStatsApiException)
assert issubclass(MlbDecodeError, TheMlbStatsApiException)

mlb_init = inspect.signature(Mlb.__init__).parameters
adapter_init = inspect.signature(MlbDataAdapter.__init__).parameters
result_init = inspect.signature(MlbResult.__init__).parameters

assert list(mlb_init) == [
    "self",
    "hostname",
    "logger",
    "timeout",
    "session",
    "strict_http",
]
assert mlb_init["hostname"].default == "statsapi.mlb.com"
assert mlb_init["logger"].default is None
assert mlb_init["timeout"].default == (3.05, 30.0)
assert mlb_init["session"].default is None
assert mlb_init["strict_http"].default is True, MLB_STRICT_DEFAULT_MESSAGE
assert mlb_init["strict_http"].kind is inspect.Parameter.KEYWORD_ONLY

assert list(adapter_init) == [
    "self",
    "hostname",
    "ver",
    "logger",
    "timeout",
    "session",
    "strict_http",
]
assert adapter_init["hostname"].default == "statsapi.mlb.com"
assert adapter_init["ver"].default == "v1"
assert adapter_init["logger"].default is None
assert adapter_init["timeout"].default == (3.05, 30.0)
assert adapter_init["session"].default is None
assert adapter_init["strict_http"].default is True, ADAPTER_STRICT_DEFAULT_MESSAGE
assert adapter_init["strict_http"].kind is inspect.Parameter.KEYWORD_ONLY

assert list(result_init) == ["self", "status_code", "message", "data"]
assert result_init["data"].default is None

result = MlbResult(200, "OK", {"copyright": "x", "ok": True})
assert result.status_code == 200
assert result.message == "OK"
assert result.data == {"ok": True}

assert callable(return_splits)
assert callable(get_stat_attributes)
assert return_splits is mlbstatsapi.return_splits
assert get_stat_attributes is mlbstatsapi.get_stat_attributes


# --- Offline HTTP behavior ---


class ForbiddenSession:
    """Injected Session stand-in that answers every GET with a final 403.

    A realistic requests.Response is built for the requested URL so the
    installed adapter runs its real status handling. No network I/O happens,
    so the smoke test never reaches the MLB API.
    """

    def __init__(self):
        self.requested_urls = []

    def get(self, url, params=None, timeout=None, **kwargs):
        self.requested_urls.append(url)
        response = requests.Response()
        response.status_code = 403
        response.reason = "Forbidden"
        response.url = url
        response.headers["Content-Type"] = "application/json"
        response.encoding = "utf-8"
        # requests only exposes a body through Response._content; building it
        # directly is the way to produce a realistic offline Response.
        response._content = json.dumps(FORBIDDEN_PAYLOAD).encode("utf-8")
        return response

    def close(self):
        pass


def assert_forbidden_error(exc, *, expected_url, label):
    assert exc.status_code == 403, f"{label}: status_code={exc.status_code}"
    assert exc.reason == "Forbidden", f"{label}: reason={exc.reason!r}"
    assert exc.method == "GET", f"{label}: method={exc.method!r}"
    assert exc.url == expected_url, f"{label}: url={exc.url!r}"
    assert isinstance(exc.response_data, dict), (
        f"{label}: response_data={exc.response_data!r}"
    )
    for key, value in FORBIDDEN_PAYLOAD.items():
        assert exc.response_data.get(key) == value, (
            f"{label}: response_data={exc.response_data!r}"
        )


def assert_raises_forbidden(call, *, expected_url, label):
    try:
        call()
    except MlbHttpError as exc:
        assert_forbidden_error(exc, expected_url=expected_url, label=label)
        return
    raise AssertionError(f"{label}: a final 403 did not raise MlbHttpError")


def capture_compatibility_warnings(call):
    """Run *call* and return (result, captured MlbHttpCompatibilityWarnings)."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = call()
    compatibility = [
        record
        for record in caught
        if issubclass(record.category, MlbHttpCompatibilityWarning)
    ]
    return result, compatibility


def assert_single_compatibility_warning(captured, *, label):
    assert len(captured) == 1, (
        f"{label}: expected exactly one MlbHttpCompatibilityWarning, "
        f"captured {[str(record.message) for record in captured]}"
    )
    record = captured[0]
    assert record.category is MlbHttpCompatibilityWarning, (
        f"{label}: warning category is {record.category!r}"
    )
    assert "strict_http=False" in str(record.message), (
        f"{label}: warning message does not mention strict_http=False: "
        f"{str(record.message)!r}"
    )


# Constructed without strict_http so the real constructor default is exercised.
session = ForbiddenSession()
with Mlb(session=session) as mlb:
    assert_raises_forbidden(
        mlb.get_sports,
        expected_url=V1_SPORTS_URL,
        label=MLB_STRICT_DEFAULT_MESSAGE,
    )

session = ForbiddenSession()
with Mlb(session=session, strict_http=True) as mlb:
    assert_raises_forbidden(
        mlb.get_sports,
        expected_url=V1_SPORTS_URL,
        label="Mlb(strict_http=True).get_sports()",
    )

session = ForbiddenSession()
with Mlb(session=session, strict_http=False) as mlb:
    sports, captured = capture_compatibility_warnings(mlb.get_sports)

assert sports == [], f"Mlb(strict_http=False).get_sports() returned {sports!r}"
assert_single_compatibility_warning(
    captured,
    label="Mlb(strict_http=False).get_sports()",
)


# --- Direct adapter construction, both documented API versions ---

for api_version, sports_url in (("v1", V1_SPORTS_URL), ("v1.1", V1_1_SPORTS_URL)):
    # Omitting strict_http exercises the real adapter default.
    adapter = MlbDataAdapter(ver=api_version, session=ForbiddenSession())
    try:
        assert_raises_forbidden(
            lambda: adapter.get(endpoint="sports"),
            expected_url=sports_url,
            label=f"{ADAPTER_STRICT_DEFAULT_MESSAGE} (ver={api_version})",
        )
    finally:
        adapter.close()

    adapter = MlbDataAdapter(
        ver=api_version,
        session=ForbiddenSession(),
        strict_http=True,
    )
    try:
        assert_raises_forbidden(
            lambda: adapter.get(endpoint="sports"),
            expected_url=sports_url,
            label=f"MlbDataAdapter(ver={api_version}, strict_http=True).get()",
        )
    finally:
        adapter.close()

    adapter = MlbDataAdapter(
        ver=api_version,
        session=ForbiddenSession(),
        strict_http=False,
    )
    label = f"MlbDataAdapter(ver={api_version}, strict_http=False).get()"
    try:
        result, captured = capture_compatibility_warnings(
            lambda: adapter.get(endpoint="sports"),
        )
    finally:
        adapter.close()

    assert isinstance(result, MlbResult), f"{label}: {type(result)!r}"
    assert result.status_code == 403, f"{label}: status_code={result.status_code}"
    assert result.message == "Forbidden", f"{label}: message={result.message!r}"
    assert result.data == {}, f"{label}: data={result.data!r}"
    assert_single_compatibility_warning(captured, label=label)


# --- Library-created Session ---

# A library-created Session is library-owned, so reading its headers and
# adapters through private attributes is acceptable for release validation only.
expected_user_agent = f"python-mlb-statsapi/{expected_version}"
with Mlb() as mlb:
    user_agent = mlb._session.headers["User-Agent"]
    assert user_agent == expected_user_agent, (
        f"library-created Session sends User-Agent {user_agent!r}, "
        f"expected {expected_user_agent!r}"
    )
    assert mlb._strict_http is True, MLB_STRICT_DEFAULT_MESSAGE
    for scheme in ("https://", "http://"):
        assert_documented_retry_policy(
            mlb._session.get_adapter(scheme).max_retries,
            label=f"library-created Session {scheme} adapter",
        )

adapter = MlbDataAdapter()
try:
    assert adapter._session.headers["User-Agent"] == expected_user_agent
    assert adapter._strict_http is True, ADAPTER_STRICT_DEFAULT_MESSAGE
finally:
    adapter.close()


# --- Injected Session stays caller-owned and unmodified ---


class OwnershipSession(requests.Session):
    """Real Session that records close() so caller ownership is observable."""

    def __init__(self):
        super().__init__()
        self.close_calls = 0

    def close(self):
        self.close_calls += 1
        super().close()


session = OwnershipSession()
session.headers["User-Agent"] = "release-smoke-test/1.0"
session.headers["X-Release-Test"] = "preserved"
# max_retries=0 so a library retry policy mounted here would be detectable.
injected_https_adapter = HTTPAdapter(max_retries=0)
injected_http_adapter = HTTPAdapter(max_retries=0)
session.mount("https://", injected_https_adapter)
session.mount("http://", injected_http_adapter)
headers_before = dict(session.headers)

try:
    with Mlb(session=session) as mlb:
        assert mlb._session is session

    assert session.close_calls == 0, (
        "the library must not close a caller-injected Session"
    )
    assert dict(session.headers) == headers_before, dict(session.headers)
    assert session.headers["User-Agent"] == "release-smoke-test/1.0"
    assert session.headers["X-Release-Test"] == "preserved"
    assert session.get_adapter("https://") is injected_https_adapter, (
        "the injected https:// adapter was replaced"
    )
    assert session.get_adapter("http://") is injected_http_adapter, (
        "the injected http:// adapter was replaced"
    )
    for scheme in ("https://", "http://"):
        mounted_retries = session.get_adapter(scheme).max_retries
        assert mounted_retries.total == 0, (
            "the library must not mount its retry policy on an injected "
            f"Session: {scheme} total={mounted_retries.total}"
        )
finally:
    session.close()

assert session.close_calls == 1, (
    f"the smoke test must close its own Session exactly once, "
    f"saw {session.close_calls}"
)

print(f"smoke test passed for python-mlb-statsapi {installed_version}")
'''


ASYNC_SMOKE_TEST_SOURCE = '''
"""Async public API smoke test for an installed artifact with its async extra.

Runs inside a throwaway virtual environment against the installed
distribution, never against a repository checkout. Every exercised HTTP
response comes from HTTPX MockTransport, so this test performs no network I/O
and never reaches the MLB API.
"""

import asyncio
import importlib.metadata
import inspect
import logging
import sys
import sysconfig
import warnings
from pathlib import Path

import httpx

import mlbstatsapi
from mlbstatsapi import (
    AsyncMlb,
    AsyncMlbDataAdapter,
    MlbHttpCompatibilityWarning,
    MlbHttpError,
)

expected_version = sys.argv[1]

# Final 403 responses exercise both strict and 1.x compatibility behavior
# without contacting the live service.
FORBIDDEN_PAYLOAD = {"messageNumber": 403, "message": "Forbidden"}
SPORTS_URL = "https://statsapi.mlb.com/api/v1/sports"
ASYNC_MLB_STRICT_DEFAULT_MESSAGE = (
    "AsyncMlb.strict_http must default to True for the 1.1 contract"
)
ASYNC_ADAPTER_STRICT_DEFAULT_MESSAGE = (
    "AsyncMlbDataAdapter.strict_http must default to True for the 1.1 contract"
)

# Expected final 403s are logged by the adapter. Keep release output concise
# without configuring logging from inside the installed package.
package_logger = logging.getLogger("mlbstatsapi")
package_logger.addHandler(logging.NullHandler())
package_logger.propagate = False


# --- The installed artifact and its optional dependency ---

assert sys.prefix != sys.base_prefix, (
    "the async smoke test must run inside the throwaway virtual environment"
)

site_packages = Path(sysconfig.get_paths()["purelib"]).resolve()
package_file = Path(mlbstatsapi.__file__).resolve()
assert package_file.is_relative_to(site_packages), (
    f"mlbstatsapi was imported from {package_file}, not from the installed "
    f"distribution artifact under {site_packages}"
)

installed_version = importlib.metadata.version("python-mlb-statsapi")
assert installed_version == expected_version, (
    f"installed metadata reports {installed_version}, expected {expected_version}"
)

# In this otherwise-clean environment, importing HTTPX and reading its
# distribution metadata proves that installing the local artifact's [async]
# extra installed the optional transport dependency.
installed_httpx_version = importlib.metadata.version("httpx")
assert installed_httpx_version, "the async extra did not install HTTPX metadata"
assert httpx.__version__ == installed_httpx_version

for name in ("AsyncMlb", "AsyncMlbDataAdapter"):
    assert hasattr(mlbstatsapi, name), f"mlbstatsapi.{name} is not importable"
    assert getattr(mlbstatsapi, name) is not None, f"mlbstatsapi.{name} is None"


# --- Public constructor and lifecycle contracts ---

async_mlb_init = inspect.signature(AsyncMlb.__init__).parameters
async_adapter_init = inspect.signature(AsyncMlbDataAdapter.__init__).parameters

assert list(async_mlb_init) == [
    "self",
    "hostname",
    "logger",
    "timeout",
    "client",
    "strict_http",
]
assert async_mlb_init["hostname"].default == "statsapi.mlb.com"
assert async_mlb_init["logger"].default is None
assert async_mlb_init["timeout"].default == (3.05, 30.0)
assert async_mlb_init["client"].default is None
assert async_mlb_init["strict_http"].default is True, (
    ASYNC_MLB_STRICT_DEFAULT_MESSAGE
)
assert async_mlb_init["strict_http"].kind is inspect.Parameter.KEYWORD_ONLY

assert list(async_adapter_init) == [
    "self",
    "hostname",
    "ver",
    "logger",
    "timeout",
    "client",
    "strict_http",
]
assert async_adapter_init["hostname"].default == "statsapi.mlb.com"
assert async_adapter_init["ver"].default == "v1"
assert async_adapter_init["logger"].default is None
assert async_adapter_init["timeout"].default == (3.05, 30.0)
assert async_adapter_init["client"].default is None
assert async_adapter_init["strict_http"].default is True, (
    ASYNC_ADAPTER_STRICT_DEFAULT_MESSAGE
)
assert async_adapter_init["strict_http"].kind is inspect.Parameter.KEYWORD_ONLY
assert inspect.iscoroutinefunction(AsyncMlb.aclose)
assert inspect.iscoroutinefunction(AsyncMlbDataAdapter.aclose)


def forbidden_response(request: httpx.Request) -> httpx.Response:
    """Return one deterministic final 403 through HTTPX's fake transport."""
    return httpx.Response(
        403,
        headers={"Content-Type": "application/json"},
        json=FORBIDDEN_PAYLOAD,
        request=request,
    )


def assert_forbidden_error(exc: MlbHttpError, *, label: str) -> None:
    assert exc.status_code == 403, f"{label}: status_code={exc.status_code}"
    assert exc.reason == "Forbidden", f"{label}: reason={exc.reason!r}"
    assert exc.method == "GET", f"{label}: method={exc.method!r}"
    assert exc.url == SPORTS_URL, f"{label}: url={exc.url!r}"
    assert isinstance(exc.response_data, dict), (
        f"{label}: response_data={exc.response_data!r}"
    )
    for key, value in FORBIDDEN_PAYLOAD.items():
        assert exc.response_data.get(key) == value, (
            f"{label}: response_data={exc.response_data!r}"
        )


def compatibility_warnings(caught):
    return [
        record
        for record in caught
        if issubclass(record.category, MlbHttpCompatibilityWarning)
    ]


async def check_library_owned_lifecycle_and_user_agent() -> None:
    expected_user_agent = f"python-mlb-statsapi/{expected_version}"

    # Construction plus async context-manager cleanup. No request is made with
    # this library-created client; its configuration is inspected directly.
    client = AsyncMlb()
    owned_httpx_client = client._client
    assert owned_httpx_client.headers["User-Agent"] == expected_user_agent
    assert client._mlb_adapter_v1._strict_http is True, (
        ASYNC_MLB_STRICT_DEFAULT_MESSAGE
    )
    async with client as entered:
        assert entered is client
        assert owned_httpx_client.is_closed is False
    assert owned_httpx_client.is_closed is True

    # Explicit cleanup is supported and idempotent for a library-owned client.
    explicitly_closed = AsyncMlb()
    explicitly_owned_httpx_client = explicitly_closed._client
    await explicitly_closed.aclose()
    assert explicitly_owned_httpx_client.is_closed is True
    await explicitly_closed.aclose()
    assert explicitly_owned_httpx_client.is_closed is True


async def check_strict_http_and_caller_ownership() -> None:
    transport = httpx.MockTransport(forbidden_response)
    caller_client = httpx.AsyncClient(
        transport=transport,
        headers={
            "User-Agent": "release-async-smoke-test/1.0",
            "X-Release-Test": "preserved",
        },
    )
    headers_before = dict(caller_client.headers)

    try:
        # Omitting strict_http exercises the real True default. The context
        # manager must leave the injected HTTPX client caller-owned and open.
        async with AsyncMlb(client=caller_client) as strict_client:
            assert strict_client._client is caller_client
            assert strict_client._mlb_adapter_v1._strict_http is True, (
                ASYNC_MLB_STRICT_DEFAULT_MESSAGE
            )
            try:
                await strict_client.get_sports()
            except MlbHttpError as exc:
                assert_forbidden_error(
                    exc,
                    label="AsyncMlb(strict_http=True).get_sports()",
                )
            else:
                raise AssertionError(
                    "AsyncMlb strict_http=True did not raise MlbHttpError"
                )

        assert caller_client.is_closed is False, (
            "AsyncMlb must not close a caller-injected httpx.AsyncClient"
        )
        assert dict(caller_client.headers) == headers_before

        # Compatibility mode remains available through 1.x and returns the
        # endpoint's historical empty result with its compatibility warning.
        async with AsyncMlb(
            client=caller_client,
            strict_http=False,
        ) as compatibility_client:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                sports = await compatibility_client.get_sports()

        assert sports == [], (
            f"AsyncMlb(strict_http=False).get_sports() returned {sports!r}"
        )
        captured = compatibility_warnings(caught)
        assert len(captured) == 1, (
            "AsyncMlb(strict_http=False) expected exactly one "
            f"MlbHttpCompatibilityWarning, captured {captured!r}"
        )
        assert "strict_http=False" in str(captured[0].message)
        assert caller_client.is_closed is False, (
            "compatibility mode closed a caller-injected httpx.AsyncClient"
        )
    finally:
        await caller_client.aclose()

    assert caller_client.is_closed is True


async def check_standalone_data_adapter_library_owned_lifecycle() -> None:
    """Directly exercise AsyncMlbDataAdapter() and its own library-owned client.

    AsyncMlb() only ever constructs AsyncMlbDataAdapter through its own client,
    so this constructs the public standalone adapter with client=None to prove
    the library-owned-client construction and cleanup path independently.
    """
    expected_user_agent = f"python-mlb-statsapi/{expected_version}"

    adapter = AsyncMlbDataAdapter()
    owned_httpx_client = adapter._client
    assert adapter._owns_client is True, (
        "AsyncMlbDataAdapter() must own the httpx.AsyncClient it creates"
    )
    assert adapter._strict_http is True, ASYNC_ADAPTER_STRICT_DEFAULT_MESSAGE
    assert owned_httpx_client.headers["User-Agent"] == expected_user_agent, (
        f"library-created httpx.AsyncClient sends User-Agent "
        f"{owned_httpx_client.headers['User-Agent']!r}, expected "
        f"{expected_user_agent!r}"
    )
    assert owned_httpx_client.is_closed is False

    await adapter.aclose()
    assert owned_httpx_client.is_closed is True

    # Repeated cleanup of a library-owned client is safe/idempotent.
    await adapter.aclose()
    assert owned_httpx_client.is_closed is True


async def main() -> None:
    await check_library_owned_lifecycle_and_user_agent()
    await check_strict_http_and_caller_ownership()
    await check_standalone_data_adapter_library_owned_lifecycle()


asyncio.run(main())
print(
    f"async smoke test passed for python-mlb-statsapi {installed_version} "
    f"with HTTPX {installed_httpx_version}"
)
'''


class ValidationError(Exception):
    """A release validation check failed."""


def _log(message: str) -> None:
    print(message, flush=True)


def _read_expected_version(project_root: Path) -> str:
    """Read the declared project version from pyproject.toml.

    Uses tomllib when available and falls back to a narrow regex so the
    validator also runs on Python 3.10, which the package still supports.
    """
    pyproject = project_root / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")

    try:
        import tomllib
    except ModuleNotFoundError:
        match = re.search(
            r'^version\s*=\s*"([^"]+)"',
            text,
            flags=re.MULTILINE,
        )
        if match is None:
            raise ValidationError(f"could not find a version in {pyproject}")
        return match.group(1)

    data = tomllib.loads(text)
    project_version = data.get("project", {}).get("version")
    poetry_version = data.get("tool", {}).get("poetry", {}).get("version")
    version = project_version or poetry_version
    if not version:
        raise ValidationError(f"could not find a version in {pyproject}")
    return version


def _find_single(dist_dir: Path, pattern: str, label: str) -> Path:
    matches = sorted(dist_dir.glob(pattern))
    if not matches:
        present = ", ".join(sorted(path.name for path in dist_dir.iterdir())) or "nothing"
        raise ValidationError(
            f"{label}: no artifact matching {pattern!r} in {dist_dir}; "
            f"found {present}. Run `poetry build` first."
        )
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise ValidationError(
            f"{label}: expected exactly one artifact matching {pattern!r} in "
            f"{dist_dir}, found {len(matches)}: {names}. "
            "Remove stale artifacts and rebuild."
        )
    return matches[0]


def _check_wheel_metadata(wheel: Path, expected_version: str) -> None:
    with zipfile.ZipFile(wheel) as archive:
        metadata_names = [
            name
            for name in archive.namelist()
            if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_names) != 1:
            raise ValidationError(
                f"{WHEEL_LABEL} {wheel.name}: expected exactly one "
                f".dist-info/METADATA file, found {metadata_names}"
            )
        raw_metadata = archive.read(metadata_names[0]).decode("utf-8")

    metadata = Parser().parsestr(raw_metadata)

    name = metadata.get("Name")
    if name != DISTRIBUTION_NAME:
        raise ValidationError(
            f"{WHEEL_LABEL} {wheel.name}: metadata Name is {name!r}, "
            f"expected {DISTRIBUTION_NAME!r}"
        )

    version = metadata.get("Version")
    if version != expected_version:
        raise ValidationError(
            f"{WHEEL_LABEL} {wheel.name}: metadata Version is {version!r}, "
            f"expected {expected_version!r}"
        )

    requires_python = metadata.get("Requires-Python")
    if requires_python != EXPECTED_REQUIRES_PYTHON:
        raise ValidationError(
            f"{WHEEL_LABEL} {wheel.name}: metadata Requires-Python is "
            f"{requires_python!r}, expected {EXPECTED_REQUIRES_PYTHON!r}"
        )

    _log(
        f"  wheel metadata: Name={name} Version={version} "
        f"Requires-Python={requires_python}"
    )


def _check_sdist_contents(sdist: Path) -> None:
    with tarfile.open(sdist, "r:gz") as archive:
        members = archive.getnames()

    # Every path inside an sdist is prefixed with the versioned root directory.
    relative_paths = {name.split("/", 1)[1] for name in members if "/" in name}

    missing = [path for path in REQUIRED_SDIST_PATHS if path not in relative_paths]
    if missing:
        raise ValidationError(
            f"{SDIST_LABEL} {sdist.name}: missing required path(s) "
            f"{', '.join(missing)}; expected every path in "
            f"{', '.join(REQUIRED_SDIST_PATHS)}"
        )

    _log(f"  sdist contains: {', '.join(REQUIRED_SDIST_PATHS)}")


def _venv_python(venv_dir: Path) -> Path:
    candidates = (
        venv_dir / "bin" / "python",
        venv_dir / "Scripts" / "python.exe",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise ValidationError(f"no interpreter found in {venv_dir}")


def _run(command: list[str], *, cwd: Path, label: str) -> None:
    result = subprocess.run(command, cwd=cwd, check=False)
    if result.returncode != 0:
        printable = " ".join(command)
        raise ValidationError(
            f"{label} failed (exit code {result.returncode}): {printable}"
        )


def _create_clean_environment(venv_dir: Path) -> Path:
    """Create an empty virtual environment and return its interpreter."""
    venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
    return _venv_python(venv_dir)


def _check_clean_install(artifact: Path, expected_version: str, *, label: str) -> None:
    """Clean-install one distribution artifact and smoke test the sync result.

    Each artifact gets its own virtual environment so the wheel and the source
    distribution are never validated against a shared install.
    """
    with tempfile.TemporaryDirectory(prefix="python-mlb-statsapi-release-") as tmp:
        workspace = Path(tmp)
        venv_dir = workspace / "venv"

        _log(f"  creating clean virtual environment for the {label} in {venv_dir}")
        python = _create_clean_environment(venv_dir)

        _run(
            [str(python), "-m", "pip", "install", "--upgrade", "--quiet", "pip"],
            cwd=workspace,
            label=f"pip upgrade for the {label} environment",
        )

        _log(f"  installing {label}: {artifact.name}")
        _run(
            [str(python), "-m", "pip", "install", "--quiet", str(artifact.resolve())],
            cwd=workspace,
            label=f"{label} installation of {artifact.name}",
        )

        smoke_test = workspace / "release_smoke_test.py"
        smoke_test.write_text(SMOKE_TEST_SOURCE, encoding="utf-8")

        # Run from the temporary workspace so the repository checkout is not on
        # sys.path and cannot shadow the installed distribution artifact.
        _log(f"  running {label} smoke test against the installed artifact")
        _run(
            [str(python), str(smoke_test), expected_version],
            cwd=workspace,
            label=f"{label} smoke test",
        )


def _check_async_clean_install(
    artifact: Path,
    expected_version: str,
    *,
    label: str,
) -> None:
    """Clean-install one artifact with ``[async]`` and smoke test the result.

    This environment is separate from both sync artifact environments. That
    separation proves HTTPX arrives through the exact local wheel or sdist's
    optional extra rather than being left over from another validation phase.
    """
    with tempfile.TemporaryDirectory(
        prefix="python-mlb-statsapi-release-async-"
    ) as tmp:
        workspace = Path(tmp)
        venv_dir = workspace / "venv"

        _log(
            f"  creating clean async virtual environment for the {label} "
            f"in {venv_dir}"
        )
        python = _create_clean_environment(venv_dir)

        _run(
            [str(python), "-m", "pip", "install", "--upgrade", "--quiet", "pip"],
            cwd=workspace,
            label=f"pip upgrade for the {label} async environment",
        )

        artifact_with_extra = f"{artifact.resolve()}[async]"
        _log(f"  installing {label} with async extra: {artifact.name}")
        _run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--quiet",
                artifact_with_extra,
            ],
            cwd=workspace,
            label=f"{label} async-extra installation of {artifact.name}",
        )

        smoke_test = workspace / "release_async_smoke_test.py"
        smoke_test.write_text(ASYNC_SMOKE_TEST_SOURCE, encoding="utf-8")

        # Running from the temporary workspace keeps the repository checkout
        # off sys.path, exactly as the sync installed-artifact phase does.
        _log(
            f"  running {label} async smoke test against the installed artifact"
        )
        _run(
            [str(python), str(smoke_test), expected_version],
            cwd=workspace,
            label=f"{label} async smoke test for {artifact.name}",
        )


def validate(dist_dir: Path, expected_version: str) -> None:
    _log(f"Validating release {expected_version} in {dist_dir}")

    wheel = _find_single(
        dist_dir,
        f"{NORMALIZED_DISTRIBUTION_NAME}-{expected_version}-*.whl",
        WHEEL_LABEL,
    )
    _log(f"  wheel: {wheel.name}")

    sdist = _find_single(
        dist_dir,
        f"{NORMALIZED_DISTRIBUTION_NAME}-{expected_version}.tar.gz",
        SDIST_LABEL,
    )
    _log(f"  source distribution: {sdist.name}")

    _check_wheel_metadata(wheel, expected_version)
    _check_sdist_contents(sdist)

    # Separate environments: an sdist that cannot build, omits package files, or
    # loses a runtime dependency must not be masked by the wheel install.
    _check_clean_install(wheel, expected_version, label=WHEEL_LABEL)
    _check_clean_install(sdist, expected_version, label=SDIST_LABEL)

    # The optional dependency must be resolved from each exact artifact in a
    # fresh environment; a working wheel must not mask a broken sdist extra.
    _check_async_clean_install(wheel, expected_version, label=WHEEL_LABEL)
    _check_async_clean_install(sdist, expected_version, label=SDIST_LABEL)

    _log(f"Release validation passed for {DISTRIBUTION_NAME} {expected_version}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root containing pyproject.toml",
    )
    parser.add_argument(
        "--dist",
        type=Path,
        default=None,
        help="directory holding the built artifacts (default: <project-root>/dist)",
    )
    parser.add_argument(
        "--expected-version",
        default=None,
        help="version to validate (default: the version declared in pyproject.toml)",
    )
    args = parser.parse_args(argv)

    project_root = args.project_root.resolve()
    dist_dir = (args.dist or project_root / "dist").resolve()

    try:
        expected_version = args.expected_version or _read_expected_version(project_root)
        if not dist_dir.is_dir():
            raise ValidationError(
                f"{dist_dir} does not exist; run `poetry build` first"
            )
        validate(dist_dir, expected_version)
    except ValidationError as exc:
        print(f"Release validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
