## Gamepace Structure

**Attributes are expandable and collapsable - [Link to Gamepace dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/gamepace/gamepace.py)**


<blockquote>

<details>
<summary>teams : List[Gamepacedata]  </summary>

* A list of teams in the gamepace. Dataclass: [Gamepaceteams](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/gamepace/attributes.py)

<blockquote>

<details>
<summary>hitsper9inn : float  </summary>

* The number of hits per 9 innings played.  
</details>

<details>
<summary>runsper9inn : float  </summary>

* The number of runs scored per 9 innings played.  
</details>

<details>
<summary>pitchesper9inn : float  </summary>

* The number of pitches thrown per 9 innings played.  
</details>

<details>
<summary>plateappearancesper9inn : float  </summary>

* The number of plate appearances per 9 innings played.  
</details>

<details>
<summary>hitspergame : float  </summary>

* The number of hits per game played.  
</details>

<details>
<summary>runspergame : float  </summary>

* The number of runs scored per game played.  
</details>

<details>
<summary>inningsplayedpergame : float  </summary>

* The number of innings played per game.  
</details>

<details>
<summary>pitchespergame : float  </summary>

* The number of pitches thrown per game played.  
</details>

<details>
<summary>pitcherspergame : float  </summary>

* The number of pitchers used per game played.  
</details>

<details>
<summary>plateappearancespergame : float  </summary>

* The number of plate appearances per game played.  
</details>

<details>
<summary>totalgametime : str  </summary>

* The total time spent playing games in the league.  
</details>

<details>
<summary>totalinningsplayed : float  </summary>

* The total number of innings played in the league.  
</details>

<details>
<summary>totalhits : int  </summary>

* The total number of hits in the league.  
</details>

<details>
<summary>totalruns : int  </summary>

* The total number of runs scored in the league.  
</details>

<details>
<summary>totalplateappearances : int  </summary>

* The total number of plate appearances in the league.  
</details>

<details>
<summary>totalpitchers : int  </summary>

* The total number of pitchers used in the league.  
</details>

<details>
<summary>totalpitches : int  </summary>

* The total number of pitches thrown in the league.  
</details>

<details>
<summary>totalgames : int  </summary>

* The total number of games played in the league.  
</details>

<details>
<summary>total7inngames : int  </summary>

* The total number of 7-inning games played in the league.  
</details>

<details>
<summary>total9inngames : int  </summary>

* The total number of 9-inning games played in the league.  
</details>

<details>
<summary>totalextrainngames : int  </summary>

* The total number of extra inning games played in the league.  
</details>

<details>
<summary>timepergame : str  </summary>

* The amount of time spent per game in the league.  
</details>

<details>
<summary>timeperpitch : str  </summary>

* The amount of time spent per pitch in the league.  
</details>

<details>
<summary>timeperhit : str  </summary>

* The amount of time spent per hit in the league.  
</details>

<details>
<summary>timeperrun : str  </summary>

* The amount of time spent per run scored in the league.  
</details>

<details>
<summary>timeperplateappearance : str  </summary>

* The amount of time spent per plate appearance in the league.  
</details>

<details>
<summary>timeper9inn : str  </summary>

* The amount of time spent per 9 innings played in the league.  
</details>

<details>
<summary>timeper77plateappearances : str  </summary>

* The amount of time spent per 7-7 plate appearances in the league.  
</details>

<details>
<summary>totalextrainntime : str  </summary>

* The total amount of time spent on extra inning games in the league.  
</details>

<details>
<summary>timeper7inngame : str  </summary>

* The amount of time spent per 7-inning game in the league.  
</details>

<details>
<summary>total7inngamescompletedearly: int  </summary>

* The total number of 7-inning games completed early in the league.  
</details>

<details>
<summary>timeper7inngamewithoutextrainn: str  </summary>

* The amount of time spent per 7-inning game without extra innings in the league.  
</details>

<details>
<summary>total7inngamesscheduled : int  </summary>

* The total number of 7-inning games scheduled in the league.  
</details>

