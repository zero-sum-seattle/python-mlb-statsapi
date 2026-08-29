<div align="center">

# Python MLB Stats API

**The Unofficial Python Wrapper for the MLB Stats API**

[![PyPI version](https://badge.fury.io/py/python-mlb-statsapi.svg)](https://badge.fury.io/py/python-mlb-statsapi)
[![Offline CI](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-mlb-statsapi)
![GitHub](https://img.shields.io/github/license/zero-sum-seattle/python-mlb-statsapi)

### [Docs](https://zero-sum-seattle.github.io/python-mlb-statsapi/) | [Methods](https://zero-sum-seattle.github.io/python-mlb-statsapi/methods/) | [Examples](https://zero-sum-seattle.github.io/python-mlb-statsapi/examples/) | [Stats](https://zero-sum-seattle.github.io/python-mlb-statsapi/stats/) | [Async](https://zero-sum-seattle.github.io/python-mlb-statsapi/async/) | [Public API](https://zero-sum-seattle.github.io/python-mlb-statsapi/public-api/) | [MLB Stats API](https://statsapi.mlb.com/)

</div>

`python-mlb-statsapi` is a Python client for MLB's Stats API.

- **Broad API coverage:** Query teams, players, schedules, games, statistics, and more.
- **Pythonic models:** Work with [Pydantic](https://docs.pydantic.dev/) objects whose fields use `snake_case` names.
- **Sync and async:** Choose the synchronous `Mlb` client or the asynchronous `AsyncMlb` client. The async API is additive, so existing sync users can upgrade without changing their code.

> **Unofficial project.** This package and its authors are not affiliated with or endorsed by Major League Baseball or any MLB team. Use of MLB data is subject to [MLB's copyright notice](https://gdx.mlb.com/components/copyright.txt). This is an educational project—not for commercial use.

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
| CI-validated versions | Python 3.10 through 3.14 (`3.10`, `3.11`, `3.12`, `3.13`, `3.14`) |

See [Python support](https://zero-sum-seattle.github.io/python-mlb-statsapi/public-api/#python-support) for the complete policy.

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

See [Async usage](https://zero-sum-seattle.github.io/python-mlb-statsapi/async/) for lifecycle, concurrency, custom HTTPX clients, and the current async endpoint list.

## Sync or Async?

| | `Mlb` | `AsyncMlb` |
| --- | --- | --- |
| HTTP library | Requests | HTTPX |
| Context manager | `with Mlb()` | `async with AsyncMlb()` |
| Request | `mlb.get_team(...)` | `await mlb.get_team(...)` |
| Explicit cleanup | `mlb.close()` | `await mlb.aclose()` |

`AsyncMlb` mirrors the full endpoint surface of `Mlb`. Both clients return the same Pydantic models and follow the same public HTTP/error behavior.

See the [public API contract](https://zero-sum-seattle.github.io/python-mlb-statsapi/public-api/#asyncmlb-public-client) for the authoritative method list and signatures.

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

The stats API has several entry points and returns a nested `stats[group][type]` structure. See the dedicated [Stats Guide](https://zero-sum-seattle.github.io/python-mlb-statsapi/stats/) for `get_player_stats()`, `get_team_stats()`, `get_stats()`, and `get_players_stats_for_game()` examples using both `Mlb` and `AsyncMlb`.

### Schedule

```python
schedule = mlb.get_schedule(date="2022-10-13")
```

See the [method reference](https://zero-sum-seattle.github.io/python-mlb-statsapi/methods/) for the full method documentation that previously lived in the README. Longer runnable examples live in the [usage examples](https://zero-sum-seattle.github.io/python-mlb-statsapi/examples/).

## HTTP and Error Behavior

Both clients use explicit timeouts, structured exceptions, and pooled HTTP connections. `strict_http=True` is the default. Final non-404 4xx responses raise `MlbHttpError`, while existing endpoint-specific 404 behavior is preserved.

Library-created clients send a versioned User-Agent. The current package version sends `python-mlb-statsapi/1.1.0`. See the [HTTP transport documentation](https://zero-sum-seattle.github.io/python-mlb-statsapi/http-transport/) for the full transport contract.

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

For timeouts, retries, compatibility mode, ownership rules, and transport details, see the [HTTP transport documentation](https://zero-sum-seattle.github.io/python-mlb-statsapi/http-transport/).

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
| [Documentation home](https://zero-sum-seattle.github.io/python-mlb-statsapi/) | Installation, quick starts, and links to every guide |
| [Method reference](https://zero-sum-seattle.github.io/python-mlb-statsapi/methods/) | Method signatures and short descriptions from the original README reference |
| [Usage examples](https://zero-sum-seattle.github.io/python-mlb-statsapi/examples/) | Extended synchronous examples |
| [Stats guide](https://zero-sum-seattle.github.io/python-mlb-statsapi/stats/) | Player, team, general, and per-game stat queries with sync and async examples |
| [Async usage](https://zero-sum-seattle.github.io/python-mlb-statsapi/async/) | Async installation, lifecycle, concurrency, and examples |
| [HTTP transport](https://zero-sum-seattle.github.io/python-mlb-statsapi/http-transport/) | Timeouts, retries, strict HTTP, exceptions, and ownership |
| [Public API contract](https://zero-sum-seattle.github.io/python-mlb-statsapi/public-api/) | Supported symbols, signatures, endpoint methods, and stability policy |
| [Release notes](https://zero-sum-seattle.github.io/python-mlb-statsapi/releases/) | Release-specific changes and migration notes |

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
