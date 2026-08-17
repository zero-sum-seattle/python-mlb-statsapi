# Usage Examples

This document collects the longer usage examples that previously lived in the
README. The README keeps a short quick start; this guide is the extended tour.

Every example uses the synchronous `Mlb` client. Async usage is documented
separately in [async.md](async.md).

For return-object structure and endpoint details see the
[Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki). For the
supported method list, parameters, and return shapes see the
[public API contract](public-api.md). For transport behavior see the
[HTTP transport documentation](http-transport.md).

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

## Endpoint Examples

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