<details>
<summary>total7inngameswithoutextrainn : int  </summary>

* The total number of 7-inning games played without extra innings in the league.  
</details>

<details>
<summary>total9inngamescompletedearly : int  </summary>

* The total number of 9-inning games completed early in the league.  
</details>

<details>
<summary>total9inngameswithoutextrainn : int  </summary>

* The total number of 9-inning games  
</details>

<details>
<summary>total9inngamesscheduled : int  </summary>

* The total number of 9 inning games scheduled  
</details>

<details>
<summary>hitsperrun : float  </summary>

* The number of hits per run  
</details>

<details>
<summary>pitchesperpitcher : float  </summary>

* Number of pitches thrown per pitcher  
</details>

<details>
<summary>season : str  </summary>

* Season number  
</details>

<details>
<summary>team: Team  </summary>

* Team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the team  
</details>

<details>
<summary>name : str  </summary>

* name of the team  
</details>

<details>
<summary>link : str  </summary>

* api link of the team  
</details>

</blockquote>

</details>

<details>
<summary>league : League </summary>

* League. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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

</blockquote>

</details>

<details>
<summary>sport : Sport  </summary>

* Sport. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the sport  
</details>

<details>
<summary>code : str  </summary>

* Sport code  
</details>

<details>
<summary>link : str  </summary>

* link of the sport  
</details>

</blockquote>

</details>

<details>
<summary>prportalcalculatedfields : Prportalcalculatedfields  </summary>

* calculated fields for a league. Dataclass: [Prportalcalculatedfields](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/gamepace/attributes.py)

<blockquote>

<details>
<summary>total7inngames : int  </summary>

* The total number of 7-inning games played.  
</details>

<details>
<summary>total9inngames : int  </summary>

* The total number of 9-inning games played.  
</details>

<details>
<summary>totalextrainngames : int  </summary>

* The total number of extra-inning games played.  
</details>

<details>
<summary>timeper7inngame : str  </summary>

* The average time per 7-inning game.  
</details>

<details>
<summary>timeper9inngame : str  </summary>

* The average time per 9-inning game.  
</details>

<details>
<summary>timeperextrainngame : str  </summary>

* The average time per extra-inning game.  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>leagues : List[Gamepacedata]  </summary>

* A list of leagues in the gamepace. Dataclass: [Gamepaceteams](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/gamepace/attributes.py)

<blockquote>

<details>
<summary>hitsper9inn : float  </summary>

* The number of hits per 9 innings played.  
</details>

<details>
<summary>runsper9inn : float  </summary>

* The number of runs scored per 9 innings played.  
</details>

<details>
<summary>pitchesper9inn : float  </summary>

* The number of pitches thrown per 9 innings played.  
</details>

<details>
<summary>plateappearancesper9inn : float  </summary>

* The number of plate appearances per 9 innings played.  
</details>

<details>
<summary>hitspergame : float  </summary>

* The number of hits per game played.  
</details>

<details>
<summary>runspergame : float  </summary>

* The number of runs scored per game played.  
</details>

<details>
<summary>inningsplayedpergame : float  </summary>

* The number of innings played per game.  
</details>

<details>
<summary>pitchespergame : float  </summary>

* The number of pitches thrown per game played.  
</details>

<details>
<summary>pitcherspergame : float  </summary>

* The number of pitchers used per game played.  
</details>

<details>
<summary>plateappearancespergame : float  </summary>

* The number of plate appearances per game played.  
</details>

<details>
<summary>totalgametime : str  </summary>

* The total time spent playing games in the league.  
</details>

<details>
<summary>totalinningsplayed : float  </summary>

* The total number of innings played in the league.  
</details>

<details>
<summary>totalhits : int  </summary>

* The total number of hits in the league.  
</details>

<details>
<summary>totalruns : int  </summary>

* The total number of runs scored in the league.  
</details>

<details>
<summary>totalplateappearances : int  </summary>

* The total number of plate appearances in the league.  
</details>

<details>
<summary>totalpitchers : int  </summary>

