<div align="center">

# Python MLB Stats API

**The Unofficial Python Wrapper for the MLB Stats API**

[![PyPI version](https://badge.fury.io/py/python-mlb-statsapi.svg)](https://badge.fury.io/py/python-mlb-statsapi)
[![Offline CI](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-mlb-statsapi)
![GitHub](https://img.shields.io/github/license/zero-sum-seattle/python-mlb-statsapi)

</div>

### *Copyright Notice*

This package and its authors are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.

###### This is an educational project - Not for commercial use.

![MLB Stats API](https://user-images.githubusercontent.com/2068393/203456246-dfdbdf0f-1e43-4329-aaa9-1c4008f9800d.jpg)

## Getting Started

`python-mlb-statsapi` provides Python access to the MLB Stats API for teams, players, schedules, games, stats, and more.

Returned objects are built with [Pydantic](https://docs.pydantic.dev/), and model fields use Python `snake_case` names.

Version 1.1.0 adds first-class async support through `AsyncMlb` while keeping the existing synchronous `Mlb` API available without changes.

[Examples](#examples) | [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) | [Public API](docs/public-api.md) | [MLB Stats API](https://statsapi.mlb.com/)

## Installation

### Synchronous client

```bash
python3 -m pip install python-mlb-statsapi
```

### Async support

Install the optional `async` extra to use `AsyncMlb` and `AsyncMlbDataAdapter`:

```bash
python3 -m pip install "python-mlb-statsapi[async]"
```

The async extra installs HTTPX. Python 3.10 or newer is required.

### Python support

| Claim | Value |
| --- | --- |
| Minimum Python version | `>=3.10` |
| CI-validated versions | 3.10, 3.11, 3.12, 3.13, 3.14 |

## Quick Start

### Sync

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    player = mlb.get_person(664034)
    team = mlb.get_team(136)

print(player.full_name)
print(team.name)
```

### Async

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        player = await mlb.get_person(664034)
        team = await mlb.get_team(136)

        print(player.full_name)
        print(team.name)


asyncio.run(main())
```

### Concurrent async requests

`AsyncMlb` supports concurrent requests on the same event loop. Concurrency is caller-controlled.

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        player, team = await asyncio.gather(
            mlb.get_person(664034),
            mlb.get_team(136),
        )

        print(player.full_name)
        print(team.name)


asyncio.run(main())
```

`AsyncMlb` does not create hidden background tasks or automatic request fanout.

## Sync or Async?

| | `Mlb` | `AsyncMlb` |
| --- | --- | --- |
| HTTP library | Requests | HTTPX |
| Context manager | `with Mlb()` | `async with AsyncMlb()` |
| Request | `mlb.get_team(...)` | `await mlb.get_team(...)` |
| Explicit cleanup | `mlb.close()` | `await mlb.aclose()` |

Where an async endpoint is supported, both clients return the same Pydantic models and follow the same public HTTP/error behavior.

Async endpoint coverage is expanding in v1.1.0. See the [public API contract](docs/public-api.md) for the current supported async methods.

## HTTP Behavior

Both clients use explicit timeouts, bounded retries for temporary failures, structured exceptions, and pooled HTTP connections.

Library-created HTTP resources are configured and closed by the library. Caller-injected Requests Sessions or HTTPX clients remain caller-owned and are not closed or reconfigured by the library.

`strict_http=True` is the default. Final non-404 4xx responses raise `MlbHttpError`, while existing endpoint-specific 404 behavior is preserved.

The main transport exceptions are:

- `MlbHttpError`
- `MlbTimeoutError`
- `MlbTransportError`
- `MlbDecodeError`

Example:

```python
from mlbstatsapi import Mlb, MlbHttpError, MlbTimeoutError

try:
    with Mlb() as mlb:
        player = mlb.get_person(664034)
except MlbTimeoutError:
    print("The MLB API timed out")
except MlbHttpError as exc:
    print(exc.status_code, exc.reason)
```

For retry policy, timeouts, compatibility mode, custom Sessions, ownership rules, and migration guidance, see the [HTTP transport documentation](docs/http-transport.md).

For the supported 1.x API surface and async endpoint list, see the [public API contract](docs/public-api.md).

## Working with Pydantic Models

All returned model objects use Pydantic.

### Convert to a dictionary

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    player = mlb.get_person(664034)

print(player.model_dump(exclude_none=True))
```

### Convert to JSON

```python
print(player.model_dump_json(indent=2))
```

### Snake case fields

MLB response names are converted to Python-style field names:

```python
print(player.full_name)          # not fullName
print(player.primary_position)   # not primaryPosition
print(player.bat_side)           # not batSide
```

## Examples

### Find a player or team

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    player_id = mlb.get_people_id("Ty France")[0]
    team_id = mlb.get_team_id("Seattle Mariners")[0]

    player = mlb.get_person(player_id)
    team = mlb.get_team(team_id)

print(player.full_name)
print(team.name)
```

### Schedule

Sync:

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    schedule = mlb.get_schedule(date="2022-10-13")
```

Async:

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        schedule = await mlb.get_schedule(date="2022-10-13")
        return schedule


schedule = asyncio.run(main())
```

### Game data

Sync:

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    game = mlb.get_game(662242)
    play_by_play = mlb.get_game_play_by_play(662242)
    line_score = mlb.get_game_line_score(662242)
    box_score = mlb.get_game_box_score(662242)
```

Async:

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        game, play_by_play, line_score, box_score = await asyncio.gather(
            mlb.get_game(662242),
            mlb.get_game_play_by_play(662242),
            mlb.get_game_line_score(662242),
            mlb.get_game_box_score(662242),
        )

        return game, play_by_play, line_score, box_score


results = asyncio.run(main())
```

### Player stats

The higher-level stats helpers remain on the synchronous `Mlb` client in v1.1.0.

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    player_id = mlb.get_people_id("Ty France")[0]
    stats = mlb.get_player_stats(
        player_id,
        stats=["season", "career"],
        groups=["hitting"],
        season=2022,
    )

season = stats["hitting"]["season"]
for split in season.splits:
    print(split.stat.model_dump(exclude_none=True))
```

### Team roster

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    players = mlb.get_team_roster(136)

for player in players:
    print(f"#{player.jersey_number} {player.person.full_name}")
```

The same roster endpoint is also available through `AsyncMlb`:

```python
players = await mlb.get_team_roster(136)
```

## Documentation

- [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) - endpoint and model documentation
- [Public API contract](docs/public-api.md) - supported package API and async endpoint coverage
- [HTTP transport](docs/http-transport.md) - retries, timeouts, errors, ownership, and compatibility behavior
- [Release notes](docs/releases/) - release-specific changes and migration notes

## Contributing

Contributions, bug fixes, tests, and documentation improvements are welcome.

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/python-mlb-statsapi.git
cd python-mlb-statsapi
poetry install -E async
```

### Tests

Offline tests are deterministic and should run before every pull request:

```bash
poetry run pytest tests/ --ignore=tests/external_tests
```

External tests contact the live MLB API and are kept separate from normal offline CI:

```bash
poetry run pytest tests/external_tests/
```

Full local validation:

```bash
poetry run pytest tests/
rm -rf dist
poetry build
python3 scripts/validate_release.py
poetry run twine check dist/*
```

Live tests may fail when the MLB service is unavailable or when MLB changes undocumented payloads.

### Pull requests

- Run offline tests before submitting a PR
- Use the [PR template](.github/pull_request_template.md)
- Keep changes focused and reviewable

Suggested branch prefixes:

- `feat/` - new features
- `fix/` - bug fixes
- `docs/` - documentation
- `refactor/` - code improvements

### Reporting issues

Found a bug or have a feature request? [Open an issue](https://github.com/zero-sum-seattle/python-mlb-statsapi/issues/new) and include:

- A clear description
- Steps to reproduce when reporting a bug
- Expected and actual behavior
- Python and package versions
