# Stats Guide

The stats methods return MLB statistics grouped by **stat group** and then by **stat type**. Both `Mlb` and `AsyncMlb` return the same structure.

## Stats methods

| Method | Use |
| --- | --- |
| `get_player_stats()` | Stats for one player |
| `get_team_stats()` | Stats for one team |
| `get_stats()` | General stats query across the Stats API |
| `get_players_stats_for_game()` | Stats for one player in one game |

The synchronous and asynchronous signatures match. With `AsyncMlb`, await the method call.

## Understanding the return value

The four stats methods return a nested dictionary:

```text
stats[group][type] -> Stat
```

For example:

```python
stats = mlb.get_player_stats(
    664034,
    stats=["season"],
    groups=["hitting"],
    season=2022,
)

season_hitting = stats["hitting"]["season"]
```

`season_hitting` is a `Stat` model. Its `splits` field contains the returned stat splits.

```python
for split in season_hitting.splits:
    print(split.stat.model_dump(exclude_none=True))
```

A query can request multiple groups and stat types at once:

```python
stats = mlb.get_player_stats(
    664034,
    stats=["season", "career"],
    groups=["hitting", "fielding"],
    season=2022,
)

for group_name, group_stats in stats.items():
    for stat_type, stat in group_stats.items():
        print(group_name, stat_type, stat.total_splits)
```

If the API response contains no usable stats, these methods return `{}`.

## Player stats

Use `get_player_stats()` when you know the MLB person ID and want one or more stat types for that player.

### Sync

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    stats = mlb.get_player_stats(
        664034,
        stats=["season", "career"],
        groups=["hitting"],
        season=2022,
    )

season = stats["hitting"]["season"]
for split in season.splits:
    print(split.stat.model_dump(exclude_none=True))
```

### Async

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        stats = await mlb.get_player_stats(
            664034,
            stats=["season", "career"],
            groups=["hitting"],
            season=2022,
        )

    season = stats["hitting"]["season"]
    for split in season.splits:
        print(split.stat.model_dump(exclude_none=True))


asyncio.run(main())
```

## Team stats

Use `get_team_stats()` for stat data scoped to one team.

### Sync

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    stats = mlb.get_team_stats(
        136,
        stats=["season", "seasonAdvanced"],
        groups=["hitting"],
        season=2022,
    )

for stat_type, stat in stats["hitting"].items():
    print(stat_type)
    for split in stat.splits:
        print(split.stat.model_dump(exclude_none=True))
```

### Async

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        stats = await mlb.get_team_stats(
            136,
            stats=["season", "seasonAdvanced"],
            groups=["hitting"],
            season=2022,
        )

    for stat_type, stat in stats["hitting"].items():
        print(stat_type)
        for split in stat.splits:
            print(split.stat.model_dump(exclude_none=True))


asyncio.run(main())
```

## General stats queries

`get_stats()` queries the general `/stats` endpoint. Additional keyword arguments can narrow the request by season, team, league, game type, sport, and other Stats API parameters.

### Sync

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    stats = mlb.get_stats(
        stats=["season"],
        groups=["hitting"],
        season=2022,
        sportIds=1,
    )

for group_name, group_stats in stats.items():
    for stat_type, stat in group_stats.items():
        print(group_name, stat_type)
        for split in stat.splits:
            print(split.stat.model_dump(exclude_none=True))
```

### Async

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        stats = await mlb.get_stats(
            stats=["season"],
            groups=["hitting"],
            season=2022,
            sportIds=1,
        )

    for group_name, group_stats in stats.items():
        for stat_type, stat in group_stats.items():
            print(group_name, stat_type)
            for split in stat.splits:
                print(split.stat.model_dump(exclude_none=True))


asyncio.run(main())
```

## Player stats for a game

Use `get_players_stats_for_game()` when you have both the player's MLB person ID and the game's `gamePk`.

### Sync

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    stats = mlb.get_players_stats_for_game(
        person_id=663728,
        game_id=715757,
    )

for group_name, group_stats in stats.items():
    for stat_type, stat in group_stats.items():
        print(group_name, stat_type)
        for split in stat.splits:
            print(split.stat.model_dump(exclude_none=True))
```

### Async

```python
import asyncio

from mlbstatsapi import AsyncMlb


async def main():
    async with AsyncMlb() as mlb:
        stats = await mlb.get_players_stats_for_game(
            person_id=663728,
            game_id=715757,
        )

    for group_name, group_stats in stats.items():
        for stat_type, stat in group_stats.items():
            print(group_name, stat_type)
            for split in stat.splits:
                print(split.stat.model_dump(exclude_none=True))


asyncio.run(main())
```

## Finding valid stat types and groups

The MLB Stats API publishes the available values directly:

- Stat types: <https://statsapi.mlb.com/api/v1/statTypes>
- Stat groups: <https://statsapi.mlb.com/api/v1/statGroups>
- Event types: <https://statsapi.mlb.com/api/v1/eventTypes>
- Game types: <https://statsapi.mlb.com/api/v1/gameTypes>

Common stat groups include `hitting`, `pitching`, and `fielding`. Available stat types depend on the group and endpoint. Examples include `season`, `career`, `seasonAdvanced`, `gameLog`, and `playLog`.

## Numeric stat fields are typed as `float`

Rate and average stats such as `avg`, `obp`, `slg`, `ops`, `era`, `whip`, and
`babip` are typed as `Optional[float]`. The MLB Stats API returns these as
decimal strings (for example `".287"`), and Pydantic converts them to floats
automatically:

```python
split.stat.avg == 0.287        # not ".287"
split.stat.model_dump()["avg"] # 0.287, not ".287"
```

This is a behavioral change from earlier releases where these fields were
`str`. Code relying on string operations (`avg.startswith(".")`) or on
`avg == ".287"` needs to switch to numeric comparisons.

The MLB Stats API also uses two placeholder strings, `".---"` and `"-.--"`,
for these rate stats when the underlying value is not applicable (for
example a caught-stealing percentage when nobody has attempted a steal).
These two known sentinels are normalized to `None` before conversion, so
`split.stat.avg` is `None` rather than raising a validation error. Any other
non-numeric string still raises a `ValidationError`, since it isn't a
sentinel MLB is known to send.

Fields that use MLB's innings notation remain `str`, because values like
`"6.2"` mean 6 2/3 innings rather than the decimal 6.2:

- `SimpleFieldingSplit.innings`
- `SimplePitchingSplit.innings_pitched`
- `AdvancedPitchingSplit.innings_pitched_per_game`

## Related documentation

- [Method reference](methods.md)
- [General usage examples](examples.md)
- [Async usage](async.md)
- [Public API contract](public-api.md)
- [Stats model Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Stats)
