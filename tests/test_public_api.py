"""Contract tests for the version 1.x public API surface.

These tests freeze the supported package-root symbols, constructor signatures,
exception and warning inheritance, Session ownership guarantees, and the
explicit ``Mlb`` and ``AsyncMlb`` public-method manifests documented in
``docs/public-api.md``.

The package-root surface is split across two manifests because "public API" and
"available without optional dependencies" are different questions. Everything in
either manifest is public and stable in 1.x; only the async manifest needs the
optional ``async`` extra to resolve.

They must not contact the live MLB API.
"""

from __future__ import annotations

import importlib.util
import inspect
import re
import warnings
from pathlib import Path
from typing import Any

import pytest
import requests
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

from http_contract_support import assert_library_retry_policy


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_API_DOC = PROJECT_ROOT / "docs" / "public-api.md"


# ---------------------------------------------------------------------------
# Package-root manifests
# ---------------------------------------------------------------------------

# Supported package-root symbols for the 1.x series that are always available,
# including in a sync-only install without the ``async`` extra. Sync-only
# environments freeze their surface against this manifest, so a symbol that
# needs an optional dependency must not be added here.
SUPPORTED_PACKAGE_ROOT_SYMBOLS: tuple[str, ...] = (
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

# Supported package-root symbols for the 1.x series that require the optional
# ``async`` extra (HTTPX). These are public and stable exactly like the symbols
# above; only their availability is conditional. See docs/public-api.md.
OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS: tuple[str, ...] = (
    "AsyncMlb",
    "AsyncMlbDataAdapter",
)

# The complete supported package-root API for the 1.x series.
SUPPORTED_PACKAGE_ROOT_API: tuple[str, ...] = (
    SUPPORTED_PACKAGE_ROOT_SYMBOLS + OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS
)

# Legacy helpers remain supported but are not preferred for new code.
LEGACY_PACKAGE_ROOT_HELPERS: tuple[str, ...] = (
    "get_stat_attributes",
    "return_splits",
)

# Submodules that appear on the package namespace as an import side effect.
# They are not part of the supported public API; see docs/public-api.md.
ACCIDENTAL_PACKAGE_ROOT_SUBMODULES: tuple[str, ...] = (
    "exceptions",
    "mlb_api",
    "mlb_dataadapter",
    "mlb_module",
    "models",
    "warnings",
)


# HTTPX ships only with the ``async`` extra, so this module must stay runnable
# in a sync-only environment. Cases that assert async availability are skipped
# there; tests/test_async_optional_dependency.py covers the sync-only half of
# the contract in child interpreters that block HTTPX outright.
def _async_extra_installed() -> bool:
    """Report whether HTTPX is available, without importing it here."""
    try:
        return importlib.util.find_spec("httpx") is not None
    except ImportError:
        # An environment may also make httpx unavailable by raising from a meta
        # path finder instead of reporting no spec.
        return False


requires_async_extra = pytest.mark.skipif(
    not _async_extra_installed(),
    reason="requires the optional async extra (HTTPX)",
)


# Python 3.14 renders typing.Union[a, b] as "a | b" while Python 3.10-3.13
# render "Union[a, b]". The annotation object itself is unchanged, so the legacy
# spelling is rewritten here and one manifest stays valid across the whole
# supported interpreter matrix.
LEGACY_UNION_RENDERINGS: dict[str, str] = {
    "Union[str, List[int]]": "str | List[int]",
}


def _normalize_annotation(annotation: Any) -> str:
    rendered = (
        annotation
        if isinstance(annotation, str)
        else inspect.formatannotation(annotation)
    )
    for legacy, pep604 in LEGACY_UNION_RENDERINGS.items():
        rendered = rendered.replace(legacy, pep604)
    return rendered


def _normalize_signature(fn: Any) -> str:
    """Return a stable, readable signature string without the ``self`` parameter."""
    sig = inspect.signature(fn)
    parts: list[str] = []
    for name, parameter in sig.parameters.items():
        if name == "self":
            continue
        if parameter.kind is inspect.Parameter.VAR_KEYWORD:
            annotation = ""
            if parameter.annotation is not inspect.Parameter.empty:
                annotation = f": {_normalize_annotation(parameter.annotation)}"
            parts.append(f"**{name}{annotation}")
            continue
        if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            parts.append(f"*{name}")
            continue
        piece = name
        if parameter.annotation is not inspect.Parameter.empty:
            piece += f": {_normalize_annotation(parameter.annotation)}"
        if parameter.default is not inspect.Parameter.empty:
            piece += f"={parameter.default!r}"
        parts.append(piece)
    return "(" + ", ".join(parts) + ")"


# Explicit inventory of public methods defined directly on Mlb.
# A newly exposed method must update this manifest intentionally.
MLB_PUBLIC_METHOD_MANIFEST: dict[str, str] = {
    "close": "()",
    "__enter__": "()",
    "__exit__": "(exc_type, exc, traceback)",
    "get_people": "(sport_id: int=1, **params)",
    "get_person": "(player_id: int, **params)",
    "get_persons": "(person_ids: str | List[int], **params)",
    "get_people_id": (
        "(fullname: str, sport_id: int=1, search_key: str='fullName', **params)"
    ),
    "get_teams": "(sport_id: int=1, **params)",
    "get_team": "(team_id: int, **params)",
    "get_team_id": "(team_name: str, search_key: str='name', **params)",
    "get_team_roster": "(team_id: int, **params)",
    "get_team_coaches": "(team_id: int, **params)",
    "get_schedule": (
        "(date: str=None, start_date: str=None, end_date: str=None, "
        "sport_id: int=1, team_id: int=None, **params)"
    ),
    "get_scheduled_games_by_date": (
        "(date: str=None, start_date: str=None, end_date: str=None, "
        "sport_id: int=1, **params)"
    ),
    "get_game": "(game_id: int, **params)",
    "get_game_play_by_play": "(game_id: int, **params)",
    "get_game_line_score": "(game_id: int, **params)",
    "get_game_box_score": "(game_id: int, **params)",
    "get_game_ids": (
        "(date: str=None, start_date: str=None, end_date: str=None, "
        "sport_id: int=1, **params)"
    ),
    "get_gamepace": "(season: str, sport_id=1, **params)",
    "get_venue": "(venue_id: int, **params)",
    "get_venues": "(**params)",
    "get_venue_id": "(venue_name: str, search_key: str='name', **params)",
    "get_sport": "(sport_id: int, **params)",
    "get_sports": "(**params)",
    "get_sport_id": "(sport_name: str, search_key: str='name', **params)",
    "get_league": "(league_id: int, **params)",
    "get_leagues": "(**params)",
    "get_league_id": "(league_name: str, search_key: str='name', **params)",
    "get_division": "(division_id: int, **params)",
    "get_divisions": "(**params)",
    "get_division_id": "(division_name: str, search_key: str='name', **params)",
    "get_season": "(season_id: str, sport_id: int=1, **params)",
    "get_seasons": "(sport_id: int=1, **params)",
    "get_standings": "(league_id: int, season: str, **params)",
    "get_attendance": (
        "(team_id: int=None, league_id: int=None, "
        "league_list_id: str=None, **params)"
    ),
    "get_draft": "(year_id: int, **params)",
    "get_awards": "(award_id: str, **params)",
    "get_homerun_derby": "(game_id, **params)",
    "get_team_stats": "(team_id: int, stats: list, groups: list, **params)",
    "get_players_stats_for_game": "(person_id: int, game_id: int, **params)",
    "get_player_stats": "(person_id: int, stats: list, groups: list, **params)",
    "get_stats": "(stats: list, groups: list, **params: dict)",
}

# Explicit inventory of public methods defined directly on AsyncMlb.
# Only currently supported async endpoints belong here.
ASYNC_MLB_PUBLIC_METHOD_MANIFEST: dict[str, str] = {
    "aclose": "()",
    "__aenter__": "()",
    "__aexit__": "(exc_type, exc, traceback)",
    "get_team": "(team_id: int, **params)",
    "get_teams": "(sport_id: int=1, **params)",
    "get_person": "(player_id: int, **params)",
    "get_people": "(sport_id: int=1, **params)",
    "get_schedule": (
        "(date: str=None, start_date: str=None, end_date: str=None, "
        "sport_id: int=1, team_id: int=None, **params)"
    ),
}


# ---------------------------------------------------------------------------
# Package-root symbols
# ---------------------------------------------------------------------------


def test_supported_package_root_symbols_are_unique() -> None:
    assert len(SUPPORTED_PACKAGE_ROOT_SYMBOLS) == len(set(SUPPORTED_PACKAGE_ROOT_SYMBOLS))


def test_optional_async_package_root_symbols_are_unique() -> None:
    assert len(OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS) == len(
        set(OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS)
    )


def test_package_root_manifests_are_disjoint() -> None:
    """A symbol is either always available or gated behind the async extra."""
    assert not set(SUPPORTED_PACKAGE_ROOT_SYMBOLS) & set(
        OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS
    )


def test_supported_package_root_api_is_the_union_of_both_manifests() -> None:
    assert set(SUPPORTED_PACKAGE_ROOT_API) == set(SUPPORTED_PACKAGE_ROOT_SYMBOLS) | set(
        OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS
    )
    assert len(SUPPORTED_PACKAGE_ROOT_API) == len(set(SUPPORTED_PACKAGE_ROOT_API))


def test_async_symbols_are_part_of_the_supported_api() -> None:
    """Async symbols are supported 1.x API, not merely optional add-ons."""
    for name in ("AsyncMlb", "AsyncMlbDataAdapter"):
        assert name in OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS
        assert name in SUPPORTED_PACKAGE_ROOT_API


def test_supported_package_root_symbols_are_importable_from_package() -> None:
    for name in SUPPORTED_PACKAGE_ROOT_SYMBOLS:
        assert hasattr(mlbstatsapi, name), name
        assert getattr(mlbstatsapi, name) is not None


@pytest.mark.parametrize("name", SUPPORTED_PACKAGE_ROOT_SYMBOLS)
def test_supported_symbols_are_importable_by_name(name: str) -> None:
    namespace: dict[str, Any] = {}
    exec(f"from mlbstatsapi import {name}", namespace)
    assert name in namespace
    assert namespace[name] is getattr(mlbstatsapi, name)


@pytest.mark.parametrize("name", OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS)
def test_optional_async_symbols_are_discoverable_without_the_extra(name: str) -> None:
    """Discoverability is unconditional; only resolution needs HTTPX."""
    assert name in dir(mlbstatsapi)


@requires_async_extra
@pytest.mark.parametrize("name", OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS)
def test_optional_async_symbols_are_importable_with_the_extra(name: str) -> None:
    namespace: dict[str, Any] = {}
    exec(f"from mlbstatsapi import {name}", namespace)
    assert name in namespace
    assert namespace[name] is getattr(mlbstatsapi, name)


@requires_async_extra
def test_async_data_adapter_resolves_to_the_async_module() -> None:
    adapter_class = mlbstatsapi.AsyncMlbDataAdapter
    assert adapter_class.__module__ == "mlbstatsapi.async_mlb_dataadapter"
    assert adapter_class.__name__ == "AsyncMlbDataAdapter"


def test_package_does_not_define_all_in_version_1_0() -> None:
    """``__all__`` is omitted so star-import behavior is not silently narrowed."""
    assert getattr(mlbstatsapi, "__all__", None) is None


def test_star_import_includes_supported_symbols() -> None:
    """Only the always-available manifest is asserted here.

    Async symbols resolve lazily, so whether a wildcard import sees them depends
    on whether something already touched them in this interpreter. Their
    documented access path is an explicit import, not ``import *``.
    """
    namespace: dict[str, Any] = {}
    exec("from mlbstatsapi import *", namespace)
    for name in SUPPORTED_PACKAGE_ROOT_SYMBOLS:
        assert name in namespace, name


def test_star_import_currently_includes_accidental_submodules() -> None:
    """Document current wildcard behavior without promoting it to supported API."""
    namespace: dict[str, Any] = {}
    exec("from mlbstatsapi import *", namespace)
    for name in ACCIDENTAL_PACKAGE_ROOT_SUBMODULES:
        assert name in namespace, name


def test_legacy_helpers_remain_package_root_importable() -> None:
    assert return_splits is mlbstatsapi.return_splits
    assert get_stat_attributes is mlbstatsapi.get_stat_attributes
    assert callable(return_splits)
    assert callable(get_stat_attributes)
    for name in LEGACY_PACKAGE_ROOT_HELPERS:
        assert name in SUPPORTED_PACKAGE_ROOT_SYMBOLS


# ---------------------------------------------------------------------------
# Documented classification
# ---------------------------------------------------------------------------


def _documented_package_root_classifications() -> dict[str, str]:
    """Return the symbol/status rows of the classification table in the docs."""
    text = PUBLIC_API_DOC.read_text(encoding="utf-8")
    section = text.split("### Classification of package-root symbols", 1)[1]
    section = re.split(r"\n#{2,} ", section, maxsplit=1)[0]

    rows: dict[str, str] = {}
    for line in section.splitlines():
        match = re.match(r"^\|\s*`([A-Za-z_][A-Za-z0-9_]*)`\s*\|(.+?)\|\s*$", line)
        if match:
            rows[match.group(1)] = match.group(2).strip()
    return rows


def test_documentation_classifies_every_supported_package_root_symbol() -> None:
    documented = _documented_package_root_classifications()
    for name in SUPPORTED_PACKAGE_ROOT_API:
        assert name in documented, f"{name} is missing from the classification table"


def test_documentation_classifies_async_symbols_as_public_and_optional() -> None:
    """Public API status and optional-dependency availability stay separate."""
    documented = _documented_package_root_classifications()
    for name in OPTIONAL_ASYNC_PACKAGE_ROOT_SYMBOLS:
        status = documented[name]
        assert "Public and stable in 1.x" in status, status
        assert "`async` extra" in status, status


# ---------------------------------------------------------------------------
# Constructor signatures
# ---------------------------------------------------------------------------


def _parameter_names(fn: Any) -> list[str]:
    return [
        name
        for name in inspect.signature(fn).parameters
        if name != "self"
    ]


def test_mlb_constructor_parameter_order_and_defaults() -> None:
    parameters = inspect.signature(Mlb.__init__).parameters

    assert _parameter_names(Mlb.__init__) == [
        "hostname",
        "logger",
        "timeout",
        "session",
        "strict_http",
    ]
    assert parameters["hostname"].default == "statsapi.mlb.com"
    assert parameters["logger"].default is None
    assert parameters["timeout"].default == (3.05, 30.0)
    assert parameters["session"].default is None
    assert parameters["strict_http"].default is True
    assert parameters["strict_http"].kind is inspect.Parameter.KEYWORD_ONLY


@requires_async_extra
def test_async_mlb_constructor_parameter_order_and_defaults() -> None:
    async_mlb = mlbstatsapi.AsyncMlb
    parameters = inspect.signature(async_mlb.__init__).parameters

    assert _parameter_names(async_mlb.__init__) == [
        "hostname",
        "logger",
        "timeout",
        "client",
        "strict_http",
    ]
    assert parameters["hostname"].default == "statsapi.mlb.com"
    assert parameters["logger"].default is None
    assert parameters["timeout"].default == (3.05, 30.0)
    assert parameters["client"].default is None
    assert parameters["strict_http"].default is True
    assert parameters["strict_http"].kind is inspect.Parameter.KEYWORD_ONLY


def test_mlb_data_adapter_constructor_parameter_order_and_defaults() -> None:
    parameters = inspect.signature(MlbDataAdapter.__init__).parameters

    assert _parameter_names(MlbDataAdapter.__init__) == [
        "hostname",
        "ver",
        "logger",
        "timeout",
        "session",
        "strict_http",
    ]
    assert parameters["hostname"].default == "statsapi.mlb.com"
    assert parameters["ver"].default == "v1"
    assert parameters["logger"].default is None
    assert parameters["timeout"].default == (3.05, 30.0)
    assert parameters["session"].default is None
    assert parameters["strict_http"].default is True
    assert parameters["strict_http"].kind is inspect.Parameter.KEYWORD_ONLY


def test_mlb_result_constructor_parameter_order_and_defaults() -> None:
    parameters = inspect.signature(MlbResult.__init__).parameters

    assert _parameter_names(MlbResult.__init__) == [
        "status_code",
        "message",
        "data",
    ]
    assert parameters["status_code"].default is inspect.Parameter.empty
    assert parameters["message"].default is inspect.Parameter.empty
    assert parameters["data"].default is None


def test_strict_http_rejects_positional_argument_for_mlb() -> None:
    with pytest.raises(TypeError):
        Mlb("statsapi.mlb.com", None, (3.05, 30.0), None, True)  # type: ignore[misc]


def test_strict_http_rejects_positional_argument_for_adapter() -> None:
    with pytest.raises(TypeError):
        MlbDataAdapter(
            "statsapi.mlb.com",
            "v1",
            None,
            (3.05, 30.0),
            None,
            True,
        )  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Mlb public method manifest
# ---------------------------------------------------------------------------


def test_mlb_public_method_manifest_has_unique_names() -> None:
    assert len(MLB_PUBLIC_METHOD_MANIFEST) == len(set(MLB_PUBLIC_METHOD_MANIFEST))


def test_mlb_public_method_manifest_matches_class_dict() -> None:
    discovered = {
        name
        for name, obj in Mlb.__dict__.items()
        if inspect.isfunction(obj)
        and (not name.startswith("_") or name in ("__enter__", "__exit__"))
        and name != "__init__"
    }
    assert discovered == set(MLB_PUBLIC_METHOD_MANIFEST)


@pytest.mark.parametrize("method_name, expected", MLB_PUBLIC_METHOD_MANIFEST.items())
def test_mlb_public_method_signature(method_name: str, expected: str) -> None:
    method = getattr(Mlb, method_name)
    actual = _normalize_signature(method)
    assert actual == expected, f"{method_name}: {actual} != {expected}"


def test_mlb_public_endpoint_count() -> None:
    endpoint_methods = [
        name
        for name in MLB_PUBLIC_METHOD_MANIFEST
        if not name.startswith("_") and name != "close"
    ]
    assert len(endpoint_methods) == 40
    assert len(MLB_PUBLIC_METHOD_MANIFEST) == 43


# ---------------------------------------------------------------------------
# AsyncMlb public method manifest
# ---------------------------------------------------------------------------


def test_async_mlb_public_method_manifest_has_unique_names() -> None:
    assert len(ASYNC_MLB_PUBLIC_METHOD_MANIFEST) == len(
        set(ASYNC_MLB_PUBLIC_METHOD_MANIFEST)
    )


@requires_async_extra
def test_async_mlb_public_method_manifest_matches_class_dict() -> None:
    async_mlb = mlbstatsapi.AsyncMlb
    discovered = {
        name
        for name, obj in async_mlb.__dict__.items()
        if inspect.isfunction(obj)
        and (not name.startswith("_") or name in ("__aenter__", "__aexit__"))
        and name != "__init__"
    }
    assert discovered == set(ASYNC_MLB_PUBLIC_METHOD_MANIFEST)


@requires_async_extra
@pytest.mark.parametrize(
    "method_name, expected", ASYNC_MLB_PUBLIC_METHOD_MANIFEST.items()
)
def test_async_mlb_public_method_signature(method_name: str, expected: str) -> None:
    method = getattr(mlbstatsapi.AsyncMlb, method_name)
    assert inspect.iscoroutinefunction(method), method_name
    actual = _normalize_signature(method)
    assert actual == expected, f"{method_name}: {actual} != {expected}"


# ---------------------------------------------------------------------------
# Exception and warning inheritance
# ---------------------------------------------------------------------------


def test_exception_hierarchy() -> None:
    assert issubclass(TheMlbStatsApiException, Exception)
    assert issubclass(MlbTransportError, TheMlbStatsApiException)
    assert issubclass(MlbTimeoutError, MlbTransportError)
    assert issubclass(MlbHttpError, TheMlbStatsApiException)
    assert issubclass(MlbDecodeError, TheMlbStatsApiException)


def test_exceptions_are_publicly_imported() -> None:
    assert mlbstatsapi.TheMlbStatsApiException is TheMlbStatsApiException
    assert mlbstatsapi.MlbTransportError is MlbTransportError
    assert mlbstatsapi.MlbTimeoutError is MlbTimeoutError
    assert mlbstatsapi.MlbHttpError is MlbHttpError
    assert mlbstatsapi.MlbDecodeError is MlbDecodeError


def test_broad_and_specific_exception_catches() -> None:
    with pytest.raises(TheMlbStatsApiException):
        raise MlbTransportError("transport")
    with pytest.raises(MlbTransportError):
        raise MlbTimeoutError("timeout")
    with pytest.raises(MlbTimeoutError):
        raise MlbTimeoutError("timeout")
    with pytest.raises(MlbHttpError):
        raise MlbHttpError(500, "Internal Server Error", "https://example.test")
    with pytest.raises(MlbDecodeError):
        raise MlbDecodeError("bad json")
    with pytest.raises(TheMlbStatsApiException):
        raise MlbDecodeError("bad json")


def test_mlb_http_error_stable_attributes() -> None:
    exc = MlbHttpError(
        status_code=502,
        reason="Bad Gateway",
        url="https://statsapi.mlb.com/api/v1/sports",
        method="get",
        response_data={"message": "nope"},
        body_excerpt="nope",
    )
    assert exc.status_code == 502
    assert exc.reason == "Bad Gateway"
    assert exc.url == "https://statsapi.mlb.com/api/v1/sports"
    assert exc.method == "GET"
    assert exc.response_data == {"message": "nope"}
    assert exc.body_excerpt == "nope"


def test_compatibility_warning_inherits_from_future_warning() -> None:
    assert issubclass(MlbHttpCompatibilityWarning, FutureWarning)
    assert mlbstatsapi.MlbHttpCompatibilityWarning is MlbHttpCompatibilityWarning


# ---------------------------------------------------------------------------
# Retry policy
# ---------------------------------------------------------------------------


def test_create_retry_policy_contract() -> None:
    assert callable(create_retry_policy)
    assert inspect.signature(create_retry_policy).parameters == {}

    first = create_retry_policy()
    second = create_retry_policy()

    assert isinstance(first, Retry)
    assert first is not second
    assert_library_retry_policy(first)
    assert_library_retry_policy(second)


# ---------------------------------------------------------------------------
# MlbResult
# ---------------------------------------------------------------------------


def test_mlb_result_public_attributes_and_non_mutation() -> None:
    payload = {"copyright": "MLB", "sports": [{"id": 1}]}
    result = MlbResult(200, "OK", payload)

    assert result.status_code == 200
    assert result.message == "OK"
    assert result.data == {"sports": [{"id": 1}]}
    assert payload == {"copyright": "MLB", "sports": [{"id": 1}]}


def test_mlb_result_default_data_is_empty_dict() -> None:
    result = MlbResult(404, "Not Found")
    assert result.data == {}


# ---------------------------------------------------------------------------
# Context managers and Session ownership
# ---------------------------------------------------------------------------


def test_mlb_context_manager_returns_self_and_closes_library_session() -> None:
    with Mlb() as mlb:
        assert mlb is mlb.__enter__()
        session = mlb._session
        assert mlb._owns_session is True
    assert mlb._closed is True
    # Requests marks a closed Session; a second close must remain safe.
    mlb.close()
    assert mlb._closed is True
    # The underlying Session object still exists but was closed by the client.
    assert session is mlb._session


def test_mlb_context_manager_does_not_close_injected_session() -> None:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "public-api-test/1.0",
            "X-Public-Api-Test": "preserved",
        }
    )
    try:
        with Mlb(session=session) as mlb:
            assert mlb._owns_session is False
            assert mlb._session is session
        mlb.close()
        assert session.headers["User-Agent"] == "public-api-test/1.0"
        assert session.headers["X-Public-Api-Test"] == "preserved"
        # Injected Sessions remain usable after the client exits.
        assert session.headers.get("X-Public-Api-Test") == "preserved"
    finally:
        session.close()


