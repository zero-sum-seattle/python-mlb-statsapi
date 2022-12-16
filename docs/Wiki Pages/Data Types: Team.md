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

* The team's spring venue. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)

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

* The league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)  

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

</blockquote>

</details>

<details>
<summary>division : Division   </summary>

* The division the team is in. Dataclass: [Division](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/divisions/division.py)

<blockquote>

<details>
<summary>id : int   </summary>

* id number of the divison  
</details>

<details>
<summary>name : str   </summary>

* name of the division  
</details>

<details>
<summary>link : str   </summary>

* link of the division  
</details>

</blockquote>

</details>

<details>
<summary>sport : Sport   </summary>

* The sport of the team. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)  

<blockquote>

<details>
<summary>id : int   </summary>

* id number of the sport  
</details>

<details>
<summary>name : str    </summary>

* name the sport  
</details>

<details>
<summary>link : str   </summary>

* link of the sport  
</details>

</blockquote>

</details>

<details>
<summary>shortname : str   </summary>

* The shortname of the team  
</details>

<details>
<summary>record : TeamRecord   </summary>

* The record of the team. Dataclass: [TeamRecord](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/attributes.py)  

<blockquote>

<details>
<summary>gamesplayed : int   </summary>

* Number of game played by team  
</details>

<details>
<summary>wildcardgamesback : str   </summary>

* Number of game back from wildcard  
</details>

<details>
<summary>leaguegamesback : str   </summary>

* Number of league games back  
</details>

<details>
<summary>springleaguegamesback : str   </summary>

* Number of game back in spring league  
</details>

<details>
<summary>sportgamesback : str   </summary>

* Number of games back in sport  
</details>

<details>
<summary>divisiongamesback : str   </summary>

* Number of games back in division  
</details>

<details>
<summary>conferencegamesback : str   </summary>

* Number of games back in conference  
</details>

<details>
<summary>leaguerecord : Dict   </summary>

* Record in league  
</details>

<details>
<summary>records : Dict   </summary>

* Records  
</details>

<details>
<summary>divisionleader : bool   </summary>

* Is this team a divison leader  
</details>

<details>
<summary>wins : int   </summary>

* Number of wins  
</details>

<details>
<summary>losses : int   </summary>

* Number of losses  
</details>

<details>
<summary>winningpercentage : str   </summary>

* Winning percentage  
</details>

</blockquote>

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


## Usage that returns Team objects

### `get_team`

Description: Return Team Object from Id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id`  | string/int| Yes      | unique team id | 

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sportId`  | string/int| No       | Insert a sportId to return a directory of team information for a particular club in a sport. |
| `season`   | string/int| No       | Insert year to return a directory of team information for a particular club in a specific season. |
| `fields`   | string    | No       | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

### `get_teams`

Description: Return all Team Objects from sportId

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_id`  | string/int| Yes      | unique sport id of teams | 1

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sportId`  | string/int| No       | Insert a sportId to return a directory of team information for a particular club in a sport. |
| `season`   | string/int| No       | Insert year to return a directory of team information for a particular club in a specific season. |
| `fields`   | string    | No       | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |
| `leagueIds` | string/int| No      | Insert leagueId to return team information for particular league. |
| `activeStatus` | string | No      | Insert activeStatus to populate a teams based on active/inactive status for a given season. There are three status types: Y, N, B |
| `allStarStatuses` | string    | No       | Insert allStarStatuses to populate a teams based on Allstar status for a given season. There are two status types: Y and N |
| `gameType`   | string    | No       | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/teams?sportId=1```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_teams(sport_id = 1)
```