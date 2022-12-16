## Division Structure

**Attributes are expandable and collapsable - [Link to Division dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/divisions/division.py)**


<blockquote>

<details>
<summary>id : int  </summary>

* id number of the divison 
</details>

<details>
<summary>name : str  </summary>

* name of the division 
</details>

<details>
<summary>link : str  </summary>

* link of the division 
</details>

<details>
<summary>season : str  </summary>

* Current season for the division 
</details>

<details>
<summary>nameshort : str  </summary>

* Short name for the division 
</details>

<details>
<summary>abbreviation : str  </summary>

* Abbreviation of the divison name 
</details>

<details>
<summary>league : League  </summary>

* League this division is in. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the league 
</details>

<details>
<summary>link : str  </summary>

* link of the league  
</details>


</blockquote>

</details>

<details>
<summary>sport : Sport  </summary>

* Sport this divison is in. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the sport 
</details>

<details>
<summary>link : str  </summary>

* link of the sport  
</details>


</blockquote>

</details>

<details>
<summary>haswildcard : bool  </summary>

* If this league has a wildcard 
</details>

<details>
<summary>sortorder : int  </summary>

* Sort order 
</details>

<details>
<summary>numplayoffteams : int  </summary>

* Number of playoff teams in division 
</details>

<details>
<summary>active : bool  </summary>

* Current status of this division 
</details>

</blockquote>


## Usage that returns Division objects

### `get_division`

Description: Returns a Division

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `divison_id` | string/int | Yes      | divisionId to return a directory of division(s) for a specific division. | None


### `get_divisions`

Description: Return all divisons

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `divisionId` | string/int | No      | Insert divisionId(s) to return a directory of division(s) for a specific division. Format '200,201' | None
| `leagueId` | string/int | No      | Insert leagueId to return a directory of division(s) for all divisions in a specific league. | None
| `sportId` | string/int | No      | Insert a sportId to return a directory of division(s) for all divisions in a specific sport. | None



## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/divisions?divisionId=200&leagueId=103&sportId=1```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_division(division_id = 200, leagueId = 103, sportId = 1)
```