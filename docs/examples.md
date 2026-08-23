# Usage Examples

This document collects the longer usage examples that previously lived in the README. The README keeps a short quick start; this guide is the extended tour.

Every example in this file uses the synchronous `Mlb` client. Async usage is documented separately in [async.md](async.md).

For return-object structure and endpoint details see the [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki). For the supported method list, parameters, and return shapes see the [public API contract](public-api.md). For transport behavior see the [HTTP transport documentation](http-transport.md).

## Working with Pydantic Models

All returned objects are Pydantic models, giving you access to serialization and validation helpers.

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    player = mlb.get_person(664034)

print(player.full_name)
print(player.model_dump(exclude_none=True))
print(player.model_dump_json(indent=2))
```

## Players and teams

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

## Player stats

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    player_id = mlb.get_people_id("Ty France")[0]
    stats = mlb.get_player_stats(
        player_id,
        stats=["season", "career"],
        groups=["hitting", "pitching"],
        season=2022,
    )

season_hitting = stats["hitting"]["season"]
for split in season_hitting.splits:
    print(split.stat.model_dump(exclude_none=True))
```

## Team stats

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    team_id = mlb.get_team_id("Seattle Mariners")[0]
    stats = mlb.get_team_stats(
        team_id,
        stats=["season", "seasonAdvanced"],
        groups=["hitting"],
        season=2022,
    )

season_hitting = stats["hitting"]["season"]
for split in season_hitting.splits:
    print(split.stat.model_dump_json(indent=2, exclude_none=True))
```

## Schedule

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    schedule = mlb.get_schedule(date="2022-10-13")

for date in schedule.dates:
    for game in date.games:
        print(game.game_pk, game.status.detailed_state)
```

## Game data

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    game = mlb.get_game(662242)
    play_by_play = mlb.get_game_play_by_play(662242)
    line_score = mlb.get_game_line_score(662242)
    box_score = mlb.get_game_box_score(662242)
```

## Rosters

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    players = mlb.get_team_roster(136)
    coaches = mlb.get_team_coaches(136)

for player in players:
    print(f"#{player.jersey_number} {player.person.full_name}")

for coach in coaches:
    print(f"{coach.person.full_name}: {coach.title}")
```

## Draft

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    draft = mlb.get_draft("2019")

for pick in draft[0].picks:
    print(f"Round {pick.pick_round}, Pick {pick.pick_number}: {pick.person.full_name}")
```

## Awards

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    retired_numbers = mlb.get_awards(award_id="RETIREDUNI_108")

for recipient in retired_numbers.awards:
    print(f"{recipient.player.full_name}: {recipient.name} ({recipient.date})")
```

## Venue, division, league, and season

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    venue_id = mlb.get_venue_id("PNC Park")[0]
    venue = mlb.get_venue(venue_id)
    division = mlb.get_division(200)
    league = mlb.get_league(103)
    season = mlb.get_season(2018)

print(venue.name)
print(division.name)
print(league.name)
print(season.season_id)
```

## Standings

```python
from mlbstatsapi import Mlb

with Mlb() as mlb:
    standings = mlb.get_standings(103, 2018)

for record in standings:
    print(f"Division: {record.division.name}")
    for team in record.team_records:
        print(f"  {team.team.name}: {team.wins}-{team.losses}")
```
