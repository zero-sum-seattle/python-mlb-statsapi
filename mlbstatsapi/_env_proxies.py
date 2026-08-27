"""Build an HTTPX-compatible proxy mount map from the environment.

HTTPX only discovers ``HTTP_PROXY`` / ``HTTPS_PROXY`` / ``ALL_PROXY`` /
``NO_PROXY`` for itself when it builds its own transport, which happens only
when the caller does not pass ``transport=`` (see ``allow_env_proxies =
trust_env and transport is None`` in ``httpx.Client.__init__``). The async
retry transport (``_async_transport.py``) always passes ``transport=``, so
that discovery never runs, and environment proxy support silently disappears
for library-created async clients (issue #324).

This module reimplements that discovery from the stdlib and hands the result
to HTTPX's public ``mounts=`` argument instead, so the library stays off
HTTPX's private ``httpx._utils.get_environment_proxies``. The parsing here
intentionally mirrors that private function's semantics, verified against
installed httpx 0.28.1. The differential test in
``tests/test_async_env_proxies.py`` (``test_matches_stock_httpx_env_proxy_resolution``)
is the drift alarm: it resolves the same URLs against a stock
``httpx.AsyncClient()`` and against this module's output on every run, so a
future httpx release changing ``NO_PROXY`` or proxy semantics fails that test
instead of silently diverging.

No httpx import here: environment variables in, a plain ``dict`` out.
"""

from __future__ import annotations

import ipaddress
from urllib.request import getproxies


def environment_proxy_map(*, trust_env: bool = True) -> dict[str, str | None]:
    """Return an HTTPX ``mounts=``-shaped map of proxies from the environment.

    Keys are URL patterns such as ``"https://"`` or ``"all://*mlb.com"``; a
    ``None`` value means "bypass the proxy for this pattern" and is meaningful
    only when a broader pattern (from ``ALL_PROXY``) would otherwise match.
    """
    if not trust_env:
        return {}

    proxy_info = getproxies()
    mounts: dict[str, str | None] = {}

    for scheme in ("http", "https", "all"):
        value = proxy_info.get(scheme)
        if value:
            mounts[f"{scheme}://"] = value if "://" in value else f"http://{value}"

    no_proxy_hosts = [host.strip() for host in proxy_info.get("no", "").split(",")]
    for hostname in no_proxy_hosts:
        if hostname == "*":
            return {}
        elif hostname:
            if "://" in hostname:
                mounts[hostname] = None
            elif _is_ipv4(hostname):
                mounts[f"all://{hostname}"] = None
            elif _is_ipv6(hostname):
                mounts[f"all://[{hostname}]"] = None
            elif hostname.lower() == "localhost":
                mounts[f"all://{hostname}"] = None
            else:
                mounts[f"all://*{hostname}"] = None

    return mounts


def _is_ipv4(hostname: str) -> bool:
    try:
        ipaddress.IPv4Address(hostname.split("/")[0])
    except ValueError:
        return False
    return True


def _is_ipv6(hostname: str) -> bool:
    try:
        ipaddress.IPv6Address(hostname.split("/")[0])
    except ValueError:
        return False
    return True
