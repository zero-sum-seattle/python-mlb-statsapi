"""Helpers for detecting drift between model field aliases and MLB API response keys.

``MLBBaseModel`` is configured with ``extra="ignore"``, so a field whose alias does not
exactly match the key MLB sends is not a validation error: the value is discarded and
the field silently keeps its ``None`` default. Issue #246 is one instance of this. When
v0.7.1 stopped lowercasing every response key and moved to a camelCase alias generator,
fields whose names are a single lowercase token -- ``strikeouts``, ``putouts``,
``walkoffs``, ``nickname`` -- were left expecting ``strikeouts`` while the API sends
``strikeOuts``, so they never populated again.

The helpers here drive two checks:

* every key MLB sends that looks like a declared field must actually reach that field
* every field's alias must match the casing MLB uses for that key

Both run offline against recorded fixtures, and again against the live API under
``tests/external_tests`` so that renames on MLB's side surface too.
"""

from __future__ import annotations

import importlib
import json
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import mlbstatsapi
from pydantic import AliasChoices

from mlbstatsapi.models.base import MLBBaseModel

FIXTURE_DIR = Path(__file__).parent / "fixtures"
API_KEYS_FIXTURE = FIXTURE_DIR / "api_keys.json"
PAYLOADS_FIXTURE = FIXTURE_DIR / "model_payloads.json"

BASE_V1 = "https://statsapi.mlb.com/api/v1"
BASE_V1_1 = "https://statsapi.mlb.com/api/v1.1"

# Fixed identifiers so a re-record produces a comparable snapshot. Several exist only
# to reach keys MLB omits from an ordinary response: catcher-only fielding stats, the
# death fields on a deceased player, and a game recent enough to carry ABS challenges.
SOTO = 665742
SKUBAL = 669373
REALMUTO = 592663
AARON = 110001
PHILLIES = 147
GAME_PK = 775296
ABS_GAME_PK = 823837
SEASON = 2025

# Endpoints crawled to build the vocabulary of real API keys. Hydrations are requested
# generously: a key that never appears in a response cannot be checked for drift.
SNAPSHOT_ENDPOINTS = (
    f"{BASE_V1}/people/{SOTO}/stats?stats=season,career,seasonAdvanced,careerAdvanced,"
    "yearByYear,gameLog,byDayOfWeek,byMonth,homeAndAway,winLoss,expectedStatistics,"
    f"sabermetrics,pitchArsenal,hotColdZones&group=hitting&season={SEASON}",
    f"{BASE_V1}/people/{SKUBAL}/stats?stats=season,career,seasonAdvanced,careerAdvanced,"
    f"yearByYear,gameLog,pitchArsenal,sabermetrics,expectedStatistics&group=pitching&season={SEASON}",
    f"{BASE_V1}/people/{SOTO}/stats?stats=season,career,seasonAdvanced,yearByYear,gameLog"
    f"&group=fielding&season={SEASON}",
    f"{BASE_V1}/people/{REALMUTO}/stats?stats=season,career,yearByYear&group=catching&season={SEASON}",
    # A catcher's fielding split carries catcherERA and passedBall, which an outfielder's
    # does not.
    f"{BASE_V1}/people/{REALMUTO}/stats?stats=season,career&group=fielding&season={SEASON}",
    f"{BASE_V1}/people/{SOTO}/stats?stats=outsAboveAverage&group=fielding&season={SEASON}",
    # Death and nickname fields are only present for players they apply to.
    f"{BASE_V1}/people/{AARON}",
    f"{BASE_V1}/teams/{PHILLIES}/stats?stats=season,seasonAdvanced,career"
    f"&group=hitting,pitching,fielding&season={SEASON}",
    f"{BASE_V1}/people/{SOTO}?hydrate=stats(group=[hitting],type=[season])",
    f"{BASE_V1}/teams/{PHILLIES}?hydrate=venue,league,division,sport",
    f"{BASE_V1}/teams/{PHILLIES}/roster?rosterType=active",
    f"{BASE_V1}/schedule?sportId=1&date={SEASON}-07-04&hydrate=linescore,team,venue,decisions,"
    "probablePitcher,weather,officials,broadcasts",
    f"{BASE_V1}/venues/3313?hydrate=location,fieldInfo,timezone",
    f"{BASE_V1}/standings?leagueId=103&season={SEASON}&standingsTypes=regularSeason",
    f"{BASE_V1}/draft/2024",
    f"{BASE_V1}/attendance?teamId={PHILLIES}&season={SEASON}",
    f"{BASE_V1}/gamePace?season={SEASON}",
    f"{BASE_V1}/awards/MLBHOF/recipients",
    f"{BASE_V1}/seasons/{SEASON}?sportId=1",
    f"{BASE_V1}/divisions?sportId=1",
    f"{BASE_V1}/league?sportId=1",
    f"{BASE_V1}/sports",
    f"{BASE_V1_1}/game/{GAME_PK}/feed/live",
    # ABS challenges only appear on games played once the system was in use.
    f"{BASE_V1_1}/game/{ABS_GAME_PK}/feed/live",
    f"{BASE_V1}/game/{GAME_PK}/boxscore",
    f"{BASE_V1}/game/{GAME_PK}/linescore",
    f"{BASE_V1}/game/{GAME_PK}/playByPlay",
    f"{BASE_V1}/homeRunDerby/511101",
)