* The total number of pitchers used in the league.  
</details>

<details>
<summary>totalpitches : int  </summary>

* The total number of pitches thrown in the league.  
</details>

<details>
<summary>totalgames : int  </summary>

* The total number of games played in the league.  
</details>

<details>
<summary>total7inngames : int  </summary>

* The total number of 7-inning games played in the league.  
</details>

<details>
<summary>total9inngames : int  </summary>

* The total number of 9-inning games played in the league.  
</details>

<details>
<summary>totalextrainngames : int  </summary>

* The total number of extra inning games played in the league.  
</details>

<details>
<summary>timepergame : str  </summary>

* The amount of time spent per game in the league.  
</details>

<details>
<summary>timeperpitch : str  </summary>

* The amount of time spent per pitch in the league.  
</details>

<details>
<summary>timeperhit : str  </summary>

* The amount of time spent per hit in the league.  
</details>

<details>
<summary>timeperrun : str  </summary>

* The amount of time spent per run scored in the league.  
</details>

<details>
<summary>timeperplateappearance : str  </summary>

* The amount of time spent per plate appearance in the league.  
</details>

<details>
<summary>timeper9inn : str  </summary>

* The amount of time spent per 9 innings played in the league.  
</details>

<details>
<summary>timeper77plateappearances : str  </summary>

* The amount of time spent per 7-7 plate appearances in the league.  
</details>

<details>
<summary>totalextrainntime : str  </summary>

* The total amount of time spent on extra inning games in the league.  
</details>

<details>
<summary>timeper7inngame : str  </summary>

* The amount of time spent per 7-inning game in the league.  
</details>

<details>
<summary>total7inngamescompletedearly: int  </summary>

* The total number of 7-inning games completed early in the league.  
</details>

<details>
<summary>timeper7inngamewithoutextrainn: str  </summary>

* The amount of time spent per 7-inning game without extra innings in the league.  
</details>

<details>
<summary>total7inngamesscheduled : int  </summary>

* The total number of 7-inning games scheduled in the league.  
</details>

<details>
<summary>total7inngameswithoutextrainn : int  </summary>

* The total number of 7-inning games played without extra innings in the league.  
</details>

<details>
<summary>total9inngamescompletedearly : int  </summary>

* The total number of 9-inning games completed early in the league.  
</details>

<details>
<summary>total9inngameswithoutextrainn : int  </summary>

* The total number of 9-inning games  
</details>

<details>
<summary>total9inngamesscheduled : int  </summary>

* The total number of 9 inning games scheduled  
</details>

<details>
<summary>hitsperrun : float  </summary>

* The number of hits per run  
</details>

<details>
<summary>pitchesperpitcher : float  </summary>

* Number of pitches thrown per pitcher  
</details>

<details>
<summary>season : str  </summary>

* Season number  
</details>

<details>
<summary>team: Team  </summary>

* Team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the team  
</details>

<details>
<summary>name : str  </summary>

* name of the team  
</details>

<details>
<summary>link : str  </summary>

* api link of the team  
</details>

</blockquote>

</details>

<details>
<summary>league : League </summary>

* League. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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

</blockquote>

</details>

<details>
<summary>sport : Sport  </summary>

* Sport. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the sport  
</details>

<details>
<summary>code : str  </summary>

* Sport code  
</details>

<details>
<summary>link : str  </summary>

* link of the sport  
</details>

</blockquote>

</details>

<details>
<summary>prportalcalculatedfields : Prportalcalculatedfields  </summary>

* calculated fields for a league. Dataclass: [Prportalcalculatedfields](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/gamepace/attributes.py)

<blockquote>

<details>
<summary>total7inngames : int  </summary>

* The total number of 7-inning games played.  
</details>

<details>
<summary>total9inngames : int  </summary>

* The total number of 9-inning games played.  
</details>

<details>
<summary>totalextrainngames : int  </summary>

* The total number of extra-inning games played.  
</details>

<details>
<summary>timeper7inngame : str  </summary>

* The average time per 7-inning game.  
</details>

