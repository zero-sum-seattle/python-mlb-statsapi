"""Tests for environment proxy support in the async transport (issue #324).

PR #323 moved async retries into a custom HTTPX transport. HTTPX only builds
its own environment-proxy mounts when the caller leaves ``transport=None``
(``allow_env_proxies = trust_env and transport is None`` in
``httpx.Client.__init__``), so passing a transport to install retries
silently disabled ``HTTP_PROXY`` / ``HTTPS_PROXY`` / ``ALL_PROXY`` /
``NO_PROXY`` support for every library-created async client.

Two layers are covered:

* ``mlbstatsapi._env_proxies.environment_proxy_map`` is pure stdlib parsing,
  tested directly against fixtures for every documented ``NO_PROXY`` form.
* ``create_library_async_client`` wires that map into HTTPX's public
  ``mounts=`` argument. The differential test at the bottom pins that wiring
  to HTTPX's own environment-proxy discovery, so a semantic change in a
  future HTTPX release (a patch bump is allowed by the ``httpx>=0.28.1,<1.0``
  pin) shows up as a failing test instead of silent drift.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from mlbstatsapi._env_proxies import environment_proxy_map

# Every test below that touches HTTPX skips as a unit when the optional
# ``async`` extra is not installed, matching the guard used throughout the
# async test suite (see tests/test_async_optional_dependency.py).
httpx = pytest.importorskip("httpx", reason="requires the async extra (HTTPX)")

from mlbstatsapi._async_transport import (  # noqa: E402
    MlbAsyncRetryTransport,
    create_library_async_client,
)
from mlbstatsapi.async_mlb_dataadapter import AsyncMlbDataAdapter  # noqa: E402

SLEEP_TARGET = "mlbstatsapi._async_transport.asyncio.sleep"
INNER_TRANSPORT_TARGET = "mlbstatsapi._async_transport.httpx.AsyncHTTPTransport"

# Both cases of every proxy variable urllib.request.getproxies() reads, so a
# proxy set in the developer's own shell can never leak into a fixture.
_PROXY_ENV_VARS = (
    "HTTP_PROXY",
    "http_proxy",
    "HTTPS_PROXY",
    "https_proxy",
    "ALL_PROXY",
    "all_proxy",
    "NO_PROXY",
    "no_proxy",
)


def _clear_proxy_env(monkeypatch) -> None:
    for name in _PROXY_ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def _set_env(monkeypatch, env: dict) -> None:
    _clear_proxy_env(monkeypatch)
    for key, value in env.items():
        monkeypatch.setenv(key, value)


# ---------------------------------------------------------------------------
# environment_proxy_map(): pure stdlib parsing
# ---------------------------------------------------------------------------


def test_https_proxy_only(monkeypatch):
    _set_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080"})
    assert environment_proxy_map() == {"https://": "http://corp:8080"}


def test_http_proxy_only(monkeypatch):
    _set_env(monkeypatch, {"HTTP_PROXY": "http://corp:8080"})
    assert environment_proxy_map() == {"http://": "http://corp:8080"}


def test_all_proxy(monkeypatch):
    _set_env(monkeypatch, {"ALL_PROXY": "http://corp:9"})
    assert environment_proxy_map() == {"all://": "http://corp:9"}


def test_bare_host_port_normalizes_to_http(monkeypatch):
    _set_env(monkeypatch, {"HTTPS_PROXY": "corp:8080"})
    assert environment_proxy_map() == {"https://": "http://corp:8080"}


def test_no_proxy_subdomain_wildcard(monkeypatch):
    _set_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080", "NO_PROXY": "mlb.com"})
    assert environment_proxy_map() == {
        "https://": "http://corp:8080",
        "all://*mlb.com": None,
    }


def test_no_proxy_localhost_ipv4_ipv6(monkeypatch):
    _set_env(
        monkeypatch,
        {"HTTPS_PROXY": "http://corp:8080", "NO_PROXY": "localhost,127.0.0.1,::1"},
    )
    assert environment_proxy_map() == {
        "https://": "http://corp:8080",
        "all://localhost": None,
        "all://127.0.0.1": None,
        "all://[::1]": None,
    }


def test_no_proxy_star_disables_every_proxy(monkeypatch):
    _set_env(monkeypatch, {"ALL_PROXY": "http://corp:8080", "NO_PROXY": "*"})
    assert environment_proxy_map() == {}


def test_empty_env(monkeypatch):
    _set_env(monkeypatch, {})
    assert environment_proxy_map() == {}


def test_trust_env_false_ignores_everything(monkeypatch):
    _set_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080"})
    assert environment_proxy_map(trust_env=False) == {}


# ---------------------------------------------------------------------------
# create_library_async_client(): wiring the map into HTTPX
# ---------------------------------------------------------------------------


def test_one_retry_policy_shared_across_direct_and_proxy_transports(monkeypatch):
    _set_env(
        monkeypatch,
        {"HTTPS_PROXY": "http://corp:8080", "HTTP_PROXY": "http://corp:9090"},
    )

    async def scenario():
        client = create_library_async_client()
        try:
            transports = [client._transport] + [
                mount for mount in client._mounts.values() if mount is not None
            ]
            assert len(transports) == 3
            assert all(isinstance(t, MlbAsyncRetryTransport) for t in transports)

            policy = transports[0]._retry_policy
            assert all(t._retry_policy is policy for t in transports)
        finally:
            await client.aclose()

    asyncio.run(scenario())


def test_aclose_closes_every_proxy_transport(monkeypatch):
    _set_env(
        monkeypatch,
        {"HTTPS_PROXY": "http://corp:8080", "HTTP_PROXY": "http://corp:9090"},
    )

    async def scenario():
        with patch.object(
            httpx.AsyncHTTPTransport, "aclose", new_callable=AsyncMock
        ) as mock_aclose:
            client = create_library_async_client()
            proxy_mounts = [m for m in client._mounts.values() if m is not None]
            assert len(proxy_mounts) == 2

            await client.aclose()

        # The direct transport plus every proxy transport, none skipped and
        # none closed twice.
        assert mock_aclose.call_count == 1 + len(proxy_mounts)

    asyncio.run(scenario())


def test_injected_client_is_unmodified_by_proxy_env(monkeypatch):
    _set_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080"})

    transport = httpx.MockTransport(lambda request: httpx.Response(200))
    client = httpx.AsyncClient(transport=transport)
    original_mounts = dict(client._mounts)

    adapter = AsyncMlbDataAdapter(client=client)

    assert adapter._owns_client is False
    assert adapter._client is client
    assert adapter._client._transport is transport
    assert adapter._client._mounts == original_mounts


def test_retry_fires_through_a_proxied_transport(monkeypatch):
    _set_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080"})

    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        return httpx.Response(503) if call_count == 1 else httpx.Response(200)

    async def scenario():
        with (
            patch(INNER_TRANSPORT_TARGET, lambda **kwargs: httpx.MockTransport(handler)),
            patch(SLEEP_TARGET, new_callable=AsyncMock),
        ):
            client = create_library_async_client()
            try:
                return await client.get("https://statsapi.mlb.com/api/v1/sports")
            finally:
                await client.aclose()

    response = asyncio.run(scenario())
    assert response.status_code == 200
    assert call_count == 2


# ---------------------------------------------------------------------------
# Differential test: pin our wiring to HTTPX's own env-proxy discovery.
#
# Each case was hand-verified against stock httpx 0.28.1 discovery
# (httpx.AsyncClient() with no transport=). If this starts failing against a
# newer 0.x httpx, treat it as a signal that NO_PROXY / proxy semantics moved
# out from under us, not as a test to loosen.
# ---------------------------------------------------------------------------


def proxy_target(transport):
    inner = getattr(transport, "_inner", transport)
    pool = getattr(inner, "_pool", None)
    url = getattr(pool, "_proxy_url", None)
    return str(url) if url is not None else None


DIFFERENTIAL_CASES = [
    (
        {"HTTPS_PROXY": "http://corp:8080"},
        ["https://statsapi.mlb.com/api", "http://statsapi.mlb.com/api"],
    ),
    (
        {"HTTP_PROXY": "http://corp:8080"},
        ["https://statsapi.mlb.com/api", "http://statsapi.mlb.com/api"],
    ),
    (
        {"ALL_PROXY": "http://corp:9"},
        ["https://statsapi.mlb.com/api", "http://anything.test/"],
    ),
    (
        {"HTTPS_PROXY": "corp:8080"},
        ["https://statsapi.mlb.com/api"],
    ),
    (
        {
            "HTTPS_PROXY": "http://corp:8080",
            "NO_PROXY": "mlb.com,localhost,127.0.0.1,::1",
        },
        [
            "https://statsapi.mlb.com/api",
            "https://mlb.com/",
            "https://other.test/",
            "http://localhost:8000/",
            "https://127.0.0.1/",
            "https://[::1]/",
        ],
    ),
    (
        {"HTTPS_PROXY": "http://corp:8080", "NO_PROXY": "*"},
        ["https://statsapi.mlb.com/api"],
    ),
    (
        {},
        ["https://statsapi.mlb.com/api"],
    ),
]


@pytest.mark.parametrize(
    "env, urls",
    DIFFERENTIAL_CASES,
    ids=[",".join(env) or "empty" for env, _ in DIFFERENTIAL_CASES],
)
def test_matches_stock_httpx_env_proxy_resolution(monkeypatch, env, urls):
    _set_env(monkeypatch, env)

    async def scenario():
        stock = httpx.AsyncClient()
        ours = create_library_async_client()
        try:
            for url in urls:
                stock_transport = stock._transport_for_url(httpx.URL(url))
                our_transport = ours._transport_for_url(httpx.URL(url))

                assert isinstance(our_transport, MlbAsyncRetryTransport), url
                assert proxy_target(our_transport) == proxy_target(
                    stock_transport
                ), url
        finally:
            await stock.aclose()
            await ours.aclose()

    asyncio.run(scenario())
