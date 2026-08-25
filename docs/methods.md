# Method Reference

This page contains the method reference that previously lived in the README.

For detailed return-object and model documentation, follow the linked Wiki pages. For the stable 1.x public API contract and current async endpoint coverage, see [public-api.md](public-api.md).

**Jump to:** [People](#people-person-players-coaches) · [Teams](#teams) · [Stats](#stats) · [Games](#games) · [Schedules](#schedules) · [Venues](#venues) · [Sports](#sports) · [Leagues](#leagues) · [Divisions](#divisions) · [Seasons](#seasons) · [Standings](#standings) · [Draft](#draft) · [Awards](#awards) · [Gamepace](#gamepace)

## People, Person, Players, Coaches

[Wiki: People](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-People)

| Method | Description |
| --- | --- |
| `get_people_id()` | Return person ID(s) from a full name |
| `get_person()` | Return a person from an ID |
| `get_people()` | Return all players for a sport |

```text
Mlb.get_people_id(fullname: str, sport_id: int = 1, search_key: str = 'fullname', **params)
Mlb.get_person(player_id: int, **params)
Mlb.get_people(sport_id: int = 1, **params)
```

## Teams

[Wiki: Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Team)

| Method | Description |
| --- | --- |
| `get_team_id()` | Return team ID(s) from a name |
| `get_team()` | Return a team from a team ID |
| `get_teams()` | Return all teams for a sport |
| `get_team_coaches()` | Return the coaching roster for a team |
| `get_team_roster()` | Return the player roster for a team |

```text
Mlb.get_team_id(team_name: str, search_key: str = 'name', **params)
Mlb.get_team(team_id: int, **params)
Mlb.get_teams(sport_id: int = 1, **params)
Mlb.get_team_coaches(team_id: int, **params)
Mlb.get_team_roster(team_id: int, **params)
```

## Stats

[Wiki: Stats](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Stats) · [Stats Guide](stats.md)

| Method | Description |
| --- | --- |
| `get_player_stats()` | Return stats for a player |
| `get_team_stats()` | Return stats for a team |
| `get_stats()` | Return stats by stat type and group |
| `get_players_stats_for_game()` | Return player stats for a game |

```text
Mlb.get_player_stats(person_id: int, stats: list, groups: list, **params)
Mlb.get_team_stats(team_id: int, stats: list, groups: list, **params)
Mlb.get_stats(stats: list, groups: list, **params: dict)
Mlb.get_players_stats_for_game(person_id: int, game_id: int, **params)
```

The [Stats Guide](stats.md) includes runnable `Mlb` and `AsyncMlb` examples and explains the nested `stats[group][type]` return structure.

## Games

[Wiki: Game](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Game)

| Method | Description |
| --- | --- |
| `get_game()` | Return a game for a game ID |
| `get_game_play_by_play()` | Return play-by-play data for a game |
| `get_game_line_score()` | Return a linescore for a game |
| `get_game_box_score()` | Return a boxscore for a game |

```text
Mlb.get_game(game_id: int, **params)
Mlb.get_game_play_by_play(game_id: int, **params)
Mlb.get_game_line_score(game_id: int, **params)
Mlb.get_game_box_score(game_id: int, **params)
```

## Schedules

[Wiki: Schedule](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Schedule)

| Method | Description |
| --- | --- |
| `get_schedule()` | Return a schedule from a date or date range |
| `get_scheduled_games_by_date()` | Return scheduled games from dates |

```text
Mlb.get_schedule(date: str, start_date: str, end_date: str, sport_id: int, team_id: int, **params)
Mlb.get_schedule(date: str = None, start_date: str = None, end_date: str = None, sport_id: int = 1, team_id: int = None, **params)
Mlb.get_scheduled_games_by_date(date: str = None, start_date: str = None, end_date: str = None, sport_id: int = 1, **params)
```

## Venues

[Wiki: Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Venue)

| Method | Description |
| --- | --- |
| `get_venue_id()` | Return venue ID(s) from a name |
| `get_venue()` | Return a venue from an ID |
| `get_venues()` | Return all venues |

```text
Mlb.get_venue_id(venue_name: str, search_key: str = 'name', **params)
Mlb.get_venue(venue_id: int, **params)
Mlb.get_venues(**params)
```

## Sports

[Wiki: Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Sport)

| Method | Description |
| --- | --- |
| `get_sport()` | Return a sport from an ID |
| `get_sports()` | Return all sports |
| `get_sport_id()` | Return sport ID(s) from a name |

```text
Mlb.get_sport(sport_id: int, **params)
Mlb.get_sports(**params)
Mlb.get_sport_id(sport_name: str, search_key: str = 'name', **params)
```

## Leagues

[Wiki: League](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-League)

| Method | Description |
| --- | --- |
| `get_league()` | Return a league from an ID |
| `get_leagues()` | Return all leagues |
| `get_league_id()` | Return league ID(s) from a name |

```text
Mlb.get_league(league_id: int, **params)
Mlb.get_leagues(**params)
Mlb.get_league_id(league_name: str, search_key: str = 'name', **params)
```

## Divisions

[Wiki: Division](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Division)

| Method | Description |
| --- | --- |
| `get_division()` | Return a division from an ID |
| `get_divisions()` | Return all divisions |
| `get_division_id()` | Return division ID(s) from a name |

```text
Mlb.get_division(division_id: int, **params)
Mlb.get_divisions(**params)
Mlb.get_division_id(division_name: str, search_key: str = 'name', **params)
```

## Seasons

[Wiki: Season](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Season)

| Method | Description |
| --- | --- |
| `get_season()` | Return a season |
| `get_seasons()` | Return all seasons |

```text
Mlb.get_season(season_id: str, sport_id: int = None, **params)
Mlb.get_seasons(sportid: int = None, **params)
```

## Standings

[Wiki: Standings](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Standings)

| Method | Description |
| --- | --- |
| `get_standings()` | Return standings for a league and season |

```text
Mlb.get_standings(league_id: int, season: str, **params)
```

## Draft

[Wiki: Draft](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Draft(round))

| Method | Description |
| --- | --- |
| `get_draft()` | Return a draft for a given year |

```text
Mlb.get_draft(year_id: int, **params)
```

## Awards

[Wiki: Award](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Award)

| Method | Description |
| --- | --- |
| `get_awards()` | Return award recipients for an award |

```text
Mlb.get_awards(award_id: int, **params)
```

## Gamepace

[Wiki: Gamepace](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Gamepace)

| Method | Description |
| --- | --- |
| `get_gamepace()` | Return pace-of-game metrics for a sport, league, or team |

```text
Mlb.get_gamepace(season: str, sport_id=1, **params)
```