def test_library_created_session_receives_user_agent_and_retries() -> None:
    with Mlb() as mlb:
        assert "python-mlb-statsapi/" in mlb._session.headers["User-Agent"]
        https_adapter = mlb._session.get_adapter("https://example.test")
        assert_library_retry_policy(https_adapter.max_retries)


def test_injected_session_adapters_remain_untouched() -> None:
    session = requests.Session()
    original_adapters = dict(session.adapters)
    try:
        with Mlb(session=session):
            assert session.adapters == original_adapters
    finally:
        session.close()


def test_adapter_close_owns_only_library_sessions() -> None:
    adapter = MlbDataAdapter()
    adapter.close()
    adapter.close()
    assert adapter._closed is True

    session = requests.Session()
    try:
        injected = MlbDataAdapter(session=session)
        injected.close()
        injected.close()
        assert injected._owns_session is False
        assert session.headers is not None
    finally:
        session.close()


def test_adapter_supports_documented_api_versions() -> None:
    for version in ("v1", "v1.1"):
        adapter = MlbDataAdapter(ver=version)
        try:
            assert adapter.url.endswith(f"/api/{version}/")
        finally:
            adapter.close()


def test_compatibility_warning_can_be_filtered_by_public_class() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warnings.warn("probe", MlbHttpCompatibilityWarning)
    assert len(caught) == 1
    assert caught[0].category is MlbHttpCompatibilityWarning
