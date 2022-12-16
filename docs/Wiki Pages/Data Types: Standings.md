## Usage that returns Standings objects

_To be added_

## Standings Structure

**Attributes are expandable and collapsable - [Link to Standings dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/standings.py)**


_To be added_


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_standings(league_id = 103, season = 2018)
```