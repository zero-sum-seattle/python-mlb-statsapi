## Usage that returns Attendance objects

`get_attendance`
----------

Description: Returns attendance data based on teamId, leagueId, or leagueListId. Required Parameters (at least one)

**Parameters:** At least one is required

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id ` | Int | Yes      | Insert a teamId to return directory of attendnace for a given team | None
| `league_id ` | Int/List[int] | Yes      | Insert leagueId(s) to return a directory of attendanace for a specific league. Format '103,104' | None
| `league_list_id ` | Str | Yes      | Insert a unique League List Identifier to return a directory of attendanace for a specific league listId. [List of Options](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/mlb_api.py#L1875)| None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | int | No      | Insert year(s) to return a directory of attendance for a given season. Season year number format yyyy | None
| `date` | string | No      | Insert date to return information for attendance on a particular date. Format: MM/DD/YYYY | None
| `gametype` | string | No      | Insert gameType(s) a directory of attendance for a given gameType. For a list of all gameTypes: https://statsapi.mlb.com/api/v1/gameTypes | None


## Attendance Structure

**Attributes are expandable and collapsable - [Link to attendance dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/attendances/attendance.py)**

<blockquote>

<details >

<summary> aggregatetotals : AttendanceTotals</summary>

+ Dataclass: [AttendanceTotals](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/models/attendances/attributes.py#L142)
<blockquote>

<details>
<summary>openingstotalaway : int  </summary>

* Total amount of opening game attendance number 
</details>

<details>
<summary>openingstotalhome : int   </summary>

* Total amount of opening home game attendance number   
</details>

    
<details>
<summary>openingstotallost : int   </summary>
    
* Total amount of opening games lost   
</details>

<details>
<summary>openingstotalytd : int   </summary>
    
* Total amount of opening games year to date   
</details>   

<details>
<summary>attendanceaverageaway : int   </summary>

* Average away game attendance   
</details>

<details>
<summary>attendanceaveragehome : int   </summary>

* Average home game attendance   
</details>

<details>
<summary>attendanceaverageytd : int   </summary>

* Average attendance year to date   
</details>

<details>
<summary>attendancehigh : int   </summary>

* Attendance high   
</details>

<details>
<summary>attendancehighdate : str   </summary>

* Attendance high date   
</details>

<details>
<summary>attendancetotal : int   </summary>

* Attendance total   
</details>

<details>
<summary>attendancetotalaway : int   </summary>

* Attendace total away   
</details>

<details>
<summary>attendancetotalhome : int   </summary>

* Attendance total home   
</details>

</blockquote>
</details>
<!-- End aggregatetotals -->

<details >
<summary>records : List[AttendanceRecords]</summary>

+ Dataclass: [AttendanceRecords](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/models/attendances/attributes.py#L58)]
<blockquote>

<details>
<summary>openingstotal : int  </summary>

* Total amount of openings   
</details>

<details>
<summary>openingstotalaway : int  </summary>

* Total amount of opening away games   
</details>

<details>
<summary>openingstotalhome : int  </summary>

* Total amount of opening home games   
</details>

<details>
<summary>openingstotallost : int  </summary>

* Total amount of openings lost   
</details>

<details>
<summary>gamestotal : int  </summary>

* Total amount of games   
</details>

<details>
<summary>gamesawaytotal : int  </summary>

* Total amount of away games   
</details>

<details>
<summary>gameshometotal : int  </summary>

* Total amount of home games   
</details>

<details>
<summary>year : str  </summary>

* Year as a string   
</details>

<details>
<summary>attendanceaverageaway : int  </summary>

* Average attendance for away games   
</details>

<details>
<summary>attendanceaveragehome : int  </summary>

* Average attendance for home games   
</details>

<details>
<summary>attendanceaverageytd : int  </summary>

* Average attendance year to date   
</details>

<details>
<summary>attendancehigh : int  </summary>

* Attendance High number   
</details>

<details>
<summary>attendancehighdate : str  </summary>

* Attendance high date   
</details>

<details >
<summary>attendancehighgame : AttendanceHighLowGame</summary>

+ Dataclass: [AttendanceHighLowGame](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/models/attendances/attributes.py#L19)
<blockquote>

<details>
<summary>gamepk : int  </summary>

* Games Id number
</details>

<details>
<summary>link : str  </summary>

* games endpoint link
</details>

<details >
<summary>content : AttendanceHighLowGameContent</summary>

+ Dataclass: [AttendanceHighLowGameContent](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/models/attendances/attributes.py#L7)
<blockquote>

<details>
<summary>link : str  </summary>

* games content endpoint link
</details>

</blockquote>

</details>

<details>
<summary>daynight : str  </summary>

* Type of time of day for game
</details>

</blockquote>

</details>

<details>
<summary>attendancelow : int  </summary>

* Attendance low number   
</details>

<details>
<summary>attendancelowdate : str  </summary>

* Attendance low date   
</details>

<details >
<summary>attendancelowgame : AttendanceHighLowGame  </summary>

<blockquote>

<details>
<summary>gamepk : int </summary>

* Games Id number
</details>

<details>
<summary>link : str </summary>

* games endpoint link
</details>

<details >
<summary>content : AttendanceHighLowGameContent </summary>

+ Dataclass: [AttendanceHighLowGameContent](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/models/attendances/attributes.py#L7)
<blockquote>

<details>
<summary>link : str </summary>

* games content endpoint link
</details>

</blockquote>

</details>

<details>
<summary>daynight : str </summary>

* Type of time of day for game
</details>

</blockquote>

</details>

<details>
<summary>attendanceopeningaverage : int  </summary>

* Attendance opening average   
</details>

<details>
<summary>attendancetotal : int  </summary>

* Attendance total   
</details>

<details>
<summary>attendancetotalaway : int  </summary>

* Attendance total away   
</details>

<details>
<summary>attendancetotalhome : int  </summary>

* Attendance total home   
</details>

<details >
<summary>gametype : AttendenceGameType  </summary>

+ Dataclass: [AttendenceGameType](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/models/attendances/attributes.py#L43)
<blockquote>

<details>
<summary>id : str  </summary>

* Game type id 
</details>

<details>
<summary>description : str  </summary>

* Game type description
</details>

<!-- End Game Type -->

</blockquote>

</details>

<details>
<summary>team : Team  </summary>

* Team   
</details>


</blockquote>

</details>
<!-- End records -->

</blockquote>


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/attendance?teamId=110&leagueId=103&season=2014&leagueListId=mlb&gameType=D```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_attendance(team_id = 110, league_id = 103, league_list_id = 'mlb', gameType = 'd', season = 2014)
```