# Public API Contract (1.x)

This document is the authoritative public API contract for the
`python-mlb-statsapi` **1.x** series.

It defines which package-root symbols, constructor signatures, exception and
warning relationships, resource ownership rules, and `Mlb` and `AsyncMlb`
endpoint methods are supported after version 1.0. Maintainers should use this
document when deciding whether a change is a patch, a minor release, or a major
release.

This package is an unofficial wrapper for the MLB Stats API and is not
affiliated with Major League Baseball.

Related documents:

* [HTTP transport](http-transport.md) — timeouts, retries, strict mode, and Session details
* Issue #286 — define the stable 1.0 public API
* Issue #282 — parent 1.0 release tracking

## Stability policy

During the 1.x series:

* Existing supported package-root symbols will not be removed or renamed
* Required constructor parameters will not be added without compatibility handling
* Positional and keyword-only parameter boundaries are part of the API
* Structured exception inheritance will remain compatible
* Documented Session ownership behavior will remain compatible
* Documented endpoint-level 404 return shapes will remain compatible

`strict_http=False` is a compatibility mode for users migrating from pre-1.0
behavior. It will remain available throughout the 1.x release series and may
be removed in 2.0. New code should use the default `strict_http=True` behavior
and handle `MlbHttpError`.

The following may still evolve in a compatible way:

* New optional parameters
* New endpoint methods
* New model fields
* New exception subclasses under `TheMlbStatsApiException`
* New documented public helpers
* Bug fixes
* Additional supported Python versions

Semantic versioning expectations after 1.0:

| Change | Typical release |
| --- | --- |
| Bug fix that preserves documented contracts | patch |
| Compatible addition (optional arg, new endpoint, new model field) | minor |
| Removal or rename of a supported symbol | major |
| Breaking change to a documented constructor signature | major |
| Breaking change to documented exception inheritance | major |
| Breaking change to documented Session ownership | major |
| Breaking change to a documented 404 return shape | major |

## Package-root imports

Supported symbols are importable as:

```python
import mlbstatsapi
from mlbstatsapi import Mlb
```

and via:

```python
from mlbstatsapi import (
    Mlb,
    MlbDataAdapter,
    MlbResult,
    create_retry_policy,
    TheMlbStatsApiException,
    MlbTransportError,
    MlbTimeoutError,
    MlbHttpError,
    MlbDecodeError,
    MlbHttpCompatibilityWarning,
    return_splits,
    get_stat_attributes,
)
```

