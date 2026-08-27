"""Tests for async client env-proxy wiring in _async_transport.py (issue #324).

PR #323 moved async retries into a custom HTTPX transport, mounted onto
library-created clients via ``AsyncClient(transport=...)``. httpx 0.28.1 only
builds its own environment-proxy mounts when the caller leaves
``transport=None`` (``allow_env_proxies = trust_env and transport is None`` in
``httpx.Client.__init__``), so passing a transport silently disabled
``HTTP_PROXY`` / ``HTTPS_PROXY`` / ``ALL_PROXY`` / ``NO_PROXY`` support for
every library-created async client.

``create_library_async_client`` (in ``mlbstatsapi/_async_transport.py``)
rebuilds that discovery via ``mlbstatsapi._env_proxies.environment_proxy_map``
and wires it through HTTPX's public ``mounts=`` argument instead. This module
covers that wiring: shared retry policy, transport cleanup, injected-client
isolation, retries through a proxy, and — at the bottom — a differential test
against HTTPX's own env-proxy discovery. The pure parsing behind the map is
covered separately in tests/test_env_proxies.py, which has no HTTPX
dependency and runs even without the ``async`` extra.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

# The whole module needs a real HTTPX-backed client, so it skips as a unit
# when the optional ``async`` extra is not installed, matching the guard used
# throughout the async test suite (see tests/test_async_optional_dependency.py).
httpx = pytest.importorskip("httpx", reason="requires the async extra (HTTPX)")

from mlbstatsapi._async_transport import (  # noqa: E402
    MlbAsyncRetryTransport,
    create_library_async_client,
)
from mlbstatsapi.async_mlb_dataadapter import AsyncMlbDataAdapter  # noqa: E402

from test_env_proxies import set_proxy_env  # noqa: E402

SLEEP_TARGET = "mlbstatsapi._async_transport.asyncio.sleep"
INNER_TRANSPORT_TARGET = "mlbstatsapi._async_transport.httpx.AsyncHTTPTransport"


# ---------------------------------------------------------------------------
# create_library_async_client(): wiring the map into HTTPX
# ---------------------------------------------------------------------------


def test_one_retry_policy_shared_across_direct_and_proxy_transports(monkeypatch):
    set_proxy_env(
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
    # NO_PROXY adds a bypass mount. That is what makes this a real regression
    # test: the bypass branch mounts None specifically so HTTPX falls back to
    # client._transport for that pattern instead of routing through (and
    # later double-closing) a second reference to the same `direct` object.
    # Without a bypass entry in the fixture, `len(proxy_mounts) == 2` below
    # would still hold even if the bypass branch mounted `direct` instead of
    # None, since there would be nothing to tell the two apart.
    set_proxy_env(
        monkeypatch,
        {
            "HTTPS_PROXY": "http://corp:8080",
            "HTTP_PROXY": "http://corp:9090",
            "NO_PROXY": "mlb.com",
        },
    )

    async def scenario():
        with patch.object(
            httpx.AsyncHTTPTransport, "aclose", new_callable=AsyncMock
        ) as mock_aclose:
            client = create_library_async_client()
            assert len(client._mounts) == 3

            proxy_mounts = [m for m in client._mounts.values() if m is not None]
            # Pinned to 2, not derived after the fact: if the bypass branch
            # ever mounts `direct` instead of None, this becomes 3 and fails
            # here, before the tautological count below could paper over it.
            assert len(proxy_mounts) == 2

            await client.aclose()

        # The direct transport plus the two real proxy transports; the
        # NO_PROXY bypass mount is None and contributes no separate close.
        assert mock_aclose.call_count == 1 + len(proxy_mounts)

    asyncio.run(scenario())


def test_injected_client_is_unmodified_by_proxy_env(monkeypatch):
    set_proxy_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080"})

    transport = httpx.MockTransport(lambda request: httpx.Response(200))
    client = httpx.AsyncClient(transport=transport)
    original_mounts = dict(client._mounts)

    async def scenario():
        adapter = AsyncMlbDataAdapter(client=client)

        assert adapter._owns_client is False
        assert adapter._client is client
        assert adapter._client._transport is transport
        assert adapter._client._mounts == original_mounts

        await client.aclose()

    asyncio.run(scenario())


def test_retry_fires_through_a_proxied_transport(monkeypatch):
    set_proxy_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080"})

    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        return httpx.Response(503) if call_count == 1 else httpx.Response(200)

    async def scenario():
        with (
            patch(
                INNER_TRANSPORT_TARGET, lambda **kwargs: httpx.MockTransport(handler)
            ),
            patch(SLEEP_TARGET, new_callable=AsyncMock),
        ):
            client = create_library_async_client()
            try:
                # Pin resolution to the proxy mount rather than the direct
                # fallback, so a request to statsapi.mlb.com with HTTPS_PROXY
                # set is guaranteed to exercise the proxied transport below,
                # not just happen to because both wrap the same handler.
                target = httpx.URL("https://statsapi.mlb.com/api/v1/sports")
                assert client._transport_for_url(target) is not client._transport

                return await client.get(str(target))
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
# newer 0.x httpx, that is the drift alarm: it means NO_PROXY / proxy
# semantics moved out from under environment_proxy_map's stdlib
# reimplementation, and the two need to be reconciled, not the test loosened.
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
    set_proxy_env(monkeypatch, env)

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
