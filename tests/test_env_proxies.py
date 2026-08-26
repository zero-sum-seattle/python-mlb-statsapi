"""Tests for ``mlbstatsapi._env_proxies.environment_proxy_map`` (issue #324).

PR #323 moved async retries into a custom HTTPX transport, which had the side
effect of disabling HTTPX's own environment-proxy discovery for library-created
async clients (see ``mlbstatsapi/_env_proxies.py`` for the full story).
``environment_proxy_map`` is the stdlib-only replacement for that discovery.

This module covers only the pure parsing in ``environment_proxy_map`` itself
and imports nothing from HTTPX, so it runs — and is meant to run — in the
no-httpx CI job: a stdlib-only helper is exactly where that job's coverage
matters most. The tests that exercise how the map is wired into an HTTPX
client (``create_library_async_client``) live in
tests/test_async_env_proxies.py, which skips as a whole without the ``async``
extra.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

from mlbstatsapi._env_proxies import environment_proxy_map

# Both cases of every proxy variable urllib.request.getproxies() reads, so a
# proxy set in the developer's own shell can never leak into a fixture.
PROXY_ENV_VARS = (
    "HTTP_PROXY",
    "http_proxy",
    "HTTPS_PROXY",
    "https_proxy",
    "ALL_PROXY",
    "all_proxy",
    "NO_PROXY",
    "no_proxy",
)


def clear_proxy_env(monkeypatch) -> None:
    for name in PROXY_ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def set_proxy_env(monkeypatch, env: dict) -> None:
    clear_proxy_env(monkeypatch)
    for key, value in env.items():
        monkeypatch.setenv(key, value)


def test_https_proxy_only(monkeypatch):
    set_proxy_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080"})
    assert environment_proxy_map() == {"https://": "http://corp:8080"}


def test_http_proxy_only(monkeypatch):
    set_proxy_env(monkeypatch, {"HTTP_PROXY": "http://corp:8080"})
    assert environment_proxy_map() == {"http://": "http://corp:8080"}


def test_all_proxy(monkeypatch):
    set_proxy_env(monkeypatch, {"ALL_PROXY": "http://corp:9"})
    assert environment_proxy_map() == {"all://": "http://corp:9"}


def test_bare_host_port_normalizes_to_http(monkeypatch):
    set_proxy_env(monkeypatch, {"HTTPS_PROXY": "corp:8080"})
    assert environment_proxy_map() == {"https://": "http://corp:8080"}


def test_no_proxy_subdomain_wildcard(monkeypatch):
    set_proxy_env(
        monkeypatch, {"HTTPS_PROXY": "http://corp:8080", "NO_PROXY": "mlb.com"}
    )
    assert environment_proxy_map() == {
        "https://": "http://corp:8080",
        "all://*mlb.com": None,
    }


def test_no_proxy_localhost_ipv4_ipv6(monkeypatch):
    set_proxy_env(
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
    set_proxy_env(monkeypatch, {"ALL_PROXY": "http://corp:8080", "NO_PROXY": "*"})
    assert environment_proxy_map() == {}


def test_empty_env(monkeypatch):
    set_proxy_env(monkeypatch, {})
    assert environment_proxy_map() == {}


def test_trust_env_false_ignores_everything(monkeypatch):
    set_proxy_env(monkeypatch, {"HTTPS_PROXY": "http://corp:8080"})
    assert environment_proxy_map(trust_env=False) == {}