<details>
<summary>timeper9inngame : str  </summary>

* The average time per 9-inning game.  
</details>

<details>
<summary>timeperextrainngame : str  </summary>

* The average time per extra-inning game.  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>sports : List[Gamepacedata]  </summary>

* A list of sports in the gamepace. Dataclass: [Gamepaceteams](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/gamepace/attributes.py)

<blockquote>

<details>
<summary>hitsper9inn : float  </summary>

* The number of hits per 9 innings played.  
</details>

<details>
<summary>runsper9inn : float  </summary>

* The number of runs scored per 9 innings played.  
</details>

<details>
<summary>pitchesper9inn : float  </summary>

* The number of pitches thrown per 9 innings played.  
</details>

<details>
<summary>plateappearancesper9inn : float  </summary>

* The number of plate appearances per 9 innings played.  
</details>

<details>
<summary>hitspergame : float  </summary>

* The number of hits per game played.  
</details>

<details>
<summary>runspergame : float  </summary>

* The number of runs scored per game played.  
</details>

<details>
<summary>inningsplayedpergame : float  </summary>

* The number of innings played per game.  
</details>

<details>
<summary>pitchespergame : float  </summary>

* The number of pitches thrown per game played.  
</details>

<details>
<summary>pitcherspergame : float  </summary>

* The number of pitchers used per game played.  
</details>

<details>
<summary>plateappearancespergame : float  </summary>

* The number of plate appearances per game played.  
</details>

<details>
<summary>totalgametime : str  </summary>

* The total time spent playing games in the league.  
</details>

<details>
<summary>totalinningsplayed : float  </summary>

* The total number of innings played in the league.  
</details>

<details>
<summary>totalhits : int  </summary>

* The total number of hits in the league.  
</details>

<details>
<summary>totalruns : int  </summary>

* The total number of runs scored in the league.  
</details>

<details>
<summary>totalplateappearances : int  </summary>

* The total number of plate appearances in the league.  
</details>

<details>
<summary>totalpitchers : int  </summary>

* The total number of pitchers used in the league.  
</details>

<details>
<summary>totalpitches : int  </summary>

* The total number of pitches thrown in the league.  
</details>

<details>
<summary>totalgames : int  </summary>

* The total number of games played in the league.  
</details>

<details>
<summary>total7inngames : int  </summary>

* The total number of 7-inning games played in the league.  
</details>

<details>
<summary>total9inngames : int  </summary>

* The total number of 9-inning games played in the league.  
</details>

<details>
<summary>totalextrainngames : int  </summary>

* The total number of extra inning games played in the league.  
</details>

<details>
<summary>timepergame : str  </summary>

* The amount of time spent per game in the league.  
</details>

<details>
<summary>timeperpitch : str  </summary>

* The amount of time spent per pitch in the league.  
</details>

<details>
<summary>timeperhit : str  </summary>

* The amount of time spent per hit in the league.  
</details>

<details>
<summary>timeperrun : str  </summary>

* The amount of time spent per run scored in the league.  
</details>

<details>
<summary>timeperplateappearance : str  </summary>

* The amount of time spent per plate appearance in the league.  
</details>

<details>
<summary>timeper9inn : str  </summary>

* The amount of time spent per 9 innings played in the league.  
</details>

<details>
<summary>timeper77plateappearances : str  </summary>

* The amount of time spent per 7-7 plate appearances in the league.  
</details>

<details>
<summary>totalextrainntime : str  </summary>

* The total amount of time spent on extra inning games in the league.  
</details>

<details>
<summary>timeper7inngame : str  </summary>

* The amount of time spent per 7-inning game in the league.  
</details>

<details>
<summary>total7inngamescompletedearly: int  </summary>

* The total number of 7-inning games completed early in the league.  
</details>

<details>
<summary>timeper7inngamewithoutextrainn: str  </summary>

* The amount of time spent per 7-inning game without extra innings in the league.  
</details>

<details>
<summary>total7inngamesscheduled : int  </summary>

