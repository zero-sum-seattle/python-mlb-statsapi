# Python MLB Stats API - Unofficial MLB Stats API

![MLB Stats API](/images/background.jpg)


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
* `mlb.get_people_id("Ty France")` - Get Person IDs
* `mlb.get_person(664034)` - Get Person Object
* `mlb.get_people(sport_id=1`) - Get all Players for Sport

### Teams
* `mlb.get_team_id()` - Get Team IDs
* `mlb.get_team(133)` - Get Team Object
* `mlb.get_teams(sport_id=1`) - Get all Teams for Sport

### Stats

### Venues
* `mlb.get_venue_id` - Get Venue IDs

### Sports

### Divisions

### Leagues