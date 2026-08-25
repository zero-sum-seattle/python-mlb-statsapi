<div align="center">

# Python MLB Stats API

**The Unofficial Python Wrapper for the MLB Stats API**

[![PyPI version](https://badge.fury.io/py/python-mlb-statsapi.svg)](https://badge.fury.io/py/python-mlb-statsapi)
[![Offline CI](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-mlb-statsapi)
![GitHub](https://img.shields.io/github/license/zero-sum-seattle/python-mlb-statsapi)

### [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) | [Methods](docs/methods.md) | [Examples](docs/examples.md) | [Stats](docs/stats.md) | [Async](docs/async.md) | [Public API](docs/public-api.md) | [MLB Stats API](https://statsapi.mlb.com/)

</div>

`python-mlb-statsapi` provides Python access to the MLB Stats API for teams, players, schedules, games, stats, and more.

Returned objects are built with [Pydantic](https://docs.pydantic.dev/), and model fields use Python `snake_case` names.

Version 1.1 adds first-class async support through `AsyncMlb` while keeping the existing synchronous `Mlb` API available without code changes for sync users.

### Copyright Notice

This package and its authors are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.

###### This is an educational project - Not for commercial use.

![MLB Stats API](https://user-images.githubusercontent.com/2068393/203456246-dfdbdf0f-1e43-4329-aaa9-1c4008f9800d.jpg)

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

| Claim | Value |
| --- | --- |
| Minimum Python version | `>=3.10` |
| CI-validated versions | Python 3.10 through 3.14 |

See [Python support](docs/public-api.md#python-support) for the complete policy.

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

### Without a context manager

Context managers are recommended, but both clients can also be created directly. When doing that, close library-owned HTTP resources explicitly.

#### Sync

```python
from mlbstatsapi import Mlb

mlb = Mlb()
try:
    player = mlb.get_person(664034)
    team = mlb.get_team(136)

    print(player.full_name)
    print(team.name)
finally:
    mlb.close()
```

#### Async

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    mlb = AsyncMlb()
    try:
        player = await mlb.get_person(664034)
        team = await mlb.get_team(136)

        print(player.full_name)
        print(team.name)
    finally:
        await mlb.aclose()


asyncio.run(main())
```

See [Async usage](docs/async.md) for lifecycle, concurrency, custom HTTPX clients, and the current async endpoint list.

## Sync or Async?

| | `Mlb` | `AsyncMlb` |
| --- | --- | --- |
| HTTP library | Requests | HTTPX |
| Context manager | `with Mlb()` | `async with AsyncMlb()` |
| Request | `mlb.get_team(...)` | `await mlb.get_team(...)` |
| Explicit cleanup | `mlb.close()` | `await mlb.aclose()` |

`AsyncMlb` mirrors the full endpoint surface of `Mlb`. Both clients return the same Pydantic models and follow the same public HTTP/error behavior.

See the [public API contract](docs/public-api.md#asyncmlb-public-client) for the authoritative method list and signatures.

## Concurrent Async Requests

`AsyncMlb` supports concurrent requests on the same event loop. Concurrency is controlled by the caller.

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        player, team = await asyncio.gather(
            mlb.get_person(664034),
            mlb.get_team(136),
        )

        return player, team


player, team = asyncio.run(main())
```

`AsyncMlb` does not create hidden background tasks or automatic request fanout.

## Common Methods

The examples below assume an initialized `Mlb` client named `mlb`, as shown in [Quick Start](#quick-start).

### Players

```python
player = mlb.get_person(664034)
players = mlb.get_people()
player_ids = mlb.get_people_id("Ty France")
```

### Teams

```python
team = mlb.get_team(136)
teams = mlb.get_teams()
team_ids = mlb.get_team_id("Seattle Mariners")
```

### Stats

The stats API has several entry points and returns a nested `stats[group][type]` structure. See the dedicated [Stats Guide](docs/stats.md) for `get_player_stats()`, `get_team_stats()`, `get_stats()`, and `get_players_stats_for_game()` examples using both `Mlb` and `AsyncMlb`.

### Schedule

```python
schedule = mlb.get_schedule(date="2022-10-13")
```

See the [method reference](docs/methods.md) for the full method documentation that previously lived in the README. Longer runnable examples live in [docs/examples.md](docs/examples.md).

## HTTP and Error Behavior

Both clients use explicit timeouts, structured exceptions, and pooled HTTP connections. `strict_http=True` is the default. Final non-404 4xx responses raise `MlbHttpError`, while existing endpoint-specific 404 behavior is preserved.

Library-created clients send a versioned User-Agent. The current package version sends `python-mlb-statsapi/1.0.1`. See the [HTTP transport documentation](docs/http-transport.md) for the full transport contract.

The main transport exceptions are:

* `MlbHttpError`
* `MlbTimeoutError`
* `MlbTransportError`
* `MlbDecodeError`

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

For timeouts, retries, compatibility mode, ownership rules, and transport details, see [docs/http-transport.md](docs/http-transport.md).

## Working with Models

Every returned model object uses Pydantic and Python-style `snake_case` fields:

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    player = mlb.get_person(664034)

print(player.full_name)                     # not fullName
print(player.model_dump(exclude_none=True))
print(player.model_dump_json(indent=2))
```

## Documentation

| Document | Contents |
| --- | --- |
| [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) | Endpoint reference, return objects, and model documentation |
| [Method reference](docs/methods.md) | Method signatures and short descriptions from the original README reference |
| [Usage examples](docs/examples.md) | Extended synchronous examples |
| [Stats guide](docs/stats.md) | Player, team, general, and per-game stat queries with sync and async examples |
| [Async usage](docs/async.md) | Async installation, lifecycle, concurrency, and examples |
| [HTTP transport](docs/http-transport.md) | Timeouts, retries, strict HTTP, exceptions, and ownership |
| [Public API contract](docs/public-api.md) | Supported symbols, signatures, endpoint methods, and stability policy |
| [Release notes](docs/releases/) | Release-specific changes and migration notes |

## Contributing

Contributions, bug fixes, tests, and documentation improvements are welcome.

```bash
git clone https://github.com/YOUR_USERNAME/python-mlb-statsapi.git
cd python-mlb-statsapi
poetry install -E async
```

Run the deterministic offline suite before a pull request:

```bash
poetry run pytest tests/ --ignore=tests/external_tests
```

External tests contact the live MLB API and are separate from normal offline CI:

```bash
poetry run pytest tests/external_tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full development and pull request workflow.

## License

Released under the [MIT License](LICENSE).
