## Draft(Round) Structure

**Attributes are expandable and collapsable - [Link to Draft(Round) dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/drafts/rounds.py)**

<blockquote>

<details>
<summary>round : str  </summary>

* The round number of the draft, represented as a string.  
</details>

<details>
<summary>picks : List[DraftPick]  </summary>

* A list of DraftPick objects representing the picks made in this round of the draft. Dataclass: [Draftpick](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/2b405b7cae75ada8b27456eb0bf25f1a910ce77d/mlbstatsapi/models/people/people.py#L226)

<blockquote>

<details>
<summary>bisplayerid : int  </summary>

* The unique identifier of the player associated with this draft pick.  
</details>

<details>
<summary>pickround : str  </summary>

* The round of the draft in which this pick was made.  
</details>

<details>
<summary>picknumber : int  </summary>

* The number of the pick in the round.  
</details>

<details>
<summary>roundpicknumber : int  </summary>

* The number of the pick overall in the draft.  
</details>

<details>
<summary>rank : int  </summary>

* The rank of the player among all players eligible for the draft.  
</details>

<details>
<summary>pickvalue : str  </summary>

* The value of the pick, if known.  
</details>

<details>
<summary>signingbonus : str  </summary>

* The signing bonus associated with this pick, if known.  
</details>

<details>
<summary>home : Home  </summary>

* Information about the player's home location. Dataclass: [Home](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/drafts/attributes.py)

<blockquote>

<details>
<summary>city : str  </summary>

* The city where the player is from.  
</details>

<details>
<summary>state : str  </summary>

* The state where the player is from.  
</details>

<details>
<summary>country : str  </summary>

* The country where the player is from.  
</details>


</blockquote>

</details>

<details>
<summary>scoutingreport : str  </summary>

* A scouting report on the player's abilities.  
</details>

<details>
<summary>school : School  </summary>

* Information about the player's school or college. Dataclass: [School](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/drafts/attributes.py)

<blockquote>

<details>
<summary>name : str  </summary>

* The name of the school.  
</details>

<details>
<summary>schoolclass : str  </summary>

* The class the student is in.  
</details>

<details>
<summary>city : str  </summary>

* The city where the school is located.  
</details>

<details>
<summary>country : str  </summary>

* The country where the school is located.  
</details>

<details>
<summary>state : str  </summary>

* The state where the school is located.  
</details>


</blockquote>

</details>

<details>
<summary>blurb : str  </summary>

* A   brief summary of the player's background and accomplishments.  
</details>

<details>
<summary>headshotlink : str  </summary>

* A   link to a headshot image of the player.  
</details>

<details>
<summary>team : Team</summary>

* The team that made this draft pick. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

<blockquote>

<details>
<summary>springleague : League</summary>

* The spring league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

<blockquote>

<details>
<summary>id : int</summary>

* id number of the league  
</details>

<details>
<summary>name : str</summary>

* name of the league  
</details>

<details>
<summary>link : str</summary>

* link of the league  
</details>

<details>
<summary>abbreviation : str</summary>

* abbreviation the league  
</details>


</blockquote>

</details>

<details>
<summary>allstarstatus : str</summary>

* The all status status of the team  
</details>

<details>
<summary>id : int</summary>

* id number of the team  
</details>

<details>
<summary>name : str</summary>

* name of the team  
</details>

<details>
<summary>link : str</summary>

* The API link for the team  
</details>


</blockquote>

</details>

<details>
<summary>drafttype : CodeDesc  </summary>

* Information about the type of draft in which this pick was made. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/2b405b7cae75ada8b27456eb0bf25f1a910ce77d/mlbstatsapi/models/data/data.py#L159)

<blockquote>

<details>
<summary>code : str  </summary>

* the pitch code to reference the pitch  
</details>

<details>
<summary>description : str  </summary>

* the description of the pitch  
</details>


</blockquote>

</details>

<details>
<summary>isdrafted : bool  </summary>

* Whether or not the player associated with this pick has been drafted.  
</details>

<details>
<summary>ispass : bool  </summary>

* Whether or not the team passed on making a pick in this round.  
</details>

<details>
<summary>year : str  </summary>

* The year in which the draft took place.  
</details>

</blockquote>

</details>

</blockquote>


## Usage that returns Draft(Round) objects

### `get_draft`

Description: Returns a draft object for year_id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `year_id` | string/int | Yes      | Insert a year_id to return a directory of seasons for a specific sport. | None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `round` | string | No      | Insert a round to return biographical and financial data for a specific round in a Rule 4 draft. | None
| `name` | string | No      | Insert the first letter of a draftees last name to return their Rule 4 biographical and financial data. | None
| `school` | string | No      | Insert the first letter of a draftees school to return their Rule 4 biographical and financial data. | None
| `state` | string | No      | Insert state to return a list of Rule 4 draftees from that given state. | None
| `country` | string | No      | Insert state to return a list of Rule 4 draftees from that given country. | None
| `position` | string | No      | Insert the position to return Rule 4 biographical and financial data for a players drafted at that position. | None
| `teamId` | string/int | No      | Insert teamId to return Rule 4 biographical and financial data for all picks made by a specific team. | None
| `playerId` | string/int | No      | Insert MLB playerId to return a player's Rule 4 biographical and financial data a specific Rule 4 draft. | None
| `bisPlayerId` | string/int | No      | Insert bisPlayerId to return a player's Rule 4 biographical and financial data a specific Rule 4 draft. | None



## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/draft/2018?round=1&name=M&school=A&position=P&teamId=116&playerId=663554&bisPlayerId=759143```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_draft(year_id = 2018, round=1, name = M, school = A, position = P, teamId = 116, playerId = 663554, bisPlayerId = 759143)
```