* The total number of 7-inning games scheduled in the league.  
</details>

<details>
<summary>total7inngameswithoutextrainn : int  </summary>

* The total number of 7-inning games played without extra innings in the league.  
</details>

<details>
<summary>total9inngamescompletedearly : int  </summary>

* The total number of 9-inning games completed early in the league.  
</details>

<details>
<summary>total9inngameswithoutextrainn : int  </summary>

* The total number of 9-inning games  
</details>

<details>
<summary>total9inngamesscheduled : int  </summary>

* The total number of 9 inning games scheduled  
</details>

<details>
<summary>hitsperrun : float  </summary>

* The number of hits per run  
</details>

<details>
<summary>pitchesperpitcher : float  </summary>

* Number of pitches thrown per pitcher  
</details>

<details>
<summary>season : str  </summary>

* Season number  
</details>

<details>
<summary>team: Team  </summary>

* Team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the team  
</details>

<details>
<summary>name : str  </summary>

* name of the team  
</details>

<details>
<summary>link : str  </summary>

* api link of the team  
</details>

</blockquote>

</details>

<details>
<summary>league : League </summary>

* League. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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

</blockquote>

</details>

<details>
<summary>sport : Sport  </summary>

* Sport. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the sport  
</details>

<details>
<summary>code : str  </summary>

* Sport code  
</details>

<details>
<summary>link : str  </summary>

* link of the sport  
</details>

</blockquote>

</details>

<details>
<summary>prportalcalculatedfields : Prportalcalculatedfields  </summary>

* calculated fields for a league. Dataclass: [Prportalcalculatedfields](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/gamepace/attributes.py)

<blockquote>

<details>
<summary>total7inngames : int  </summary>

* The total number of 7-inning games played.  
</details>

<details>
<summary>total9inngames : int  </summary>

* The total number of 9-inning games played.  
</details>

<details>
<summary>totalextrainngames : int  </summary>

* The total number of extra-inning games played.  
</details>

<details>
<summary>timeper7inngame : str  </summary>

* The average time per 7-inning game.  
</details>

<details>
<summary>timeper9inngame : str  </summary>

* The average time per 9-inning game.  
</details>

<details>
<summary>timeperextrainngame : str  </summary>

* The average time per extra-inning game.  
</details>

</blockquote>

</details>

</blockquote>

</details>

</blockquote>

## Usage that returns Gamepace objects

### `get_gamepace`

Description: Returns a Gamepace

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | int | Yes      | Insert year to return a directory of pace of game metrics for a given season. | None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `teamIds` | int | No      | Insert a teamIds to return directory of pace of game metrics for a given team. Format '110' or '110,147' | None
| `leagueId` | int | No      | Insert leagueIds to return a directory of pace of game metrics for a given league. Format '103' or '103,104' | None
| `leagueListId` | string | No      | Insert a unique League List Identifier to return a directory of pace of game metrics for a specific league listId. | None
| `sportId` | int | No      | Insert a sportId to return a directory of pace of game metrics for a specific sport. Format '11' or '1,11' | None
| `gameType` | string | No      | Insert gameType(s) a return a directory of pace of game metrics for a specific gameType. For a list of all gameTypes:  | None
| `date` | string | No      | Insert date to return a directory of pace of game metrics for a particular date range. Format: MM/DD/YYYY !startDate must be coupled with endDate! | None
| `endDate` | string | No      | Insert date to return a directory of pace of game metrics for a particular date range. Format: MM/DD/YYYY ! endDate must be coupled with startDate ! | None
| `venueIds` | int | No      | Insert venueId to return a directory of pace of game metrics for a particular venueId. | None
| `orgType` | string | No      | Insert a orgType to return a directory of pace of game metrics based on team, league or sport. Available values : T- TEAM, L- LEAGUE, S- SPORT | None
| `includeChildren` | bool | No      | Insert includeChildren to return a directory of pace of game metrics for all child teams in a given parent sport. | None
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attr



## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/gamePace?season=2018```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_gamepace(season = 2018)
```