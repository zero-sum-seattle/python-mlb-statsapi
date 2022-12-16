## Usage that returns Venue objects

_To be added_

## Venue Structure

**Attributes are expandable and collapsable - [Link to Venue dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)**


<blockquote>

<details>
<summary>id : int   </summary>

* id for this venue  
</details>

<details>
<summary>name : str   </summary>

* Name for this venue  
</details>

<details>
<summary>link : str   </summary>

* Link to venues endpoint  
</details>

<details>
<summary>location : Location   </summary>

* Location for this venue  
</details>

<details>
<summary>timezone : TimeZone   </summary>

* Timezone for this venue  
</details>

<details>
<summary>fieldinfo :  FieldInfo   </summary>

* Info on this venue's field  
</details>

<details>
<summary>active : bool = None   </summary>

* Is this field currently active  
</details>


</blockquote>


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/venues?venueIds=15```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_venue(venue_id = 15)
```