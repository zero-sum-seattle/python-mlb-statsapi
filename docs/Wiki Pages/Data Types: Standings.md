## Usage that returns Standings objects

_To be added_

## Standings Structure

**Attributes are expandable and collapsable - [Link to Standings dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/standings.py)**


<blockquote>

<details>
<summary>standingstype : str   </summary>

* A string indicating the type of standings.  
</details>

<details>
<summary>league : league   </summary>

* An object containing information about the league. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py) 

<blockquote>

<details>
<summary>id : int   </summary>

* id number of the league  
</details>

<details>
<summary>link : str   </summary>

* link of the league  
</details>

</blockquote>

</details>

<details>
<summary>division : Division   </summary>

* An object containing information about the division. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py) 

<blockquote>

<details>
<summary>id : int   </summary>

* id number of the sport  
</details>

<details>
<summary>link : str   </summary>

* link of the sport  
</details>

</blockquote>

</details>

<details>
<summary>sport : Sport   </summary>

* An object containing information about the sport.  
</details>

<details>
<summary>lastupdated : str   </summary>

* A string indicating the last time the standing was updated.  
</details>

<details>
<summary>teamrecords : List[Teamrecords]   </summary>

* A list of Teamrecord objects containing the data for the teams standings.  
</details>


</blockquote>


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2018```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_standings(league_id = 103, season = 2018)
```