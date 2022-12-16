## Usage that returns Venue objects

_To be added_

## Venue Structure

**Attributes are expandable and collapsable - [Link to Venue dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)**


_To be added_


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/venues?venueIds=15```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_venue(venue_id = 15)
```