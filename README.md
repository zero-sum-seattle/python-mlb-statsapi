<div align="center">

# Python MLB Stats API

**The Unofficial Python Wrapper for the MLB Stats API**

[![PyPI version](https://badge.fury.io/py/python-mlb-statsapi.svg)](https://badge.fury.io/py/python-mlb-statsapi)
![Development Branch Status](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test-mlbstatsapi-test.yml/badge.svg?event=push)
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
```python
python3 -m pip install python-mlb-statsapi
```

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

```bash
# Run tests
poetry run pytest

# Run external tests (requires internet)
poetry run pytest tests/external_tests/
```

### Pull Request Guidelines

- **All tests must pass** before submitting a PR
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

### Note on External Tests

Some tests make real API calls to the MLB Stats API. These may occasionally fail due to:
- API changes (new fields, removed endpoints)
- Season/data availability

If you notice external test failures, please check if the MLB API has changed and update the models accordingly.


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
