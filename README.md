# Python MLB Stats API - Unofficial MLB Stats API

![MLB Stats API](https://user-images.githubusercontent.com/2068393/203456246-dfdbdf0f-1e43-4329-aaa9-1c4008f9800d.jpg)


*Python-mlb-statsapi* is an unffocial MLB Stats API written in python 3.7+. It provides developers access to the MLB Stats API endpoint to pull information related to MLB Rosters, Teams, Players, and stats. 

This is a educational project so no commercial use. 

*Copyright Notice*
This package and its authors are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.

## Installation
```
python3 -m pip install -i https://test.pypi.org/simple/ python-mlb-statsapi
```
## Usage
```
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

### People, Person, Players, Coaches
* `Mlb.get_people_id()` - Return Person Id(s) from fullname
* `Mlb.get_person()` - Return Person Object from Id
* `Mlb.get_people()` - Return all Players from Sport
### Teams
* `Mlb.get_team_id()` - Return Team Id(s) from name
* `Mlb.get_team()` - Return Team Object from Team Id
* `Mlb.get_teams()`) - Return all Teams for Sport
* `Mlb.get_team_coaches()` - Return coaching roster for team for current or specified season
* `Mlb.get_team_roster()` - Return player roster for team for current or specified season
### Stats
* `Mlb.get_player_stats()` Return stats by player id, stat type and groups
* `Mlb.get_team_stats()` Return stats by team id, stat types and groups
### Venues
* `Mlb.get_venue_id()` - Return Venue Id(s)
* `Mlb.get_venue()` - Return Venue Object from venue Id
* `Mlb.get_venues()` - Return all Venues
### Sports
* `Mlb.get_sport()` - Return a Sport object from Id
* `Mlb.get_sports()` - Return all teams for Sport Id
* `Mlb.get_sport_id()`- Return Sport Id from name
### Divisions
* `Mlb.get_division()` - Return a Divison 
* `Mlb.get_divisions()` - Return all Divisions
* `Mlb.get_division_id()` - Return Division Id(s) from name
### Leagues
* `Mlb.get_league()` - Return a League from Id
* `Mlb.get_leagues()` - Return all Leagues
* `Mlb.get_league_id()` - Return League Id(s)
### Schedules
* `Mlb.get_schedule()` : Return a Schedule from dates
* `Mlb.get_schedule_today()` : Return Schedule for today
* `Mlb.get_schedule_date()` : Return Schedule for date
* `Mlb.get_schedule_date_range()` : Return Schedule between date
### Games
* `Mlb.get_game()` : Return the Game for a specific Game Id
* `Mlb.get_game_play_by_play()` : Return Play by play data for a game
* `Mlb.get_game_line_score()` : Return a Linescore for a game
* `Mlb.get_game_box_score()` : Return a Boxscore for a game

## Examples

Let's show some examples of getting stat objects from the API. What is baseball with out stats right?

NOTE: Stat types and groups are case sensitive
### Stats

#### Player Stats
Get the Id(s) of the players you want stats for and set stat types and groups.
```
>>> mlb = mlbstatsapi.Mlb()
>>> player = mlb.get_player_id("Ty France")
>>> types = ['season`, `career` ]
>>> groups = ['hitting', 'pitching]
```
Use player.id and stat types and groups to return a stats dictionary
```
>>> stat_dict = mlb.get_player_stats(player.id, stats=types, groups=groups )
>>> season_hitting_stat = stat_dict['hitting']['season']
>>> career_pitching_stat = stat_dict['pitching']['career']
```
Print season hitting stats
```
>>> for attribute, value in season_hitting_stat.__dict__.items():
>>>     print(attribute, value)
>>>
```
#### Team stats
Get the Team Id(s)
```
python3
>>> mlb = mlbstatsapi.Mlb()
>>> team = mlb.get_team_id('Seattle Mariners')
>>> print(team.id)
[136]
```
Set the stat types and groups.
```
>>> types = ['season', 'seasonAdvanced']
>>> groups = ['hitting']
```
Use team.id and the stat types and groups to return season hitting stats
```
stats = mlb.get_team_stats(team.id, stats=types, groups=groups)
season_hitting = stats['hitting']['season']
advanced_hitting = stats['hitting']['seasonadvanced']
```
Print season and seasonadvanced stats
```
>>> for attribute, value in season_hitting.__dict__.items():
>>>     print(attribute, value)
>>>
>>> for attribute, value in advanced_hitting.__dict__.items():
>>>     print(attribute, value)
```

### More stats examples

#### hotColdZones
Get player Id's
```
>>> hitter = mlb.get_player_id('Ty France')
>>> pitcher = mlb.get_player_id('Shoei Ohtani')
```
Set the stat types and groups
```
>>> type = ['hotColdZones']
>>> hitting_group = ['hitting']
>>> pitching_group = ['pitching']
```
The stat groups pitching and hitting both return hotColdZones for a pitcher and hitter. hotColdZones are not assigned to a
stat group because of issues related to the REST API. So hotColdZones will be assigned to the stat key in stats return dict.
```
>>> hitting_hotcoldzones = mlb.get_player_stats(hitter.id, stats=type, groups=hitting_group)
>>> pitching_hotcoldzones = mlb.get_player_stats(pitcher.id, stats=type, groups=pitching_group)
```
hotColdZones returns a list of the HotColdZones
```
>>> ty_france_hotcoldzones = hitting_hotcoldzones['stats']['hotcoldzones']
>>> shoei_ohtani_hotcoldzones = pitching_hotcoldzones['stats']['hotcoldzones']
```
Loop through the hotColdZone objects for Ty France
```
>>> for hotcoldzone in ty_france_hotcoldzones:
>>>     print(hotcoldzone.name)
>>>         for zonecodes in hotcoldzone.zones
>>>             print(zonecodes.zone)
>>>             print(zonecodes.value)
>>>             print(zonecodes.color)
>>>             print(zonecodes.temp)
```
Loop through the hotColdZone objects for Shoei Ohtani
```
>>> for hotcoldzone in shoei_ohtani_hotcoldzones:
>>>     print(hotcoldzone.name)
>>>         for zonecodes in hotcoldzone.zones
>>>             print(zonecodes.zone)
>>>             print(zonecodes.value)
>>>             print(zonecodes.color)
>>>             print(zonecodes.temp)
```

### Game Examples

### People Examples

### Team Examples

### Venue Examples

