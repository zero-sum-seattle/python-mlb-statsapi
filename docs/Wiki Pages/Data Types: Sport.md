## Usage that returns Sport objects

_To be added_

## Sport Structure

**Attributes are expandable and collapsable - [Link to Sport dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)**


_To be added_


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```http://statsapi.mlb.com/api/v1/sports```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_sports()
```