The symbols above are available in every install. `AsyncMlb` and
`AsyncMlbDataAdapter` are equally public, but they resolve only when the
optional `async` extra is installed; see
[Optional async support](#optional-async-support).

### Classification of package-root symbols

Status and availability are separate questions. Every symbol below is public and
covered by the stability policy above; the availability column records whether
resolving it needs an optional dependency.

| Symbol | Status | Availability |
| --- | --- | --- |
| `Mlb` | Public and stable in 1.x | Always available |
| `AsyncMlb` | Public and stable in 1.x | Requires the optional `async` extra |
| `MlbDataAdapter` | Public and stable in 1.x | Always available |
| `AsyncMlbDataAdapter` | Public and stable in 1.x | Requires the optional `async` extra |
| `MlbResult` | Public and stable in 1.x | Always available |
| `create_retry_policy` | Public and stable in 1.x | Always available |
| `TheMlbStatsApiException` | Public and stable in 1.x | Always available |
| `MlbTransportError` | Public and stable in 1.x | Always available |
| `MlbTimeoutError` | Public and stable in 1.x | Always available |
| `MlbHttpError` | Public and stable in 1.x | Always available |
| `MlbDecodeError` | Public and stable in 1.x | Always available |
| `MlbHttpCompatibilityWarning` | Public and stable in 1.x | Always available |
| `return_splits` | Public legacy helper, stable in 1.x but not preferred for new code | Always available |
| `get_stat_attributes` | Public legacy helper, stable in 1.x but not preferred for new code | Always available |

`AsyncMlb` and `AsyncMlbDataAdapter` are supported 1.x API on the same terms as
the synchronous symbols: they will not be removed or renamed during the
series, and their documented behavior stays compatible. Only their
availability is conditional, because their HTTP dependency ships with the
`async` extra. See
[Optional async support](#optional-async-support).

No package-root symbol is marked deprecated in version 1.0. Deprecation requires
a documented replacement, a warning strategy, a removal timeline, and a
separate focused issue.

### Accidentally exposed submodule names

Python attaches imported submodules to the package namespace. The following
names may appear via `dir(mlbstatsapi)` and `from mlbstatsapi import *`, but
they are **not** part of the supported public API:

| Name | Where exposed | Recommended 1.0 status | Follow-up |
| --- | --- | --- | --- |
| `exceptions` | package attribute / star import | Accidentally exposed | Yes — dedicated cleanup issue |
| `warnings` | package attribute / star import | Accidentally exposed | Yes — dedicated cleanup issue |
| `mlb_api` | package attribute / star import | Accidentally exposed | Yes — dedicated cleanup issue |
| `mlb_dataadapter` | package attribute / star import | Accidentally exposed | Yes — dedicated cleanup issue |
| `mlb_module` | package attribute / star import | Accidentally exposed | Yes — dedicated cleanup issue |
| `models` | package attribute / star import | Accidentally exposed | Yes — dedicated cleanup issue |

These names are not documented as public imports. Prefer the explicit
package-root symbols above. Do not remove them from star imports in a patch
release without an approved issue; wildcard callers may currently receive them.

### Why `__all__` is not defined

Version 1.0 intentionally omits `__all__`.

Without `__all__`, `from mlbstatsapi import *` currently includes both the
supported symbols and the accidentally exposed submodule names listed above.

Adding `__all__` that lists only the supported symbols would silently change
wildcard-import behavior by removing those submodule names. Adding them to
`__all__` would incorrectly promote accidental exposure into the supported
surface.

A future focused issue may introduce `__all__` after deciding how to treat the
accidental submodule names (for example, a documented deprecation period).

## Optional async support

`AsyncMlb` and `AsyncMlbDataAdapter` are public package-root symbols, like
`Mlb` and `MlbDataAdapter`, and appear in the classification table above. Their
HTTP dependency is optional and installed with the `async` extra:

```bash
pip install "python-mlb-statsapi[async]"
```

With the extra installed:

```python
from mlbstatsapi import AsyncMlb, AsyncMlbDataAdapter
```

Async symbols are resolved on first access, so the optional dependency is not
imported by `import mlbstatsapi`. A synchronous-only install is unaffected:

* `import mlbstatsapi` succeeds without the `async` extra
* every package-root symbol marked "Always available" above stays importable
* nothing in the synchronous surface changes

Requesting async functionality without the extra raises `ImportError` naming
the install command above. That failure happens only when async functionality
is requested — importing the package, or any supported synchronous symbol,
never triggers it.

The async HTTP library is an implementation detail. It is not re-exported from
the package root, and its types are not part of the public API.

## Primary client

`Mlb` is the primary synchronous client.

### Constructor

```text
Mlb(
    hostname="statsapi.mlb.com",
    logger=None,
    timeout=(3.05, 30.0),
    session=None,
    *,
    strict_http=True,
)
```

Stable constructor rules:

* Parameter order above is part of the API
* Default values above are part of the API
* `strict_http` is keyword-only
* Version 1.0 defaults `strict_http` to `True`
* Pass `strict_http=False` for the historical empty-result compatibility path
  on final non-404 4xx responses

Private attributes such as `_session`, `_owns_session`, `_mlb_adapter_v1`, and
`_mlb_adapter_v1_1` are **not** public API.

### Context-manager behavior

```python
with mlbstatsapi.Mlb() as mlb:
    person = mlb.get_person(664034)
```

* `Mlb.__enter__` returns `self`
* `Mlb.__exit__` calls `close()`
* Repeated `close()` calls are safe
* Library-owned Sessions are closed
* Caller-injected Sessions are not closed

### API versions used by `Mlb`

`Mlb` constructs internal adapters for both `v1` and `v1.1` that share one
Session. Most endpoint methods use `v1`. `get_game` uses the `v1.1` live feed
endpoint. Standalone `MlbDataAdapter(ver="v1")` and
`MlbDataAdapter(ver="v1.1")` remain supported.

## AsyncMlb public client

`AsyncMlb` is the public asynchronous client and requires the optional `async`
extra.

### Constructor

```text
AsyncMlb(
    hostname="statsapi.mlb.com",
    logger=None,
    timeout=(3.05, 30.0),
    client=None,
    *,
    strict_http=True,
)
```

Parameter order and default values above are part of the API.
`strict_http` is keyword-only.

### Lifecycle

* `async with AsyncMlb(...) as mlb` returns the `AsyncMlb` instance itself
* `AsyncMlb.__aexit__` awaits cleanup
* Explicit cleanup with `await mlb.aclose()` is supported
* Repeated `aclose()` calls are safe
* Library-owned async clients are closed
* Caller-injected async clients remain caller-owned and open

### Concurrency

One `AsyncMlb` instance supports concurrent in-flight requests on the same
event loop. Concurrency is caller-controlled. Cross-event-loop use is not
promised.

### API versions used by `AsyncMlb`

`AsyncMlb` constructs internal adapters for both `v1` and `v1.1` that share
one HTTPX client, mirroring `Mlb`'s shared-Session pattern. Most endpoint
methods use `v1`. `get_game` uses the `v1.1` live feed endpoint. `AsyncMlb`
owns the shared client, exactly as `Mlb` owns the shared `Session`: it creates
one when the caller passes none, closes only a client it created, and hands
the same client to both adapters.

Retries are a property of that client, not of either adapter. A
library-created client is built with the library retry transport mounted on
it, the way a library-created `Session` is built with the library retry
adapters mounted on it, so both API versions retry identically without either
adapter holding retry state. A caller-injected client keeps whatever transport
its caller mounted.

### Endpoint methods

The currently supported awaitable endpoint methods are:

```text
get_team(team_id: int, **params)
get_teams(sport_id: int = 1, **params)
get_team_roster(team_id: int, **params)
get_team_coaches(team_id: int, **params)
get_person(player_id: int, **params)
get_people(sport_id: int = 1, **params)
get_schedule(
    date: str = None,
    start_date: str = None,
    end_date: str = None,
    sport_id: int = 1,
    team_id: int = None,
    **params,
)
get_sport(sport_id: int, **params)
get_sports(**params)
get_league(league_id: int, **params)
get_leagues(**params)
get_division(division_id: int, **params)
get_divisions(**params)
get_season(season_id: str, sport_id: int = 1, **params)
get_seasons(sport_id: int = 1, **params)
get_venue(venue_id: int, **params)
get_venues(**params)
get_standings(league_id: int, season: str, **params)
get_attendance(
    team_id: int = None,
    league_id: int = None,
    league_list_id: str = None,
    **params,
)
get_draft(year_id: int, **params)
get_awards(award_id: str, **params)
get_homerun_derby(game_id, **params)
get_team_stats(team_id: int, stats: list, groups: list, **params)
get_players_stats_for_game(person_id: int, game_id: int, **params)
get_player_stats(person_id: int, stats: list, groups: list, **params)
get_stats(stats: list, groups: list, **params)
get_persons(person_ids: str | list[int], **params)
get_scheduled_games_by_date(
    date: str = None,
    start_date: str = None,
    end_date: str = None,
    sport_id: int = 1,
    **params,
)
get_gamepace(season: str, sport_id=1, **params)
get_team_id(team_name: str, search_key: str = 'name', **params)
get_people_id(
    fullname: str,
    sport_id: int = 1,
    search_key: str = 'fullName',
    **params,
)
get_sport_id(sport_name: str, search_key: str = 'name', **params)
get_league_id(league_name: str, search_key: str = 'name', **params)
get_division_id(division_name: str, search_key: str = 'name', **params)
get_venue_id(venue_name: str, search_key: str = 'name', **params)
get_game(game_id: int, **params)
get_game_play_by_play(game_id: int, **params)
get_game_line_score(game_id: int, **params)
get_game_box_score(game_id: int, **params)
get_game_ids(
    date: str = None,
    start_date: str = None,
    end_date: str = None,
    sport_id: int = 1,
    **params,
)
```

`get_venue` inherits the same documented quirk as `Mlb.get_venue`: it is
annotated `Venue | None` but returns `[]` (not `None`) on a 400–499 response,
matching the sync behavior noted above. This is preserved for parity, not
introduced by the async port.

`get_game_line_score` inherits the same documented quirk as
`Mlb.get_game_line_score`: it does not short-circuit on a 400–499 status the
way its sibling game helpers do; missing linescore data falls through to an
implicit `None`.

The four stat methods return the same nested `dict` their sync counterparts
do, keyed by stat group and then by stat type — `{'hitting': {'season': Stat}}`
— and return `{}` on a 400–499 response, on a body with no `stats`, and on a
`stats` entry carrying no splits. Note that an unrecognized value in `stats` or
`groups` is not rejected; it produces the same empty `{}`. Valid values are
listed at `https://statsapi.mlb.com/api/v1/statTypes` and
`https://statsapi.mlb.com/api/v1/statGroups`.

`AsyncMlb` now covers every endpoint method `Mlb` exposes. The only public
name that differs is lifecycle: `Mlb.close()` is spelled `AsyncMlb.aclose()`.

`get_scheduled_games_by_date` inherits the same documented quirk as
`Mlb.get_scheduled_games_by_date`: it is annotated `list[ScheduleGames]` but
returns `None` when no `date`, `start_date`/`end_date` pair, or `gamePks` was
given to select with. This is preserved for parity, not introduced by the
async port.

`get_gamepace` sends the same request on both clients but builds it
differently. `Mlb` embeds the season in the endpoint string
(`gamePace?season=2021`) and relies on Requests merging that query with the
rest of the parameters. HTTPX replaces a URL's existing query rather than
merging into it, so `AsyncMlb` passes the season as an ordinary parameter.
Callers see no difference; this matters only if you are reading the two
implementations side by side.

## Low-level adapter

`MlbDataAdapter` is the public low-level HTTP adapter.

### Constructor

```text
MlbDataAdapter(
    hostname="statsapi.mlb.com",
    ver="v1",
    logger=None,
    timeout=(3.05, 30.0),
    session=None,
    *,
    strict_http=True,
)
```

Stable constructor rules:

* Parameter order above is part of the API
* Default values above are part of the API
* `strict_http` is keyword-only
* Version 1.0 defaults `strict_http` to `True`
* `ver` supports the library's documented API versions, including `v1` and
  `v1.1`

`MlbDataAdapter` exposes `get()` and `close()`. It does not implement the
context-manager protocol in version 1.0; callers should call `close()`
explicitly when they own a standalone adapter.

## Result object

```text
MlbResult(
    status_code,
    message,
    data=None,
)
```

Stable public attributes:

* `status_code` — coerced to `int`
* `message` — coerced to `str`
* `data` — a dictionary; defaults to `{}` when `data` is omitted or `None`

Stable behaviors already covered by offline tests:

* Caller-provided dictionaries are not mutated
* Each instance gets an independent `data` dictionary
* A top-level `"copyright"` key is removed from the stored `data` copy

## Retry policy

```text
create_retry_policy()
```

Stable factory contract:

* Takes no arguments
* Returns `urllib3.util.retry.Retry`
* Each call returns a new instance
* Callers may mount the returned policy on their own `requests.Session`
* The library does not automatically modify injected Sessions

Current numeric configuration (also asserted by the HTTP contract tests and
treated as stable for 1.x unless a future major release documents otherwise):

```text
total=3
connect=3
read=2
status=3
backoff_factor=0.5
status_forcelist={429, 500, 502, 503, 504}
allowed_methods={"GET"}
respect_retry_after_header=True
raise_on_status=False
```

## Exception hierarchy

```text
Exception
└── TheMlbStatsApiException
    ├── MlbTransportError
    │   └── MlbTimeoutError
    ├── MlbHttpError
    └── MlbDecodeError
```

Supported catch patterns:

* Broad package failures: `except TheMlbStatsApiException`
* Transport failures: `except MlbTransportError`
* Timeouts: `except MlbTimeoutError`
* HTTP failures: `except MlbHttpError`
* JSON decode failures: `except MlbDecodeError`

### `MlbHttpError` stable attributes

* `status_code`
* `reason`
* `url`
* `method`
* `response_data`
* `body_excerpt`

Exact `str(exc)` formatting beyond the currently tested
`"{status_code}: {reason}"` shape for `MlbHttpError` is not frozen as a broader
string-formatting promise for every exception type.

## Compatibility warning

```text
issubclass(MlbHttpCompatibilityWarning, FutureWarning)
```

remains true.

`MlbHttpCompatibilityWarning` is emitted when `strict_http=False` suppresses a
final non-404 4xx response that strict mode would raise. Warning message text
may be refined for clarity within 1.x as long as the warning class and
filtering behavior remain compatible. See [HTTP transport](http-transport.md).

## Session ownership

These ownership rules are stable public API:

```text
Library-created Session
    Owned by the library
    Receives library retry adapters
    Receives the package User-Agent
    Closed by Mlb.close(), adapter.close(), or Mlb context-manager exit

Caller-injected Session
    Owned by the caller
    Existing headers remain untouched
    Existing adapters remain untouched
    Not closed by the library
```

## Python support

| Claim | Value |
| --- | --- |
| Minimum declared Python version (`Requires-Python`) | `>=3.10` |
| CI-validated versions | 3.10, 3.11, 3.12, 3.13, 3.14 |
| Later Python versions | May work, but are not claimed as CI-validated unless added to the matrix |

The minimum declared Python version is 3.10 and the CI-validated versions are
3.10 through 3.14. Every version in that range runs the deterministic offline
suite on each pull request and push to a watched branch. Prerelease
interpreters are deliberately excluded from the required matrix and are not
claimed as supported until they reach a stable release.

Version 1.0 does not add an upper Python bound, and the declared runtime
requirement stays `>=3.10`. Adding a new interpreter is a compatible change:
extend the CI matrix and update this table in the same pull request.

## Mlb endpoint methods

The following public methods are defined directly on `Mlb`. Newly exposed
methods require an intentional update to the public API tests.

Lifecycle and context managers:

| Method | Signature notes |
| --- | --- |
| `close` | no parameters |
| `__enter__` | returns `self` |
| `__exit__` | closes only library-owned Sessions |

Endpoint methods (parameter order and defaults are part of the API):

| Method | Parameters | Top-level return shape | 404 / client-empty shape |
| --- | --- | --- | --- |
| `get_people` | `sport_id=1, **params` | `list[Person]` | `[]` |
| `get_person` | `player_id, **params` | `Person \| None` | `None` |
| `get_persons` | `person_ids, **params` | `list[Person]` | `[]` |
| `get_people_id` | `fullname, sport_id=1, search_key='fullName', **params` | `list[int]` | `[]` |
| `get_teams` | `sport_id=1, **params` | `list[Team]` | `[]` |
| `get_team` | `team_id, **params` | `Team \| None` | `None` |
| `get_team_id` | `team_name, search_key='name', **params` | `list[int]` | `[]` |
| `get_team_roster` | `team_id, **params` | `list[Player]` | `[]` |
| `get_team_coaches` | `team_id, **params` | `list[Coach]` | `[]` |
| `get_schedule` | `date=None, start_date=None, end_date=None, sport_id=1, team_id=None, **params` | `Schedule \| None` | `None` |
| `get_scheduled_games_by_date` | `date=None, start_date=None, end_date=None, sport_id=1, **params` | `list[ScheduleGames]` | `[]` |
| `get_game` | `game_id, **params` | `Game \| None` | `None` (uses `v1.1`) |
| `get_game_play_by_play` | `game_id, **params` | `Plays \| None` | `None` |
| `get_game_line_score` | `game_id, **params` | `Linescore \| None` | see notes |
| `get_game_box_score` | `game_id, **params` | `BoxScore \| None` | `None` |
| `get_game_ids` | `date=None, start_date=None, end_date=None, sport_id=1, **params` | `list[int]` | `[]` |
| `get_gamepace` | `season, sport_id=1, **params` | `GamePace \| None` | `None` |
| `get_venue` | `venue_id, **params` | annotated `Venue \| None` | returns `[]` today; see notes |
| `get_venues` | `**params` | `list[Venue]` | `[]` |
| `get_venue_id` | `venue_name, search_key='name', **params` | `list[int]` | `[]` |
| `get_sport` | `sport_id, **params` | `Sport \| None` | `None` |
| `get_sports` | `**params` | `list[Sport]` | `[]` |
| `get_sport_id` | `sport_name, search_key='name', **params` | `list[int]` | `[]` |
| `get_league` | `league_id, **params` | `League \| None` | `None` |
| `get_leagues` | `**params` | `list[League]` | `[]` |
| `get_league_id` | `league_name, search_key='name', **params` | `list[int]` | `[]` |
| `get_division` | `division_id, **params` | `Division \| None` | `None` |
| `get_divisions` | `**params` | `list[Division]` | `[]` |
| `get_division_id` | `division_name, search_key='name', **params` | `list[int]` | `[]` |
| `get_season` | `season_id, sport_id=1, **params` | annotated `Season`; may return `None` | `None` |
| `get_seasons` | `sport_id=1, **params` | `list[Season]` | `[]` |
| `get_standings` | `league_id, season, **params` | `list[Standings]` | `[]` |
| `get_attendance` | `team_id=None, league_id=None, league_list_id=None, **params` | `Attendance \| None` | `None` |
| `get_draft` | `year_id, **params` | `list[Round]` | `[]` |
| `get_awards` | `award_id, **params` | `list[Award]` | `[]` |
| `get_homerun_derby` | `game_id, **params` | `HomeRunDerby \| None` | see notes |
| `get_team_stats` | `team_id, stats, groups, **params` | `dict` | `{}` |
| `get_players_stats_for_game` | `person_id, game_id, **params` | `dict` | `{}` |
| `get_player_stats` | `person_id, stats, groups, **params` | `dict` | `{}` |
| `get_stats` | `stats, groups, **params` | `dict` | `{}` |

Notes and known conflicts (documented, not redesigned by this contract):

* Under the version 1.0 strict default, final non-404 4xx responses raise
  `MlbHttpError` before endpoint empty-shape logic runs. The empty shapes above
  remain the documented domain-level not-found / empty results for **404**
  responses (and for compatibility mode where applicable).
* `get_game_line_score` does not currently short-circuit on a 400–499 status
  the same way as sibling game helpers; missing linescore data falls through to
  an implicit `None`.
* `get_venue` is annotated to return `Venue | None` but currently returns `[]`
  on 400–499 statuses. Treat the implementation shape as the observed behavior
  until a focused fix lands.
* `get_homerun_derby` previously executed a bare `None` expression on
  400–499 instead of `return None`, so a 4xx response whose body happened to
  contain a truthy `status` key would have continued into
  `HomeRunDerby(**data)` and raised instead of returning `None`. Fixed to
  `return None` while porting the endpoint to `AsyncMlb` (issue #305).
* `get_attendance`'s "at least one of `team_id`/`league_id`/`league_list_id`"
  guard previously used `any(required_args)`, which iterates dict keys
  (always truthy) rather than values, so the guard never actually fired. This
  was fixed to `any(required_args.values())` while porting the endpoint to
  `AsyncMlb` (issue #305); calling either client with no identifier now
  returns `None` without making a request, as already documented above.
* Nested Pydantic model fields are not frozen by this contract.

## Return-contract boundaries

Version 1.0 guarantees endpoint method availability, parameter order and
defaults, top-level return types or shapes listed above, and documented 404
empty shapes.

Version 1.0 does **not** guarantee:

* Every nested model field
* Every upstream JSON property
* Undocumented behavior caused by malformed upstream data
* Exact log messages
* Exact exception string formatting beyond documented attributes
* The availability or stability of the unofficial MLB Stats API itself

## Internal APIs

The following are outside the 1.0 stability promise:

* Private names beginning with an underscore
* Internal adapter helpers such as `_configure_library_session`,
  `_build_http_error`, and `_warn_http_compatibility`
* Private `Mlb` attributes such as `_session` or `_mlb_adapter_v1`
* Exact log messages
* Exact exception string formatting beyond documented attributes
* Undocumented upstream MLB response fields
* The availability or stability of the unofficial MLB API itself
* Every symbol located in `mlbstatsapi.models` unless separately documented
* Accidentally exposed package-root submodule names listed above

Do not treat every Pydantic model field as permanently frozen.

## Legacy helpers

`return_splits` and `get_stat_attributes` remain importable from the package
root and are stable in 1.x for existing callers.

They are not the preferred entry point for new application code. Prefer the
`Mlb` statistics endpoint methods. These helpers are **not** deprecated in
version 1.0.

## Deprecation policy

No new deprecations are introduced by the version 1.0 public API audit.

A future deprecation must include:

1. A documented replacement
2. A warning strategy
3. A removal timeline
4. A separate focused issue

## Semantic-versioning expectations

After 1.0.0:

* Preserve supported package-root imports across minor and patch releases
* Prefer additive changes for new endpoints and optional parameters
* Use a major version for removals, renames, or incompatible contract changes
* Update this document when the supported surface intentionally changes