@dataclass(frozen=True)
class PayloadSpec:
    """Locates one real payload to record and check a model against.

    Exactly one of ``path`` and ``probe`` is used. ``path`` indexes into the response;
    ``probe`` selects the first nested dict containing that key, which is more durable
    for deeply nested payloads such as the live game feed.
    """

    label: str
    model: str
    url: str
    path: tuple[Any, ...] | None = None
    probe: str | None = None


PAYLOAD_SPECS = (
    PayloadSpec(
        "hitting_season",
        "mlbstatsapi.models.stats.hitting:SimpleHittingSplit",
        f"{BASE_V1}/people/{SOTO}/stats?stats=season&group=hitting&season={SEASON}",
        path=("stats", 0, "splits", 0, "stat"),
    ),
    PayloadSpec(
        "hitting_season_advanced",
        "mlbstatsapi.models.stats.hitting:AdvancedHittingSplit",
        f"{BASE_V1}/people/{SOTO}/stats?stats=seasonAdvanced&group=hitting&season={SEASON}",
        path=("stats", 0, "splits", 0, "stat"),
    ),
    PayloadSpec(
        "pitching_season",
        "mlbstatsapi.models.stats.pitching:SimplePitchingSplit",
        f"{BASE_V1}/people/{SKUBAL}/stats?stats=season&group=pitching&season={SEASON}",
        path=("stats", 0, "splits", 0, "stat"),
    ),
    PayloadSpec(
        "pitching_season_advanced",
        "mlbstatsapi.models.stats.pitching:AdvancedPitchingSplit",
        f"{BASE_V1}/people/{SKUBAL}/stats?stats=seasonAdvanced&group=pitching&season={SEASON}",
        path=("stats", 0, "splits", 0, "stat"),
    ),
    PayloadSpec(
        "fielding_season",
        "mlbstatsapi.models.stats.fielding:SimpleFieldingSplit",
        f"{BASE_V1}/people/{SOTO}/stats?stats=season&group=fielding&season={SEASON}",
        path=("stats", 0, "splits", 0, "stat"),
    ),
    PayloadSpec(
        "fielding_season_catcher",
        "mlbstatsapi.models.stats.fielding:SimpleFieldingSplit",
        f"{BASE_V1}/people/{REALMUTO}/stats?stats=season&group=fielding&season={SEASON}",
        path=("stats", 0, "splits", 0, "stat"),
    ),
    PayloadSpec(
        "outs_above_average",
        "mlbstatsapi.models.stats.stats:OutsAboveAverage",
        f"{BASE_V1}/people/{SOTO}/stats?stats=outsAboveAverage&group=fielding&season={SEASON}",
        path=("stats", 0, "splits", 0),
    ),
    PayloadSpec(
        "catching_season",
        "mlbstatsapi.models.stats.catching:SimpleCatchingSplit",
        f"{BASE_V1}/people/{REALMUTO}/stats?stats=season&group=catching&season={SEASON}",
        path=("stats", 0, "splits", 0, "stat"),
    ),
    PayloadSpec(
        "hitting_sabermetrics",
        "mlbstatsapi.models.stats.stats:Sabermetrics",
        f"{BASE_V1}/people/{SOTO}/stats?stats=sabermetrics&group=hitting&season={SEASON}",
        path=("stats", 0, "splits", 0, "stat"),
    ),
    PayloadSpec(
        "person",
        "mlbstatsapi.models.people.people:Person",
        f"{BASE_V1}/people/{SOTO}",
        path=("people", 0),
    ),
    PayloadSpec(
        "person_deceased",
        "mlbstatsapi.models.people.people:Person",
        f"{BASE_V1}/people/{AARON}",
        path=("people", 0),
    ),
    PayloadSpec(
        "abs_challenge_info",
        "mlbstatsapi.models.game.gamedata.attributes:AbsChallengeInfo",
        f"{BASE_V1_1}/game/{ABS_GAME_PK}/feed/live",
        probe="usedSuccessful",
    ),
    PayloadSpec(
        "season",
        "mlbstatsapi.models.seasons.season:Season",
        f"{BASE_V1}/seasons/{SEASON}?sportId=1",
        path=("seasons", 0),
    ),
    PayloadSpec(
        "venue",
        "mlbstatsapi.models.venues.venue:Venue",
        f"{BASE_V1}/venues/3313?hydrate=location,fieldInfo,timezone",
        path=("venues", 0),
    ),
    PayloadSpec(
        "team_records",
        "mlbstatsapi.models.standings.attributes:TeamRecords",
        f"{BASE_V1}/standings?leagueId=103&season={SEASON}&standingsTypes=regularSeason",
        path=("records", 0, "teamRecords", 0),
    ),
    PayloadSpec(
        "schedule_game",
        "mlbstatsapi.models.schedules.attributes:ScheduleGames",
        f"{BASE_V1}/schedule?sportId=1&date={SEASON}-07-04",
        path=("dates", 0, "games", 0),
    ),
    PayloadSpec(
        "game_status",
        "mlbstatsapi.models.game.gamedata.attributes:GameStatus",
        f"{BASE_V1_1}/game/{GAME_PK}/feed/live",
        probe="startTimeTBD",
    ),
    PayloadSpec(
        "game_data_game",
        "mlbstatsapi.models.game.gamedata.attributes:GameDataGame",
        f"{BASE_V1_1}/game/{GAME_PK}/feed/live",
        probe="calendarEventID",
    ),
    PayloadSpec(
        "pitch_coordinates",
        "mlbstatsapi.models.data.data:PitchCoordinates",
        f"{BASE_V1}/game/{GAME_PK}/playByPlay",
        probe="aX",
    ),
)


