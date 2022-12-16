## Usage that returns Team objects

_To be added_

## Team Structure

**Attributes are expandable and collapsable - [Link to Team dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)**


_To be added_


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/teams?sportId=1```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_teams(sport_id = 1)
```