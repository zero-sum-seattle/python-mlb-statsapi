## League Structure

**Attributes are expandable and collapsable - [Link to League dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)**

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the league  
</details>

<details>
<summary>name : str  </summary>

* name of the league  
</details>

<details>
<summary>link : str  </summary>

* link of the league  
</details>

<details>
<summary>abbreviation : str  </summary>

* abbreviation the league  
</details>

<details>
<summary>nameshort : str  </summary>

* Short name for the league  
</details>

<details>
<summary>seasonstate : str  </summary>

* State of the leagues season  
</details>

<details>
<summary>haswildcard : bool  </summary>

* Status of the leagues wildcard  
</details>

<details>
<summary>hassplitseason : bool  </summary>

* Status of the leagues split season  
</details>

<details>
<summary>numgames : int  </summary>

* Total number of league games  
</details>

<details>
<summary>hasplayoffpoints : bool  </summary>

* Status of the leagues playoff points  
</details>

<details>
<summary>numteams : int  </summary>

* Total number of team in league  
</details>

<details>
<summary>numwildcardteams : int  </summary>

* Total number of wildcard teams in league  
</details>

<details>
<summary>seasondateinfo : Season  </summary>

* LeagueSeasonDateInfo attribue. Dataclass: [Season](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/seasons/season.py)

<blockquote>

<details>
<summary>seasonid : str  </summary>

* season id  
</details>

<details>
<summary>haswildcard :  bool  </summary>

* wild card status  
</details>

<details>
<summary>preseasonstartdate : str  </summary>

* pre-season start date  
</details>

<details>
<summary>preseasonenddate : str  </summary>

* pre-season end date  
</details>

<details>
<summary>seasonstartdate : str  </summary>

* season start date  
</details>

<details>
<summary>springstartdate : str  </summary>

* spring start date  
</details>

<details>
<summary>springenddate : str  </summary>

* spring end date  
</details>

<details>
<summary>regularseasonstartdate : str  </summary>

* regular season start date  
</details>

<details>
<summary>lastdate1sthalf : str  </summary>

* last date 1st half  
</details>

<details>
<summary>allstardate : str  </summary>

* all star date  
</details>

<details>
<summary>firstdate2ndhalf : str  </summary>

* first date 2nd half  
</details>

<details>
<summary>regularseasonenddate : str  </summary>

* regular season end date  
</details>

<details>
<summary>postseasonstartdate : str  </summary>

* post season start date  
</details>

<details>
<summary>postseasonenddate : str  </summary>

* post season end date  
</details>

<details>
<summary>seasonenddate : str  </summary>

* season end date  
</details>

<details>
<summary>offseasonstartdate : str  </summary>

* off season start date  
</details>

<details>
<summary>offseasonenddate : str  </summary>

* off season end date  
</details>

<details>
<summary>seasonlevelgamedaytype : str  </summary>

* season level game day type  
</details>

<details>
<summary>gamelevelgamedaytype : str  </summary>

* game level game day type  
</details>

<details>
<summary>qualifierplateappearances :  float  </summary>

* qualifier plate appearances  
</details>

<details>
<summary>qualifieroutspitched : int  </summary>

* qualifier outs pitched  
</details>

</blockquote>

</details>

<details>
<summary>season : str  </summary>

* League season  
</details>

<details>
<summary>orgcode : str  </summary>

* Leagues orginization code  
</details>

<details>
<summary>conferencesinuse : bool  </summary>

* Status of the in use conferences of the league  
</details>

<details>
<summary>divisionsinuse : bool  </summary>

* Status of leagues divisions in use  
</details>

<details>
<summary>sport : Sport  </summary>

* What 'sport' this league is a part of. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)

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
<summary>sortorder : int  </summary>

* League sort order  
</details>

<details>
<summary>active : bool  </summary>

* Status on the activity of the league  
</details>

</blockquote>


## Usage that returns League objects

### `get_league`

Description: Returns 

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `league_id` | string | Yes      | leagueId to return league information for a specific league |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute|

### `get_leagues`

Description: Return all leagues

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `leagueId` | string | No      | leagueId(s) to return league information for specific leagues. Format '103,104'|
| `sportId` | string | No      | Insert sportId to return league information for a specific sport. For a list of all sportIds: http://statsapi.mlb.com/api/v1/sports|
| `seasons` | string | No      | Insert year(s) to return league information for a specific season. |
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |



## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/league?leagueIds=103&seasons=2018```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_league(league_id = 103, seasons = 2018)
```