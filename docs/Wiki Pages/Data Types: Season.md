## Usage that returns Season objects

_To be added_

## Season Structure

**Attributes are expandable and collapsable - [Link to Season dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/seasons/season.py)**


_To be added_


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/seasons?sportId=1```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_seasons()
```