def normalize(key: str) -> str:
    """Reduce a key to the form that makes ``strikeouts`` and ``strikeOuts`` comparable."""
    return key.replace("_", "").lower()


def validation_aliases(model: type[MLBBaseModel], field_name: str) -> list[str]:
    """Every key this field validates against, explicit, generated or a set of choices."""
    field = model.model_fields[field_name]
    alias = field.validation_alias
    if isinstance(alias, AliasChoices):
        return [choice for choice in alias.choices if isinstance(choice, str)]
    if isinstance(alias, str):
        return [alias]
    return [field.alias or field_name]


def effective_alias(model: type[MLBBaseModel], field_name: str) -> str:
    """The key this field is primarily expected to arrive under."""
    return validation_aliases(model, field_name)[0]


def accepted_keys(model: type[MLBBaseModel]) -> set[str]:
    """Keys that populate a field, given ``populate_by_name`` accepts names too."""
    keys = set(model.model_fields)
    for name in model.model_fields:
        keys.update(validation_aliases(model, name))
    return keys


def resolve(dotted: str) -> type[MLBBaseModel]:
    module, _, name = dotted.partition(":")
    return getattr(importlib.import_module(module), name)


def iter_models() -> Iterator[type[MLBBaseModel]]:
    """Every model in the package, with submodules imported so subclasses are registered."""
    for module in pkgutil.walk_packages(mlbstatsapi.__path__, f"{mlbstatsapi.__name__}."):
        try:
            importlib.import_module(module.name)
        except ImportError:
            continue

    def descend(cls):
        for subclass in cls.__subclasses__():
            yield subclass
            yield from descend(subclass)

    yield from sorted(set(descend(MLBBaseModel)), key=lambda c: (c.__module__, c.__name__))


