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

* An object containing information about the division. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/divisions/division.py) 

<blockquote>

<details>
<summary>id : int   </summary>

* id number of the division  
</details>

<details>
<summary>link : str   </summary>

* link of the divison  
</details>

</blockquote>

</details>

<details>
<summary>sport : Sport   </summary>

* An object containing information about the sport. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py) 

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
<summary>lastupdated : str   </summary>

* A string indicating the last time the standing was updated.  
</details>

<details>
<summary>teamrecords : List[Teamrecords]   </summary>

* A list of Teamrecord objects containing the data for the teams standings. Dataclass: [Teamrecords](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py)

<blockquote>

<details>
<summary>team: Team   </summary>

* The team for which the data belongs to. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

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

</blockquote>

</details>

<details>
<summary>season: int   </summary>

* The season for which the data belongs to.  
</details>

<details>
<summary>streak: Streak   </summary>

* The streak of the team. Dataclass: [Streak](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py)

<blockquote>

<details>
<summary>streaktype : str   </summary>

* Steak type  
</details>

<details>
<summary>streaknumber : int   </summary>

* Streak number  
</details>

<details>
<summary>streakcode : str   </summary>

* Steak code  
</details>

</blockquote>

</details>

<details>
<summary>divisionrank: str   </summary>

* The rank of the team in their division.  
</details>

<details>
<summary>leaguerank: str   </summary>

* The rank of the team in their league.  
</details>

<details>
<summary>sportrank: str   </summary>

* The rank of the team in their sport.  
</details>

<details>
<summary>gamesplayed: int   </summary>

* The number of games played by the team.  
</details>

<details>
<summary>gamesback: str   </summary>

* The number of games behind the leader in the division.  
</details>

<details>
<summary>wildcardgamesback: str   </summary>

* The number of games behind the leader in the wild card race.  
</details>

<details>
<summary>leaguegamesback: str   </summary>

* The number of games behind the leader in the league.  
</details>

<details>
<summary>springleaguegamesback: str   </summary>

* The number of games behind the leader in the spring league.  
</details>

<details>
<summary>sportgamesback: str   </summary>

* The number of games behind the leader in the sport.  
</details>

<details>
<summary>divisiongamesback: str   </summary>

* The number of games behind the leader in the division.  
</details>

<details>
<summary>conferencegamesback: str   </summary>

* The number of games behind the leader in the conference.  
</details>

<details>
<summary>leaguerecord: OverallleagueRecord   </summary>

* The overall league record of the team. Dataclass: [OverallleagueRecord](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py) 

<blockquote>

<details>
<summary>wins : int   </summary>

* Overall number of wins in league  
</details>

<details>
<summary>losses : int   </summary>

* Overall number of losses in league  
</details>

<details>
<summary>pct : str   </summary>

* Overall percentage in league  
</details>

</blockquote>

</details>

<details>
<summary>lastupdated: str   </summary>

* The date when the data was last updated.  
</details>

<details>
<summary>records: Records   </summary>

* The records of the team. Dataclass: [Records](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py)

<blockquote>

<details>
<summary>splitrecords : Typerecords   </summary>

* A list of split records. Dataclass: [Typerecords](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py)  

<blockquote>

<details>
<summary>wins : int   </summary>

* Number of wins in type  
</details>

<details>
<summary>losses : int   </summary>

* Number of losses in type  
</details>

<details>
<summary>pct : str   </summary>

* Percentage in type  
</details>

<details>
<summary>type : str   </summary>

* Type of record  
</details>

</blockquote>

</details>

<details>
<summary>divisionrecords : Divisionrecords   </summary>

* A list of division records. Dataclass: [Divisionrecords](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py)  

<blockquote>

<details>
<summary>wins : int   </summary>

* Number of wins in division
</details>

<details>
<summary>losses : int   </summary>

* Number of losses in division
</details>

<details>
<summary>pct : str   </summary>

* Percentage in division
</details>

<details>
<summary>division : Divison   </summary>

* Division. Dataclass: [Division](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/divisions/division.py)

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

</blockquote>

</details>

<details>
<summary>overallrecords : Typerecords   </summary>

* A list of overall records. Dataclass: [Typerecords](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py)  

<blockquote>

<details>
<summary>wins : int   </summary>

* Number of wins in type  
</details>

<details>
<summary>losses : int   </summary>

* Number of losses in type  
</details>

<details>
<summary>pct : str   </summary>

* Percentage in type  
</details>

<details>
<summary>type : str   </summary>

* Type of record  
</details>

</blockquote>

</details>

<details>
<summary>leaguerecords : Leaguerecords   </summary>

* A list of league records. Dataclass: [Leaguerecords](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py)  

<blockquote>

<details>
<summary>wins : int   </summary>

* Number of wins in league  
</details>

<details>
<summary>losses : int   </summary>

* Number of losses in league  
</details>

<details>
<summary>pct : str   </summary>

* Percentage in league  
</details>

<details>
<summary>league : League   </summary>

* League. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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

</blockquote>

</details>

<details>
<summary>expectedrecords : Typerecords   </summary>

* A list of expected records. Dataclass: [Typerecords](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/standings/attributes.py)  

<blockquote>

<details>
<summary>wins : int   </summary>

* Number of wins in type  
</details>

<details>
<summary>losses : int   </summary>

* Number of losses in type  
</details>

<details>
<summary>pct : str   </summary>

* Percentage in type  
</details>

<details>
<summary>type : str   </summary>

* Type of record  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>runsallowed: int   </summary>

* The number of runs allowed by the team.  
</details>

<details>
<summary>runsscored: int   </summary>

* The number of runs scored by the team.  
</details>

<details>
<summary>divisionchamp: bool   </summary>

* A flag indicating whether the team is the division champion.  
</details>

<details>
<summary>divisionleader: bool   </summary>

* A flag indicating whether the team is the leader in their division.  
</details>

<details>
<summary>haswildcard: bool   </summary>

* A flag indicating whether the team has a wild card spot.  
</details>

<details>
<summary>clinched: bool   </summary>

* A flag indicating whether the team has clinched a spot in the playoffs.  
</details>

<details>
<summary>eliminationnumber: str   </summary>

* The number of games the team needs to win or the number of games their opponents need to lose in order to be eliminated from playoff contention.  
</details>

<details>
<summary>wildcardeliminationnumber: str   </summary>

* The number of games the team needs to win or the number of games their opponents need to lose in order to be eliminated from wild card contention.  
</details>

<details>
<summary>wins: int   </summary>

* The number of wins of the team.  
</details>

<details>
<summary>losses: int   </summary>

* The number of losses of the team.  
</details>

<details>
<summary>rundifferential: int   </summary>

* The run differential of the team (runs scored minus runs allowed).  
</details>

<details>
<summary>winningpercentage: str   </summary>

* The winning percentage of the team.  
</details>

<details>
<summary>wildcardrank: str   </summary>

* The rank of the team in the wild card race.  
</details>

<details>
<summary>wildcardleader: bool   </summary>

* A flag indicating whether the team is the leader in the wild card race.  
</details>

<details>
<summary>magicnumber: str   </summary>

* The number of games the team needs to win or the number of games their opponents need to lose in order to clinch a spot in the playoffs.  
</details>

<details>
<summary>clinchindicator: str   </summary>

* Clinch indicator.  
</details>

</blockquote>

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