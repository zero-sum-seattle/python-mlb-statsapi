# Python MLB Stats API

`python-mlb-statsapi` is a Python client for MLB's Stats API with synchronous and asynchronous interfaces.

[View usage examples](examples.md){ .md-button .md-button--primary }
[Browse the method reference](methods.md){ .md-button }

<div class="grid cards" markdown>

-   **Broad API coverage**

    Query teams, players, schedules, games, statistics, and more.

-   **Pythonic models**

    Work with [Pydantic](https://docs.pydantic.dev/) objects whose fields use `snake_case` names.

-   **Sync and async**

    Choose the synchronous `Mlb` client or the asynchronous `AsyncMlb` client. Existing sync users can upgrade without changing their code.

</div>

## Installation

Install the synchronous client:

```bash
python3 -m pip install python-mlb-statsapi
```

Install the optional `async` extra to use `AsyncMlb` and `AsyncMlbDataAdapter`:

```bash
python3 -m pip install "python-mlb-statsapi[async]"
```

Python 3.10 or newer is required.

## Quick start

### Synchronous client

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    player = mlb.get_person(664034)
    team = mlb.get_team(136)

print(player.full_name)
print(team.name)
```

### Asynchronous client

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

## Explore the documentation

- [Usage examples](examples.md) cover common synchronous workflows.
- [Stats guide](stats.md) explains player, team, general, and per-game statistics.
- [Async usage](async.md) covers lifecycle, concurrency, custom HTTPX clients, and endpoint support.
- [Method reference](methods.md) lists the available endpoint methods.
- [HTTP transport](http-transport.md) documents timeouts, retries, errors, proxies, and ownership.
- [Public API contract](public-api.md) defines supported symbols and compatibility guarantees.
- [Release notes](releases.md) summarize each published version.

> **Unofficial project.** This package and its authors are not affiliated with or endorsed by Major League Baseball or any MLB team. Use of MLB data is subject to [MLB's copyright notice](https://gdx.mlb.com/components/copyright.txt). This is an educational project—not for commercial use.