def dropped_keys(model: type[MLBBaseModel], payload: dict) -> list[tuple[str, str]]:
    """Keys in ``payload`` that name a declared field but miss it on casing.

    Returns ``(api_key, field_name)`` pairs. Keys with no matching field are ignored:
    MLB adds fields the library has not modelled yet, which is not drift.
    """
    accepted = accepted_keys(model)
    by_normalized = {normalize(name): name for name in model.model_fields}
    missed = []
    for key in payload:
        if key in accepted:
            continue
        field = by_normalized.get(normalize(key))
        if field is not None:
            missed.append((key, field))
    return sorted(missed)


def alias_mismatches(vocabulary: set[str]) -> list[tuple[type[MLBBaseModel], str, str, list[str]]]:
    """Fields whose alias differs only in casing from a key the API really sends.

    Returns ``(model, field_name, expected_alias, observed_keys)``. A field is only
    reported when the API demonstrably uses that key, so unused or stale fields stay
    quiet rather than producing noise.
    """
    observed: dict[str, set[str]] = {}
    for key in vocabulary:
        observed.setdefault(normalize(key), set()).add(key)

    mismatches = []
    for model in iter_models():
        for name in model.model_fields:
            aliases = validation_aliases(model, name)
            real = set().union(*(observed.get(normalize(a), set()) for a in aliases))
            if real and not real.intersection(aliases):
                mismatches.append((model, name, aliases[0], sorted(real)))
    return mismatches


def collect_keys(payload: Any, into: set[str] | None = None) -> set[str]:
    """Every distinct dict key anywhere in a response."""
    keys = set() if into is None else into
    if isinstance(payload, dict):
        for key, value in payload.items():
            keys.add(key)
            collect_keys(value, keys)
    elif isinstance(payload, list):
        for value in payload:
            collect_keys(value, keys)
    return keys


def extract(payload: Any, spec: PayloadSpec) -> dict:
    """Pull the sub-payload a spec points at."""
    if spec.path is not None:
        for step in spec.path:
            payload = payload[step]
        return payload

    stack = [payload]
    while stack:
        current = stack.pop(0)
        if isinstance(current, dict):
            if spec.probe in current:
                return current
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)
    raise LookupError(f"no dict containing {spec.probe!r} in response for {spec.label}")


def load_api_keys() -> set[str]:
    return set(json.loads(API_KEYS_FIXTURE.read_text())["keys"])


def load_payloads() -> dict[str, dict]:
    return json.loads(PAYLOADS_FIXTURE.read_text())["payloads"]


def describe_dropped(model: type[MLBBaseModel], payload: dict, missed: list[tuple[str, str]]) -> str:
    lines = [
        f"{model.__name__} silently drops {len(missed)} value(s) returned by the MLB API.",
        "Each field below keeps its None default because its alias does not match the "
        "key the API sends. Set an explicit Field(alias=...) to fix it:",
        "",
    ]
    for key, field in missed:
        alias = effective_alias(model, field)
        lines.append(f"  {field}: expects {alias!r}, API sends {key!r} = {payload[key]!r}")
    return "\n".join(lines)
