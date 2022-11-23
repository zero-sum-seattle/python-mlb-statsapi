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
* `mlb.get_people_id('Ty France')` - Get Person IDs from fullname
* `mlb.get_person(664034)` - Get Person Object
* `mlb.get_people(sport_id=1`) - Get all Players for Sport
### Teams
* `mlb.get_team_id('Seattle Mariners')` - Get Team IDs from name
* `mlb.get_team(133)` - Get Team Object from team id
* `mlb.get_teams(sport_id=1`) - Get all Teams for Sport
### Stats
* `mlb.get_player_stats()` get stats by player id, stat types, and stat groups
* `mlb.get_team_stats()` get stats by team id, stat types, and stat groups
### Venues
* `mlb.get_venue_id()` - Get Venue IDs
* `mlb.get_venue()` - Get Venue Object from venue id
* `mlb.get_venues()` - Get all Venues
### Sports
* `mlb.get_sport()` - Get a Sport object from id
* `mlb.get_sports()` - Get all teams for sport id
* `mlb.get_sport_id()`- Get sport ID from name
### Divisions
* `mlb.get_division()` - Get a Divison 
* `mlb.get_divisions()` - Get all divisions
* `mlb.get_division_id()` - Get divion id from name
### Leagues
* `mlb.get_league()` - Get a League from id
* `mlb.get_leagues()` - Get all Leagues
* `mlb.get_league_id()` - Get League IDs by name


## Examples

Let's show some examples of getting stat objects from the API. What is baseball with out stats right?

NOTE: Stat types and stat groups are case sensitive
### Player Stats


- Get the ID(s) of the players you want stats for and set stat type and group.
```
>>> mlb = mlbstatsapi.Mlb()
>>> player = mlb.get_player_id("Ty France")
>>> types = ['season`, `career` ]
>>> groups = ['hitting', 'pitching]
```

- Use player.id and stat types and groups to return a stats dictionary
```
>>> stat_dict = mlb.get_player_stats(player.id, stats=types groups=groups )
>>> season_hitting_stat = stat_dict['hitting']['season']
>>> career_pitching_stat = stat_dict['pitching']'career']

- Print season hitting stats
>>> for attribute, value in season_hitting_stat.__dict__.items():
>>>     print(attribute, value)
>>>
```
    
    
    