<div align="center">

# Python MLB Stats API

**The Unofficial Python Wrapper for the MLB Stats API**

[![PyPI version](https://badge.fury.io/py/python-mlb-statsapi.svg)](https://badge.fury.io/py/python-mlb-statsapi)
![Development Branch Status](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/build-and-test-mlbstatsapi-test.yml/badge.svg?event=push)
![Periodic External Test Status](https://github.com/zero-sum-seattle/python-mlb-statsapi/actions/workflows/catch-and-report.yml/badge.svg?event=schedule)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-mlb-statsapi)
![GitHub](https://img.shields.io/github/license/zero-sum-seattle/python-mlb-statsapi)

<div align="left">

### *Copyright Notice*  
This package and its authors are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.

###### This is an educational project so no commercial use. 


![MLB Stats API](https://user-images.githubusercontent.com/2068393/203456246-dfdbdf0f-1e43-4329-aaa9-1c4008f9800d.jpg)

## Getting Started

*Python-mlb-statsapi* is an unofficial MLB Stats API written in python 3.7+. It provides developers access to the MLB Stats API endpoint to pull information related to MLB Rosters, Teams, Players, stats and much more. All the information for getting started can be found in this README. However, a more detailed explanation can be found in our Docs section or in our Wiki.


<div align="center">

### [Docs](https://github.com/zero-sum-seattle/python-mlb-statsapi/tree/development/docs) | [Examples](#examples) | [Wiki](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki) | [API](https://statsapi.mlb.com/) 

<div align="left">

## Installation
```python
python3 -m pip install -i https://test.pypi.org/simple/ python-mlb-statsapi
```
## Usage
```python
python3
>>> mlb = mlbstatsapi.Mlb()
>>> mlb.get_people_id("Ty France")
[664034]
>>> stats = ['season', 'seasonAdvanced']
>>> groups = ['hitting']
>>> mlb.get_player_stats(664034, stats=stats, groups=groups)
{'hitting': {'season': [HittingSeason], 'seasonadvanced': [HittingSeasonAdvanced] }}

>>> mlb.get_team_id("Oakland Athletics")
[133]

>>> stats = ['season', 'seasonAdvanced']
>>> groups = ['pitching']
>>> mlb.get_team_stats(133, stats, groups)
{'pitching': {'season': [PitchingSeason], 'seasonadvanced': [PitchingSeasonAdvanced] }}
```


## Documentation

### [People, Person, Players, Coaches](docs/people.md#class-mlb)
* `Mlb.get_people_id(self, fullname: str, sport_id: int = 1, search_key: str = 'fullname', **params)` - Return Person Id(s) from fullname
* `Mlb.get_person(self, player_id: int, **params)` - Return Person Object from Id
* `Mlb.get_people(self, sport_id: int = 1, **params)` - Return all Players from Sport
### [Draft](docs/drafts.md#class-mlb)
* `Mlb.get_draft(self, year_id: int, **params)` - Return a draft for a given year
### [Awards](docs/awards.md#class-mlb)
* `Mlb.get_awards(self, award_id: int, **params)` - Return rewards recipinets for a given award
### [Teams](docs/teams.md#class-mlb)
* `Mlb.get_team_id(self, team_name: str, search_key: str = 'name', **params)` - Return Team Id(s) from name
* `Mlb.get_team(self, team_id: int, **params)` - Return Team Object from Team Id
* `Mlb.get_teams(self, sport_id: int = 1, **params)` - Return all Teams for Sport
* `Mlb.get_team_coaches(self, team_id: int, **params)` - Return coaching roster for team for current or specified season
* `Mlb.get_team_roster(self, team_id: int, **params)` - Return player roster for team for current or specified season
### [Stats](docs/stats.md#class-mlb)
* `Mlb.get_player_stats(self, person_id: int, stats: list, groups: list, **params)` - Return stats by player id, stat type and groups
* `Mlb.get_team_stats(self, team_id: int, stats: list, groups: list, **params)` - Return stats by team id, stat types and groups
* `Mlb.get_stats(self, stats: list, groups: list, **params: dict)` - Return stats by stat type and group args
* `Mlb.get_players_stats_for_game(self, person_id: int, game_id: int, **params)` - Return player stats for a game
### [Gamepace](#gamepace-examples)
* `Mlb.get_gamepace(self, season: str, sport_id=1, **params)` - Return pace of game metrics for specific sport, league or team.
### [Venues](docs/venues.md#class-mlb)
* `Mlb.get_venue_id(self, venue_name: str, search_key: str = 'name', **params)` - Return Venue Id(s)
* `Mlb.get_venue(self, venue_id: int, **params)` - Return Venue Object from venue Id
* `Mlb.get_venues(self, **params)` - Return all Venues
### [Sports](docs/sports.md#class-mlb)
* `Mlb.get_sport(self, sport_id: int, **params)` - Return a Sport object from Id
* `Mlb.get_sports(self, **params)` - Return all teams for Sport Id
* `Mlb.get_sport_id(self, sport_name: str, search_key: str = 'name', **params)`- Return Sport Id from name
### [Schedules](docs/schedules.md#class-mlb)
* `Mlb.get_schedule(self, date: str, start_date: str, end_date: str, sport_id: int, team_id: int, **params)` - Return a Schedule
### [Divisions](docs/divisions.md#class-mlb)
* `Mlb.get_division(self, division_id: int, **params)` - Return a Divison 
* `Mlb.get_divisions(self, **params)` - Return all Divisions
* `Mlb.get_division_id(self, division_name: str, search_key: str = 'name', **params)` - Return Division Id(s) from name
### [Leagues](docs/leagues.md#class-mlb)
* `Mlb.get_league(self, league_id: int, **params)` - Return a League from Id
* `Mlb.get_leagues(self, **params)` - Return all Leagues
* `Mlb.get_league_id(self, league_name: str, search_key: str = 'name', **params)` - Return League Id(s)
### [Seasons](docs/seasons.md#class-mlb)
* `Mlb.get_season(self, season_id: str, sport_id: int = None, **params)` - Return a season
* `Mlb.get_seasons(self, sportid: int = None, **params)` - Return all seasons
### [Standings](docs/standings.md#class-mlb)
* `Mlb.get_standings(self, league_id: int, season: str, **params)` - Return standings
### [Schedules](#schedule-examples)
* `Mlb.get_schedule(self, date: str = None, start_date: str = None, end_date: str = None, sport_id: int = 1, team_id: int = None, **params)` - Return a Schedule from dates
* `Mlb.get_scheduled_games_by_date(self, date: str = None,start_date: str = None, end_date: str = None, sport_id: int = 1, **params)` - Return game ids from dates
### [Games](docs/games.md#class-mlb)
* `Mlb.get_game(self, game_id: int, **params)` - Return the Game for a specific Game Id
* `Mlb.get_game_play_by_play(self, game_id: int, **params)` - Return Play by play data for a game
* `Mlb.get_game_line_score(self, game_id: int, **params)` - Return a Linescore for a game
* `Mlb.get_game_box_score(self, game_id: int, **params)` - Return a Boxscore for a game

## Examples

Let's show some examples of getting stat objects from the API. What is baseball with out stats right?

### MLB Stats

#### Player Stats
Get the Id(s) of the players you want stats for and set stat types and groups.
```python
>>> mlb = mlbstatsapi.Mlb()
>>> player = mlb.get_player_id("Ty France")
>>> types = ['season', 'career']
>>> groups = ['hitting', 'pitching']
```
Use player.id and stat types and groups to return a stats dictionary
```python
>>> stat_dict = mlb.get_player_stats(player.id, stats=types, groups=groups )
>>> season_hitting_stat = stat_dict['hitting']['season']
>>> career_pitching_stat = stat_dict['pitching']['career']
```
Print season hitting stats
```python
>>> for attribute, value in season_hitting_stat.stat.__dict__.items():
...     print(attribute, value)
>>>
```
#### Team stats
Get the Team Id(s)
```python
python3
>>> mlb = mlbstatsapi.Mlb()
>>> team = mlb.get_team_id('Seattle Mariners')
>>> print(team.id)
[136]
```
Set the stat types and groups.
```python
>>> types = ['season', 'seasonAdvanced']
>>> groups = ['hitting']
```
Use team.id and the stat types and groups to return season hitting stats
```python
stats = mlb.get_team_stats(team.id, stats=types, groups=groups)
season_hitting = stats['hitting']['season']
advanced_hitting = stats['hitting']['seasonadvanced']
```
Print season and seasonadvanced stats
```python
>>> for attribute, value in season_hitting.stat.__dict__.items():
...     print(attribute, value)
>>>
... for attribute, value in advanced_hitting.stat.__dict__.items():
>>>     print(attribute, value)
```
### More stats examples
#### Expected Stats
Get player Id's
```python
>>> player = mlb.get_player_id('Ty France')
```
Set the stat type and group
```python
>>> stats = ['expectedStatistics']
>>> group = ['hitting']
```
Get Stats
```python
>>> stats = mlb.get_player_stats(player, stats=stats, groups=group)
>>> expectedstats = stats['hitting']['expectedstatistics']
```
#### vsPlayer
Get pitcher and batter player Ids
```
>>> hitter = mlb.get_player_id('Ty France')
>>> pitcher = mlb.get_player_id('Shoei Ohtani')
```
Set stat type, stat groups, and params
```
>>> stats = ['vsPlayer']
>>> group = ['hitting']
>>> params = {'opposingPlayerId': pitcher.id}
```
Get stats
```
>>> stats = self.mlb.get_player_stats(self.ty_france, stats=self.stats, groups=self.group, **self.params)
```
#### hotColdZones
Get player Id's
```python
>>> hitter = mlb.get_player_id('Ty France')
>>> pitcher = mlb.get_player_id('Shoei Ohtani')
```
Set the stat types and groups
```python
>>> type = ['hotColdZones']
>>> hitting_group = ['hitting']
>>> pitching_group = ['pitching']
```
The stat groups pitching and hitting both return hotColdZones for a pitcher and hitter. hotColdZones are not assigned to a
stat group because of issues related to the REST API. So hotColdZones will be assigned to the stat key in stats return dict.
```python
>>> hitting_hotcoldzones = mlb.get_player_stats(hitter.id, stats=type, groups=hitting_group)
>>> pitching_hotcoldzones = mlb.get_player_stats(pitcher.id, stats=type, groups=pitching_group)
```
hotColdZones returns a list of the HotColdZones
```python
>>> ty_france_hotcoldzones = hitting_hotcoldzones['stats']['hotcoldzones'][0]
>>> shoei_ohtani_hotcoldzones = pitching_hotcoldzones['stats']['hotcoldzones'][0]
```
Loop through the hotColdZone objects for Ty France
```python
>>> for zone in ty_france_hotcoldzones:
>>>     print(zone.zone)
>>>     print(zone.value)
>>>             
```
Loop through the hotColdZone objects for Shoei Ohtani
```python
>>> for zone in shoei_ohtani_hotcoldzones:
>>>     print(zonecodes.zone)
>>>     print(zonecodes.value)
>>>
```
#### Passing params
Get Team Ids
```python
python3
>>> mlb = mlbstatsapi.Mlb()
>>> team = mlb.get_team_id('Seattle Mariners')
```
Set the stat types and groups.
```python
>>> types = ['season', 'seasonAdvanced']
>>> groups = ['hitting']
```
Pass season to get_team_stats()
```python
stats = mlb.get_team_stats(team.id, stats=types, groups=groups, season=2018)

season_hitting = stats['hitting']['season']
advanced_hitting = stats['hitting']['seasonadvanced']
```
season should be 2018
```python
assertEqual(season_hitting.season == 2018)
assertEqual(advanced_hitting.season == 2018)
```

### Gamepace examples
Get pace of game metrics for specific sport, league or team.
```python
>>> mlb = mlbstatsapi.Mlb()
>>> season = 2021
>>> gamepace = mlb.get_gamepace(season)
```

### Schedule Examples
Get a schedule for given date
```python
>>> mlb = mlbstatsapi.Mlb()
>>> schedule = mlb.get_schedule_date('2022-10-13')
```
Get ScheduleDates from Schedule
```python
dates = schedule.dates
```
Print Game status and Home and Away Teams
```python
>>> for date in dates:
...     for game in date.games:
...             print(game.status)
...             print(game.teams.home)
...             print(game.teams.away)
```
### Game Examples
Get a Game for a given game id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> game = mlb.get_game(662242)
```
Get the weather for a game for a given game id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> game = mlb.get_game(662242)
>>> weather = game.gamedata.weather
>>>
>>> print(weather.condition)
>>> print(weather.temp)
>>> print(weather.wind)
```
Get the current status of a game for a given game id
```python
>>> mlb = mlbstatsapi.mlb()
>>> game = mlb.get_game(662242)
>>>
>>> linescore = game.livedata.linescore
>>> hometeaminfo = game.gamedata.teams.home
>>> awayteaminfo = game.gamedata.teams.away
>>> hometeamstatus = linescore.teams.home
>>> awayteamstatus = linescore.teams.away
>>>
>>> print("home: ", hometeaminfo.franchisename, hometeaminfo.clubname)
>>> print("      runs:", hometeamstatus.runs)
>>> print("      hits:", hometeamstatus.hits)
>>> print("      errors:", hometeamstatus.errors)
>>> print("away: ", awayteaminfo.franchisename, awayteaminfo.clubname)
>>> print("      runs:", awayteamstatus.runs)
>>> print("      hits:", awayteamstatus.hits)
>>> print("      errors:", awayteamstatus.errors)
>>> print("")
>>> print("inning:", linescore.inninghalf, linescore.currentinningordinal)
>>> print("balls:", linescore.balls)
>>> print("strikes:", linescore.strikes)
>>> print("Outs:", linescore.outs)
```
Get the play by play, line score, and box score objects from a game
```python
>>> mlb = mlbstatsapi.Mlb()
>>> game = mlb.get_game(662242)
>>>
>>> play_by_play = game.livedata.plays
>>> line_score = game.livedata.linescore
>>> box_score = game.livedata.boxscore
```
#### Play by Play
Get only the play by play for a given game id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> playbyplay = mlb.get_play_by_play(662242)
```
#### Line Score
Get only the line score for a given game id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> linescore = mlb.get_line_score(662242)
```
#### Box Score
Get only the box score for a given game id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> boxscore = mlb.get_box_score(662242)
```

### People Examples
Get all Players for a given sport id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> sport_id = mlb.get_sport_id()
>>> players = mlb.get_players(sport_id=sport_id)
>>> for player in players:
...     print(player.id)
```
Get a player id
```python
>>> player_id = mlb.get_player_id("Ty France")
>>> print(player_id[0])
```

### Team Examples
Get a Team
```python
>>> mlb = mlbstatsapi.Mlb()
>>> team_ids = mlb.get_team_id("Seattle Mariners")
>>> team_id = team_ids[0]
>>> team = mlb.get_team(team_id.id)
>>> print(team.id)
>>> print(team.name)
```
Get a Player Roster
```python
>>> mlb = mlbstatsapi.Mlb()
>>> team_id = 133
>>> players = mlb.get_team_roster(team_id)
>>> for player in players:
        print(player.jerseynumber)
```
Get a Coach Roster
```python
>>> mlb = mlbstatsapi.Mlb()
>>> team_id = 133
>>> coaches = mlb.get_team_coaches(team_id)
>>> for coach in coaches:
        print(coach.title)
```

### Draft Examples
Get a draft for a year
```python
>>> mlb = mlbstatsapi.Mlb()
>>> draft_year = '2019'
>>> draft = mlb.get_draft(draft_year)
```
Get Players from Draft
```python
>>> draftpicks = draft[0].picks
>>> for draftpick in draftpicks:
...     print(draftpick.id)
...     print(draftpick.pickround)
```

### Award Examples
Get awards for a given award id
```python
>>> mlb = mlbstatsapi.Mlb()
>>> retiredjersy = self.mlb.get_awards(award_id='RETIREDUNI_108')
>>> for recipient in retiredjersy.awards:
...     print (recipient.player.nameFirstLast, recipient.name, recipient.date)
```

### Venue Examples
Get a Venue
```python
>>> mlb = mlbstatsapi.Mlb()
>>> vevue_ids = mlb.get_venue_id('PNC Park')
>>> venue_id = venue_ids[0]
>>> venue = mlb.get_team(venue.id)
>>> print(venue.id)
>>> print(venue.name)
```

### Sport Examples
Get a Sport
```python
>>> mlb = mlbstatsapi.Mlb()
>>> sport_ids = mlb.get_sport_id('Major League Baseball')
>>> sport_id = sport_ids[0]
>>> sport = mlb.get_sport(sport_id)
```

### Division Examples
Get a division
```python
>>> mlb = mlbstatsapi.Mlb()
>>> division = mlb.get_division(200)
>>> print(division.name)
```

### League Examples
Get a league
```python
>>> mlb = mlbstatsapi.Mlb()
>>> league = mlb.get_league(103)
>>> print(league.name)
```

### Season Examples
Get a Season
```python
>>> mlb = mlbstatsapi.Mlb()
>>> season = mlb.get_season(2018)
>>> print(season.seasonid)
```

### Standings Examples
Get a Standings
```python
>>> mlb = mlbstatsapi.Mlb()
>>> standings = mlb.get_standings(103, 2018)
```
