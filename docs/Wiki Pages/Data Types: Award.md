## Award Structure

**Attributes are expandable and collapsable - [Link to award dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/awards/attributes.py)**

<blockquote>

<details>
<summary>id : str  </summary>

* Award id 
</details>

<details>
<summary>name : str  </summary>

* Name of the award 
</details>

<details>
<summary>date : str  </summary>

* Date of when award was given 
</details>

<details>
<summary>season : str  </summary>

* Season award is for/from 
</details>

<details>
<summary>team : Team  </summary>

* Team award was to/ Player is from. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Team)

<blockquote>

<details>
<summary>id : int</summary>

* id number of the team
</details>

<details>
<summary>link : str</summary>

* The API link for the team
</details>

</blockquote>

</details>

<details>
<summary>player : Person  </summary>

* Person award is for. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-People)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person 
</details>

<details>
<summary>link : str  </summary>

* link to person 
</details>

<details>
<summary> primaryPosition : Position  </summary>

+ Dataclass: [AttendanceTotals](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/models/attendances/attributes.py#L142)
<blockquote>

<details>
<summary>code: str  </summary>

* code number of the Position 
</details>

<details>
<summary>name: str  </summary>

* the name of the Position 
</details>

<details>
<summary>type: str  </summary>

* the type of the Position 
</details>

<details>
<summary>abbreviation: str  </summary>

* the abbreviation of the Position 
</details>


</blockquote>

</details>


<details>
<summary>namefirstlast : str  </summary>

* The first and last name of the Person 
</details>

<blockquote>

</details>

<details>
<summary>notes : str  None  </summary>

* Any notes associated with award 
</details>

</blockquote>


## Usage that returns Award objects

### `get_awards`

Description: Return a list of awards

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `award_id` | string | Yes      | Insert a awardId to return a directory of players for a given award. | None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sportId` | string/int | No      | Insert a sportId to return a directory of players for a given award in a specific sport. | None
| `leagueId` | string/int | No      | Insert leagueId(s) to return a directory of players for a given award in a specific league. Format '103,104' | None
| `season` | string/int | No      | Insert year(s) to return a directory of players for a given award in a given season. Format '2016,2017' | None



## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/awards/MLBHOF/recipients?sportId=1&season=2017&leagueId=103```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_awards(award_id = MLBHOF, sportId = 1, season = 2017, leagueId = 103)
```