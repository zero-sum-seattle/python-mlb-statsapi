## Season Structure

**Attributes are expandable and collapsable - [Link to Season dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/seasons/season.py)**


<blockquote>

<details>
<summary>seasonid : str   </summary>

* season id  
</details>

<details>
<summary>haswildcard :  bool   </summary>

* wild card status  
</details>

<details>
<summary>preseasonstartdate : str   </summary>

* pre-season start date  
</details>

<details>
<summary>preseasonenddate : str   </summary>

* pre-season end date  
</details>

<details>
<summary>seasonstartdate : str   </summary>

* season start date  
</details>

<details>
<summary>springstartdate : str   </summary>

* spring start date  
</details>

<details>
<summary>springenddate : str   </summary>

* spring end date  
</details>

<details>
<summary>regularseasonstartdate : str   </summary>

* regular season start date  
</details>

<details>
<summary>lastdate1sthalf : str   </summary>

* last date 1st half  
</details>

<details>
<summary>allstardate : str   </summary>

* all star date  
</details>

<details>
<summary>firstdate2ndhalf : str   </summary>

* first date 2nd half  
</details>

<details>
<summary>regularseasonenddate : str   </summary>

* regular season end date  
</details>

<details>
<summary>postseasonstartdate : str   </summary>

* post season start date  
</details>

<details>
<summary>postseasonenddate : str   </summary>

* post season end date  
</details>

<details>
<summary>seasonenddate : str   </summary>

* season end date  
</details>

<details>
<summary>offseasonstartdate : str   </summary>

* off season start date  
</details>

<details>
<summary>offseasonenddate : str   </summary>

* off season end date  
</details>

<details>
<summary>seasonlevelgamedaytype : str   </summary>

* season level game day type  
</details>

<details>
<summary>gamelevelgamedaytype : str   </summary>

* game level game day type  
</details>

<details>
<summary>qualifierplateappearances :  float   </summary>

* qualifier plate appearances  
</details>

<details>
<summary>qualifieroutspitched : int   </summary>

* qualifier outs pitched  
</details>

</blockquote>


## Usage that returns Season objects

### `get_season`

Description: Returns a Season

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season_id` | string/int | Yes      | Insert year to return season information for a particular season. |
| `sport_id` | string/int | No      | Insert a sportId to return a directory of seasons for a specific sport. | 1


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `withGameTypeDates` | bool | No      | Insert a withGameTypeDates to return season information for all gameTypes. |
| `fields` | string/int | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute  | 


### `get_seasons`

Description: Return a list of Seasons

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_id` | string/int | Yes      | Insert a sportId to return a directory of seasons for a specific sport. | 1

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `divisionId` | string/int | No      | Insert divisionId to return a directory of seasons for a specific division. |
| `leagueId` | string/int | No      |  Insert leagueId to return a directory of seasons in a specific league. |
| `withGameTypeDates` | bool | No      | Insert a withGameTypeDates to return season information for all gameTypes. |
| `fields` | string/int | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |



## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/seasons?sportId=1```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_seasons()
```