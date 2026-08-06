# Public API Contract (1.x)

This document is the authoritative public API contract for the
`python-mlb-statsapi` **1.x** series.

It defines which package-root symbols, constructor signatures, exception and
warning relationships, Session ownership rules, and `Mlb` endpoint methods are
supported after version 1.0. Maintainers should use this document when deciding
whether a change is a patch, a minor release, or a major release.

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

### Classification of package-root symbols

| Symbol | Status |
| --- | --- |
| `Mlb` | Public and stable in 1.x |
| `MlbDataAdapter` | Public and stable in 1.x |
| `MlbResult` | Public and stable in 1.x |
| `create_retry_policy` | Public and stable in 1.x |
| `TheMlbStatsApiException` | Public and stable in 1.x |
| `MlbTransportError` | Public and stable in 1.x |
| `MlbTimeoutError` | Public and stable in 1.x |
| `MlbHttpError` | Public and stable in 1.x |
| `MlbDecodeError` | Public and stable in 1.x |
| `MlbHttpCompatibilityWarning` | Public and stable in 1.x |
| `return_splits` | Public legacy helper, stable in 1.x but not preferred for new code |
| `get_stat_attributes` | Public legacy helper, stable in 1.x but not preferred for new code |

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

## Primary client

`Mlb` is the primary synchronous client.

### Constructor

```python
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

## Low-level adapter

`MlbDataAdapter` is the public low-level HTTP adapter.

### Constructor

```python
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

```python
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

```python
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

```python
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
| Actively validated CI versions on this release branch | 3.10, 3.11, 3.12 |
| Later Python versions | May work, but are not claimed as CI-validated unless added to the matrix |

Version 1.0 does not add an upper Python bound. Absence of Python 3.13 (or
newer) CI coverage should be tracked under the release-validator / CI issue
stream rather than silently claimed here.

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
* `get_homerun_derby` currently executes a bare `None` expression on 400–499
  instead of `return None`, so execution may continue. A focused bugfix is
  recommended.
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
