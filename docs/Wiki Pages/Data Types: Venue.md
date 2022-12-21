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

* Location for this venue. Dataclass: [Location](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/attributes.py)

<blockquote>

<details>
<summary>address1 : str   </summary>

* Venues first address line  
</details>

<details>
<summary>address2 : str   </summary>

* Venues second address line  
</details>

<details>
<summary>city : str   </summary>

* City the venue is in  
</details>

<details>
<summary>state : str   </summary>

* The State the venue is in  
</details>

<details>
<summary>stateAbbrev : str   </summary>

* The staes abbreviation  
</details>

<details>
<summary>postalCode : str   </summary>

* Postal code for this venue  
</details>

<details>
<summary>defaultCoordinates : VenueDefaultCoordinates   </summary>

* Long and lat for this venues location. Dataclass: [VenueDefaultCoordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/attributes.py)  

<blockquote>

<details>
<summary>latitude : float   </summary>

* The latatude coordinate for this venue  
</details>

<details>
<summary>longitude : float   </summary>

* The longitude coordinate for this venue  
</details>

</blockquote>

</details>

<details>
<summary>country : str   </summary>

* What country this venue is in  
</details>

<details>
<summary>phone : str   </summary>

* Phone number for this venue  
</details>

</blockquote>
</details>

<details>
<summary>timezone : TimeZone   </summary>

* Timezone for this venue. Dataclass: [TimeZone](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/attributes.py)  

<blockquote>

<details>
<summary>id : str   </summary>

* id string for a venues timezone  
</details>

<details>
<summary>offset : int   </summary>

* The offset for this timezone from  
</details>

<details>
<summary>tz : str   </summary>

* Timezone string  
</details>

</blockquote>

</details>

<details>
<summary>fieldinfo :  FieldInfo   </summary>

* Info on this venue's field. Dataclass: [FieldInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/attributes.py)

<blockquote>

<details>
<summary>capacity : int   </summary>

* Capacity for this venue  
</details>

<details>
<summary>turfType : str   </summary>

* The type of turf in this venue  
</details>

<details>
<summary>roofType : str   </summary>

* What kind of roof for this venue  
</details>

<details>
<summary>leftLine : int   </summary>

* Distance down the left line  
</details>

<details>
<summary>left : int   </summary>

* Distance to left  
</details>

<details>
<summary>leftCenter : int   </summary>

* Distance to left center  
</details>

<details>
<summary>center : int   </summary>

* Distance to center  
</details>

<details>
<summary>rightCenter : int   </summary>

* Distance to right center  
</details>

<details>
<summary>right : int   </summary>

* Distance to right  
</details>

<details>
<summary>rightLine : int   </summary>

* Distance to right line  
</details>

</blockquote>

</details>

<details>
<summary>active : bool   </summary>

* Is this field currently active  
</details>

</blockquote>


## Usage that returns Venue objects

### `get_venue`

Description: Returns venue directorial information for all available venues in the Stats API.

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `venue_id`  | string/int | Yes      | venueId to return venue directorial information based venueId. |


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `fields`   | string | Yes       | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | 

### `get_venues`

Description: Return all venues

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `venueIds`   | int/list | No | Insert venueId to return venue directorial information based venueId. | 
| `sportIds`   | string/int | No | Insert sportIds to return venue directorial information based a given sport(s). For a list of all sports: https://statsapi.mlb.com/api/v1/sports | 
| `season`   | string/int | No | Insert year to return venue directorial information for a given season.  | 
| `fields`   | string | No | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | 


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/venues?venueIds=15```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_venue(venue_id = 15)
```