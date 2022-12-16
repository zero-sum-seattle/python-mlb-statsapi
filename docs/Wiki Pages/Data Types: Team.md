## Usage that returns Team objects

_To be added_

## Team Structure

**Attributes are expandable and collapsable - [Link to Team dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)**


<blockquote>

<details>
<summary>id : int   </summary>

* id number of the team  
</details>

<details>
<summary>name : str   </summary>

* name of the team  
</details>

<details>
<summary>link : str   </summary>

* The API link for the team  
</details>

<details>
<summary>springleague : League   </summary>

* The spring league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

<blockquote>

<details>
<summary>id : int   </summary>

* id number of the league  
</details>

<details>
<summary>name : str   </summary>

* name of the league  
</details>

<details>
<summary>link : str   </summary>

* link of the league  
</details>

<details>
<summary>abbreviation : str   </summary>

* abbreviation the league  
</details>

</blockquote>

</details>

<details>
<summary>allstarstatus : str   </summary>

* The all status status of the team  
</details>

<details>
<summary>season : str   </summary>

* The team's current season  
</details>

<details>
<summary>venue : Venue   </summary>

* The team's home venue. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)  

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

</blockquote>

</details>

<details>
<summary>springvenue : Venue   </summary>

* The team's spring venue. Dataclass: [Venue]()

<blockquote>

<details>
<summary>id : int   </summary>

* id for this venue  
</details>

<details>
<summary>link : str   </summary>

* Link to venues endpoint  
</details>


</blockquote>

</details>

<details>
<summary>teamcode : str   </summary>

* team code   
</details>

<details>
<summary>filecode : str   </summary>

* filecode name of the team  
</details>

<details>
<summary>abbreviation : str   </summary>

* The abbreviation of the team name  
</details>

<details>
<summary>teamname : str   </summary>

* The team name   
</details>

<details>
<summary>locationname : str   </summary>

* The location of the team  
</details>

<details>
<summary>firstyearofplay : str   </summary>

* The first year the team began play  
</details>

<details>
<summary>league : League   </summary>

* The league of the team  
</details>

<details>
<summary>division : Division   </summary>

* The division the team is in  
</details>

<details>
<summary>sport : Sport   </summary>

* The sport of the team  
</details>

<details>
<summary>shortname : str   </summary>

* The shortname of the team  
</details>

<details>
<summary>record : TeamRecord   </summary>

* The record of the team  
</details>

<details>
<summary>franchisename : str   </summary>

* The franchisename of the team  
</details>

<details>
<summary>clubname : str   </summary>

* The clubname of the team  
</details>

<details>
<summary>active : str   </summary>

* Active status of the team  
</details>

<details>
<summary>parentorgname : str   </summary>

* The name of the parent team or org  
</details>

<details>
<summary>parentorgid : str   </summary>

* The id of the partent team or org  
</details>


</blockquote>


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/teams?sportId=1```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_teams(sport_id = 1)
```