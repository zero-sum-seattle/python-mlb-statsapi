<div align="center">

# Python MLB Stats API

**The Unofficial Python Wrapper for the MLB Stats API**

[![PyPI version](https://badge.fury.io/py/python-mlb-statsapi.svg)](https://badge.fury.io/py/python-mlb-statsapi)
[![Offline CI](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-mlb-statsapi)
![GitHub](https://img.shields.io/github/license/zero-sum-seattle/python-mlb-statsapi)

<div align="left">

### *Copyright Notice*  
This package and its authors are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.

###### This is an educational project - Not for commercial use. 


![MLB Stats API](https://user-images.githubusercontent.com/2068393/203456246-dfdbdf0f-1e43-4329-aaa9-1c4008f9800d.jpg)

## Getting Started

*Python-mlb-statsapi* is a Python library that provides access to the MLB Stats API, allowing developers to retrieve information related to MLB teams, players, stats, and more. Written in Python 3.10+.

All models are built with [Pydantic](https://docs.pydantic.dev/) for robust data validation and serialization. Field names follow Python's `snake_case` convention for a more Pythonic experience.

For detailed documentation, check out the [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) which contains information on return objects, endpoint structure, usage examples, and more.


<div align="center">

### [Examples](#examples) | [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) | [API](https://statsapi.mlb.com/) 

<div align="left">

## Installation
```bash
python3 -m pip install python-mlb-statsapi
```

### Python support

| Claim | Value |
| --- | --- |
| Minimum declared Python version (`Requires-Python`) | `>=3.10` |
| CI-validated versions | 3.10, 3.11, 3.12, 3.13, 3.14 |

The minimum declared Python version is 3.10 and the CI-validated versions are
3.10 through 3.14. There is no upper Python bound. Prerelease interpreters are
excluded from the required test matrix and are not claimed as supported.

## Quick Start
```python
>>> import mlbstatsapi
>>> mlb = mlbstatsapi.Mlb()

>>> mlb.get_people_id("Ty France")
[664034]

>>> player = mlb.get_person(664034)
>>> print(player.full_name)
Ty France

>>> stats = ['season', 'seasonAdvanced']
>>> groups = ['hitting']
>>> params = {'season': 2022}
>>> mlb.get_player_stats(664034, stats, groups, **params)
{'hitting': {'season': Stat, 'seasonAdvanced': Stat }}

>>> mlb.get_team_id("Seattle Mariners")
[136]

>>> team = mlb.get_team(136)
>>> print(team.name, team.franchise_name)
Seattle Mariners Seattle
```

## HTTP Sessions, Timeouts, Retries, and Error Behavior

Version 0.8.0 added shared HTTP Sessions, explicit timeouts, optional Session injection, bounded retries, and structured transport exceptions. Version 0.9.0 made that transport configurable with a public retry policy, richer `MlbHttpError` context, compatibility warnings, and a versioned User-Agent. Version 1.0.0 makes strict HTTP handling the default and documents the stable public API contract.

The `Mlb` client remains synchronous. Shared Sessions pool reusable connections; they do not cache MLB response bodies, and the client does not enable response caching by default.

For the complete reference see the [HTTP transport documentation](docs/http-transport.md). For what changed in this release see the [1.0.0 release notes](docs/releases/1.0.0.md). For the stable public API boundary see the [public API contract](docs/public-api.md).

### Upgrading to version 1.0

`Mlb()` now uses strict HTTP handling by default. It is equivalent to `Mlb(strict_http=True)`.

```text
Mlb() now uses strict HTTP handling by default
Final non-404 4xx responses raise MlbHttpError
404 keeps endpoint-specific None / [] / {} behavior
Final 5xx still raises MlbHttpError
Timeouts still raise MlbTimeoutError
Transport failures still raise MlbTransportError
Successful invalid JSON still raises MlbDecodeError
```

Recommended version 1.0 usage:

```python
import mlbstatsapi

try:
    with mlbstatsapi.Mlb() as mlb:
        player = mlb.get_person(664034)
except mlbstatsapi.MlbHttpError as exc:
    print(exc.status_code)
    print(exc.reason)
    print(exc.url)
```

Temporary compatibility opt-out while migrating:

```python
import mlbstatsapi

with mlbstatsapi.Mlb(strict_http=False) as mlb:
    player = mlb.get_person(664034)
```

`strict_http=False` is a temporary migration opt-out and an explicit request for historical 0.9 behavior. It is not the recommended long-term 1.0 configuration. See [Migrating from 0.9.x to 1.0](docs/http-transport.md#migrating-from-09x-to-10) for the full process, warning-as-error guidance, and before-and-after examples.

### Recommended context-manager usage

Prefer a context manager so library-owned HTTP resources are closed when the block exits, including when the block exits because of an exception:

```python
import mlbstatsapi

with mlbstatsapi.Mlb() as mlb:
    player = mlb.get_person(664034)
    team = mlb.get_team(136)
```

One `Mlb` client uses one shared `requests.Session`. The v1 and v1.1 adapters share that Session, so repeated requests can reuse pooled connections. A Session manages a pool of reusable connections; it is not one permanent network connection.

Callers who do not use a context manager may call `mlb.close()` instead. Repeated `close()` calls are safe. Closing a client only closes a Session the library created; a caller-injected Session is left open for its owner.

### Compatibility mode

Callers who need historical 0.9 empty-result behavior for final non-404 4xx responses can pass `strict_http=False`. That path emits `MlbHttpCompatibilityWarning` exactly once per suppressed final response, does not change 404 handling, and does not suppress final 5xx, timeout, transport, or decode failures.

The category inherits from `FutureWarning`, so it stays visible under default Python warning filters. Applications can promote only this package category to an error:

```python
import warnings
import mlbstatsapi

warnings.filterwarnings(
    "error",
    category=mlbstatsapi.MlbHttpCompatibilityWarning,
)
```

Filter on `mlbstatsapi.MlbHttpCompatibilityWarning` specifically rather than disabling all warnings or all `FutureWarning` instances, which would also hide unrelated notices from other libraries. Prefer removing `strict_http=False` and catching `MlbHttpError` over permanently ignoring the warning.

### Custom timeouts

Every request uses an explicit timeout. The defaults are:

```text
Connection timeout: 3.05 seconds
Read timeout: 30 seconds
```

The read timeout is the maximum wait while reading response data. It is not one absolute total duration for the complete request.

Use a scalar to apply the same value to both connect and read phases:

```python
import mlbstatsapi

with mlbstatsapi.Mlb(timeout=10) as mlb:
    player = mlb.get_person(664034)
```

Or provide separate connection and read timeouts:

```python
import mlbstatsapi

with mlbstatsapi.Mlb(
    timeout=(5.0, 60.0),
) as mlb:
    player = mlb.get_person(664034)
```

```text
5.0 seconds: connection timeout
60.0 seconds: read timeout
```

### Injecting a custom Session

Advanced callers may inject a caller-owned Session:

```python
import requests
import mlbstatsapi

session = requests.Session()
session.headers.update({
    "User-Agent": "my-baseball-project/1.0",
})

try:
    with mlbstatsapi.Mlb(session=session) as mlb:
        player = mlb.get_person(664034)
finally:
    session.close()
```

Ownership rules:

```text
Library-created Session
    The library configures and closes it
Caller-injected Session
    The caller configures and closes it
```

`Mlb.close()` does not close a caller-injected Session, and exiting `with Mlb(session=session)` does not close the injected Session either. The library does not replace or reconfigure adapters or headers on an injected Session. Callers control custom retry, TLS, proxy, header, and adapter configuration.

### Reusing the retry policy on a caller-managed Session

`create_retry_policy()` remains public. It returns a new instance of the same tested policy the library mounts on Sessions it creates, so a caller-managed Session can opt in to identical retry behavior:

```python
import requests
import mlbstatsapi

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    max_retries=mlbstatsapi.create_retry_policy(),
)
session.mount("https://", adapter)
session.mount("http://", adapter)

try:
    with mlbstatsapi.Mlb(session=session) as mlb:
        player = mlb.get_person(664034)
finally:
    session.close()
```

* The caller mounts the adapters
* The caller closes the injected Session
* The library never reconfigures an injected Session

### Versioned User-Agent

A Session created by the library sends a package-specific User-Agent:

```text
python-mlb-statsapi/<installed-version>
```

For this release's currently declared package metadata that resolves to `python-mlb-statsapi/1.0.1`. The version is read from the installed distribution metadata, so it always matches the installed release. Only the `User-Agent` header is set; other Requests defaults such as `Accept-Encoding` remain intact, and the header carries no identifiers beyond the package name and version.

Headers on a caller-injected Session are left untouched, so applications that set their own User-Agent keep it.

### Structured exception handling

```python
import mlbstatsapi

try:
    with mlbstatsapi.Mlb() as mlb:
        player = mlb.get_person(664034)
except mlbstatsapi.MlbTimeoutError:
    print("The MLB API timed out")
except mlbstatsapi.MlbTransportError:
    print("The request could not reach the MLB API")
except mlbstatsapi.MlbHttpError as exc:
    print(exc.method)
    print(exc.status_code)
    print(exc.reason)
    print(exc.url)
    print(exc.response_data)
    print(exc.body_excerpt)
except mlbstatsapi.MlbDecodeError:
    print("The MLB API returned invalid JSON")
```

* `MlbTimeoutError` represents connection and read timeouts
* `MlbTransportError` represents other request transport failures
* `MlbHttpError` represents an unexpected final HTTP response
* `MlbDecodeError` represents invalid JSON in a successful response

`MlbHttpError` exposes `method`, `status_code`, `reason`, `url`, `response_data`, and `body_excerpt`. `response_data` holds the decoded JSON dictionary or list when the error body contains one, and is `None` otherwise. `body_excerpt` is a bounded excerpt of the response text, capped at 500 characters. Complete response bodies are never automatically logged, and `str(exc)` stays concise.

### Backward-compatible exception handling

All new transport exceptions inherit from `TheMlbStatsApiException`, so existing broad exception handling remains compatible:

```python
import mlbstatsapi

try:
    with mlbstatsapi.Mlb() as mlb:
        player = mlb.get_person(664034)
except mlbstatsapi.TheMlbStatsApiException:
    print("The MLB request failed")
```

### Default retry behavior

Library-created Sessions automatically retry temporary GET failures for:

```text
429
500
502
503
504
```

```text
Initial request: 1
Maximum retries: 3
Maximum total attempts: 4
Backoff factor: 0.5
Retry-After respected: yes
```

Only GET requests are retried, and retries are bounded. Ordinary client errors such as 400, 401, 403, and 404 are not retried. Invalid JSON and Pydantic validation failures are not retried. Retries improve resilience for transient failures, but they do not guarantee success. The retry values are unchanged from versions 0.8.0 and 0.9.0. The version 1.0 strict default does not change retry or Session behavior.

### Existing 404 compatibility

Version 1.0.0 preserves existing endpoint-specific not-found behavior under both the default and `strict_http=False`. Depending on the endpoint, a 404 may still produce:

```text
None
[]
{}
```

Not every 404 raises `MlbHttpError`, and the strict default does not change that.

### HTTP behavior at a glance

| Final response | Default 1.0 behavior | Explicit compatibility mode |
| -------------- | -------------------- | --------------------------- |
| Successful 2xx | Normal result | Normal result |
| Non-404 4xx | `MlbHttpError` | Warning and historical empty result |
| 404 | Existing endpoint behavior | Existing endpoint behavior |
| Final 429 | `MlbHttpError` after retries | Warning and historical empty result after retries |
| Final 5xx | `MlbHttpError` | `MlbHttpError` |

See the [HTTP transport documentation](docs/http-transport.md) for the complete retry policy, Session ownership rules, warning behavior, cleanup behavior, and migration guidance, and the [1.0.0 release notes](docs/releases/1.0.0.md) for the release summary.

## Working with Pydantic Models

All returned objects are Pydantic models, giving you access to powerful serialization and validation features.

### Convert to Dictionary
```python
>>> player = mlb.get_person(664034)
>>> player.model_dump()
{'id': 664034, 'full_name': 'Ty France', 'link': '/api/v1/people/664034', ...}

# Exclude None values
>>> player.model_dump(exclude_none=True)
{'id': 664034, 'full_name': 'Ty France', 'link': '/api/v1/people/664034', ...}

# Include only specific fields
>>> player.model_dump(include={'id', 'full_name', 'primary_position'})
{'id': 664034, 'full_name': 'Ty France', 'primary_position': Position(...)}
```

### Convert to JSON
```python
>>> player = mlb.get_person(664034)
>>> player.model_dump_json()
'{"id": 664034, "full_name": "Ty France", "link": "/api/v1/people/664034", ...}'

# Pretty print with indentation
>>> print(player.model_dump_json(indent=2))
{
  "id": 664034,
  "full_name": "Ty France",
  "link": "/api/v1/people/664034",
  ...
}
```

### Access Fields with Snake Case Names
```python
>>> player = mlb.get_person(664034)
>>> player.full_name          # Not fullName
'Ty France'
>>> player.primary_position   # Not primaryPosition
Position(code='3', name='First Base', ...)
>>> player.bat_side           # Not batSide  
CodeDesc(code='R', description='Right')
```

## Documentation

### [People, Person, Players, Coaches](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-People)
* `Mlb.get_people_id(self, fullname: str, sport_id: int = 1, search_key: str = 'fullname', **params)` - Return Person Id(s) from fullname
* `Mlb.get_person(self, player_id: int, **params)` - Return Person Object from Id
* `Mlb.get_people(self, sport_id: int = 1, **params)` - Return all Players from Sport
### [Draft](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Draft(round))
* `Mlb.get_draft(self, year_id: int, **params)` - Return a draft for a given year
### [Awards](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Award)
* `Mlb.get_awards(self, award_id: int, **params)` - Return award recipients for a given award
### [Teams](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Team)
* `Mlb.get_team_id(self, team_name: str, search_key: str = 'name', **params)` - Return Team Id(s) from name
* `Mlb.get_team(self, team_id: int, **params)` - Return Team Object from Team Id
* `Mlb.get_teams(self, sport_id: int = 1, **params)` - Return all Teams for Sport
* `Mlb.get_team_coaches(self, team_id: int, **params)` - Return coaching roster for team for current or specified season
* `Mlb.get_team_roster(self, team_id: int, **params)` - Return player roster for team for current or specified season
### [Stats](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Stats)
* `Mlb.get_player_stats(self, person_id: int, stats: list, groups: list, **params)` - Return stats by player id, stat type and groups
* `Mlb.get_team_stats(self, team_id: int, stats: list, groups: list, **params)` - Return stats by team id, stat types and groups
* `Mlb.get_stats(self, stats: list, groups: list, **params: dict)` - Return stats by stat type and group args
* `Mlb.get_players_stats_for_game(self, person_id: int, game_id: int, **params)` - Return player stats for a game
### [Gamepace](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Gamepace)
* `Mlb.get_gamepace(self, season: str, sport_id=1, **params)` - Return pace of game metrics for specific sport, league or team.
### [Venues](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Venue)
* `Mlb.get_venue_id(self, venue_name: str, search_key: str = 'name', **params)` - Return Venue Id(s)
* `Mlb.get_venue(self, venue_id: int, **params)` - Return Venue Object from venue Id
* `Mlb.get_venues(self, **params)` - Return all Venues
### [Sports](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Sport)
* `Mlb.get_sport(self, sport_id: int, **params)` - Return a Sport object from Id
* `Mlb.get_sports(self, **params)` - Return all Sports
* `Mlb.get_sport_id(self, sport_name: str, search_key: str = 'name', **params)`- Return Sport Id from name
### [Schedules](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Schedule)
* `Mlb.get_schedule(self, date: str, start_date: str, end_date: str, sport_id: int, team_id: int, **params)` - Return a Schedule
### [Divisions](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Division)
* `Mlb.get_division(self, division_id: int, **params)` - Return a Division 
* `Mlb.get_divisions(self, **params)` - Return all Divisions
* `Mlb.get_division_id(self, division_name: str, search_key: str = 'name', **params)` - Return Division Id(s) from name
### [Leagues](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-League)
* `Mlb.get_league(self, league_id: int, **params)` - Return a League from Id
* `Mlb.get_leagues(self, **params)` - Return all Leagues
* `Mlb.get_league_id(self, league_name: str, search_key: str = 'name', **params)` - Return League Id(s)
### [Seasons](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Season)
* `Mlb.get_season(self, season_id: str, sport_id: int = None, **params)` - Return a season
* `Mlb.get_seasons(self, sportid: int = None, **params)` - Return all seasons
### [Standings](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Standings)
* `Mlb.get_standings(self, league_id: int, season: str, **params)` - Return standings
### [Schedules](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Schedule)
* `Mlb.get_schedule(self, date: str = None, start_date: str = None, end_date: str = None, sport_id: int = 1, team_id: int = None, **params)` - Return a Schedule from dates
* `Mlb.get_scheduled_games_by_date(self, date: str = None,start_date: str = None, end_date: str = None, sport_id: int = 1, **params)` - Return game ids from dates
### [Games](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Game)
* `Mlb.get_game(self, game_id: int, **params)` - Return the Game for a specific Game Id
* `Mlb.get_game_play_by_play(self, game_id: int, **params)` - Return Play by play data for a game
* `Mlb.get_game_line_score(self, game_id: int, **params)` - Return a Linescore for a game
* `Mlb.get_game_box_score(self, game_id: int, **params)` - Return a Boxscore for a game


## Contributing

Contributions are welcome! Whether it's bug fixes, new features, or documentation improvements, we appreciate your help.

### Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/python-mlb-statsapi.git`
3. Install dependencies: `poetry install`
4. Create a branch: `git checkout -b feat/your-feature`

### Development

Offline tests are deterministic and should run before every pull request:

```bash
poetry run pytest \
  tests/ \
  --ignore=tests/external_tests
```

External tests contact the live MLB API. They require internet access and are separate from normal offline CI:

```bash
poetry run pytest \
  tests/external_tests/
```

These live tests may fail because the MLB service is unavailable or because MLB changes undocumented payloads.

Full local validation:

```bash
poetry run pytest tests/
rm -rf dist
poetry build
python3 scripts/validate_release.py
poetry run twine check dist/*
```

`scripts/validate_release.py` is the same release check offline CI runs. It inspects the built wheel and source distribution, clean-installs each artifact into its own temporary virtual environment, and runs the same public-API smoke test against both installed artifacts. The smoke test verifies the declared metadata, the supported package-root imports, the strict HTTP default, explicit strict and compatibility modes, the versioned `User-Agent`, and injected-Session ownership. Every response it observes comes from an injected fake Session, so it never contacts the MLB API.

Offline CI is the normal pull-request gate. External tests are available manually, on a weekly schedule, and before releases.

### Pull Request Guidelines

- Run offline tests before submitting a PR
- Use the [PR template](.github/pull_request_template.md) when creating your pull request
- Follow the branch naming convention:
  - `feat/` - New features
  - `fix/` - Bug fixes
  - `docs/` - Documentation updates
  - `refactor/` - Code improvements

### Reporting Issues

Found a bug or have a feature request? Please [open an issue](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues/new) with:

- A clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Python version and package version


## Examples

Let's show some examples of getting stat objects from the API. What is baseball without stats, right?

### Player Stats
Get the Id(s) of the players you want stats for and set stat types and groups.
```python
>>> mlb = mlbstatsapi.Mlb()
>>> player_id = mlb.get_people_id("Ty France")[0]
>>> stats = ['season', 'career']
>>> groups = ['hitting', 'pitching']
>>> params = {'season': 2022}
```

Use player id with stat types and groups to return a stats dictionary
```python
>>> stat_dict = mlb.get_player_stats(player_id, stats=stats, groups=groups, **params)
>>> season_hitting_stat = stat_dict['hitting']['season']
>>> career_pitching_stat = stat_dict['pitching']['career']
```

Print season hitting stats using Pydantic's `model_dump()`
```python
>>> for split in season_hitting_stat.splits:
...     print(split.stat.model_dump(exclude_none=True))
{'games_played': 140, 'groundouts': 163, 'airouts': 148, 'runs': 65, 'doubles': 27, ...}
```

Or access individual fields directly
```python
>>> for split in season_hitting_stat.splits:
...     print(f"Games: {split.stat.games_played}")
...     print(f"Home Runs: {split.stat.home_runs}")
...     print(f"Batting Avg: {split.stat.avg}")
Games: 140
Home Runs: 20
Batting Avg: .274
```

### Team Stats
Get the Team Id(s)
```python
>>> mlb = mlbstatsapi.Mlb()
>>> team_id = mlb.get_team_id('Seattle Mariners')[0]
```

Set the stat types and groups
```python
>>> stats = ['season', 'seasonAdvanced']
>>> groups = ['hitting']
>>> params = {'season': 2022}
```

Use team id and the stat types and groups to return season hitting stats
```python
>>> stats = mlb.get_team_stats(team_id, stats=stats, groups=groups, **params)
>>> season_hitting = stats['hitting']['season']
>>> advanced_hitting = stats['hitting']['seasonAdvanced']
```

Print stats as JSON
```python
>>> for split in season_hitting.splits:
...     print(split.stat.model_dump_json(indent=2, exclude_none=True))
{
  "games_played": 162,
  "groundouts": 1273,
  "runs": 690,
  "doubles": 229,
  ...
}
```

### Expected Stats
```python
>>> player_id = mlb.get_people_id('Ty France')[0]
>>> stats = ['expectedStatistics']
>>> group = ['hitting']
>>> params = {'season': 2022}

>>> stats = mlb.get_player_stats(player_id, stats=stats, groups=group, **params)
>>> expected = stats['hitting']['expectedStatistics']
>>> for split in expected.splits:
...     print(f"Expected AVG: {split.stat.avg}")
...     print(f"Expected SLG: {split.stat.slg}")
Expected AVG: .259
Expected SLG: .394
```

### vsPlayer Stats
Get pitcher and batter player Ids
```python
>>> ty_france_id = mlb.get_people_id('Ty France')[0]
>>> shohei_ohtani_id = mlb.get_people_id('Shohei Ohtani')[0]
```

Set stat type, stat groups, and params
```python
>>> stats = ['vsPlayer']
>>> group = ['hitting']
>>> params = {'opposingPlayerId': shohei_ohtani_id, 'season': 2022}
```

Get stats
```python
>>> stats = mlb.get_player_stats(ty_france_id, stats=stats, groups=group, **params)
>>> vs_player = stats['hitting']['vsPlayer']
>>> for split in vs_player.splits:
...     print(f"Games: {split.stat.games_played}, Hits: {split.stat.hits}")
Games: 2, Hits: 2
```

### Hot/Cold Zones
```python
>>> ty_france_id = mlb.get_people_id('Ty France')[0]
>>> stats = ['hotColdZones']
>>> hitting_group = ['hitting']
>>> params = {'season': 2022}

>>> hotcoldzones = mlb.get_player_stats(ty_france_id, stats=stats, groups=hitting_group, **params)
>>> zones = hotcoldzones['stats']['hotColdZones']

>>> for split in zones.splits:
...     print(f"Stat: {split.stat.name}")
...     for zone in split.stat.zones:
...         print(f"  Zone {zone.zone}: {zone.value}")
Stat: battingAverage
  Zone 01: .226
  Zone 02: .400
  ...
```

### Schedule Examples
Get a schedule for a given date
```python
>>> mlb = mlbstatsapi.Mlb()
>>> schedule = mlb.get_schedule(date='2022-10-13')
>>> dates = schedule.dates

>>> for date in dates:
...     for game in date.games:
...         print(f"Game: {game.game_pk}")
...         print(f"Status: {game.status.detailed_state}")
...         print(f"Home: {game.teams.home.team.name}")
...         print(f"Away: {game.teams.away.team.name}")
```

### Game Examples
Get a Game for a given game id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> game = mlb.get_game(662242)
```

Get the weather for a game
```python
>>> weather = game.game_data.weather
>>> print(f"Condition: {weather.condition}")
>>> print(f"Temperature: {weather.temp}")
>>> print(f"Wind: {weather.wind}")
```

Get the current status of a game
```python
>>> linescore = game.live_data.linescore
>>> home_info = game.game_data.teams.home
>>> away_info = game.game_data.teams.away
>>> home_status = linescore.teams.home
>>> away_status = linescore.teams.away

>>> print(f"Home: {home_info.franchise_name} {home_info.club_name}")
>>> print(f"  Runs: {home_status.runs}, Hits: {home_status.hits}, Errors: {home_status.errors}")
>>> print(f"Away: {away_info.franchise_name} {away_info.club_name}")
>>> print(f"  Runs: {away_status.runs}, Hits: {away_status.hits}, Errors: {away_status.errors}")
>>> print(f"Inning: {linescore.inning_half} {linescore.current_inning_ordinal}")
```

Get play by play, line score, and box score objects
```python
>>> play_by_play = game.live_data.plays
>>> line_score = game.live_data.linescore
>>> box_score = game.live_data.boxscore
```

#### Play by Play
Get only the play by play for a given game id
```python
>>> playbyplay = mlb.get_game_play_by_play(662242)
```

#### Line Score
Get only the line score for a given game id
```python
>>> linescore = mlb.get_game_line_score(662242)
```

#### Box Score
Get only the box score for a given game id
```python
>>> boxscore = mlb.get_game_box_score(662242)
```

### Gamepace Examples
Get pace of game metrics for a specific season
```python
>>> mlb = mlbstatsapi.Mlb()
>>> gamepace = mlb.get_gamepace(season=2021)
>>> print(f"Hits per game: {gamepace.sports[0].sport_game_pace.hits_per_game}")
```

### People Examples
Get all Players for a given sport id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> players = mlb.get_people(sport_id=1)
>>> for player in players:
...     print(f"{player.id}: {player.full_name}")
```

Get a player id
```python
>>> player_id = mlb.get_people_id("Ty France")
>>> print(player_id[0])
664034
```

### Team Examples
Get a Team
```python
>>> mlb = mlbstatsapi.Mlb()
>>> team_id = mlb.get_team_id("Seattle Mariners")[0]
>>> team = mlb.get_team(team_id)
>>> print(f"{team.id}: {team.name}")
>>> print(f"Venue: {team.venue.name}")
```

Get a Player Roster
```python
>>> mlb = mlbstatsapi.Mlb()
>>> players = mlb.get_team_roster(136)
>>> for player in players:
...     print(f"#{player.jersey_number} {player.person.full_name}")
```

Get a Coach Roster
```python
>>> mlb = mlbstatsapi.Mlb()
>>> coaches = mlb.get_team_coaches(136)
>>> for coach in coaches:
...     print(f"{coach.person.full_name}: {coach.title}")
```

### Draft Examples
Get a draft for a year
```python
>>> mlb = mlbstatsapi.Mlb()
>>> draft = mlb.get_draft('2019')
```

Get Players from Draft
```python
>>> draftpicks = draft[0].picks
>>> for pick in draftpicks:
...     print(f"Round {pick.pick_round}, Pick {pick.pick_number}: {pick.person.full_name}")
```

### Award Examples
Get awards for a given award id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> retired_numbers = mlb.get_awards(award_id='RETIREDUNI_108')
>>> for recipient in retired_numbers.awards:
...     print(f"{recipient.player.full_name}: {recipient.name} ({recipient.date})")
```

### Venue Examples
Get a Venue
```python
>>> mlb = mlbstatsapi.Mlb()
>>> venue_id = mlb.get_venue_id('PNC Park')[0]
>>> venue = mlb.get_venue(venue_id)
>>> print(f"{venue.name} - {venue.location.city}, {venue.location.state}")
```

### Division Examples
Get a division
```python
>>> mlb = mlbstatsapi.Mlb()
>>> division = mlb.get_division(200)
>>> print(division.name)
American League West
```

### League Examples
Get a league
```python
>>> mlb = mlbstatsapi.Mlb()
>>> league = mlb.get_league(103)
>>> print(league.name)
American League
```

### Season Examples
Get a Season
```python
>>> mlb = mlbstatsapi.Mlb()
>>> season = mlb.get_season(2018)
>>> print(f"Season: {season.season_id}")
>>> print(f"Regular Season: {season.regular_season_start_date} to {season.regular_season_end_date}")
```

### Standings Examples
Get Standings
```python
>>> mlb = mlbstatsapi.Mlb()
>>> standings = mlb.get_standings(103, 2018)
>>> for record in standings:
...     print(f"Division: {record.division.name}")
...     for team in record.team_records:
...         print(f"  {team.team.name}: {team.wins}-{team.losses}")
```
