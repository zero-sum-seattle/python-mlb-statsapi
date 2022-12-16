## Usage that returns Schedule objects

_To be added_

## Schedule Structure

**Attributes are expandable and collapsable - [Link to Schedule dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/schedules/schedule.py)**


<blockquote>

<details>
<summary>totalitems : int   </summary>

* Total items in schedule  
</details>

<details>
<summary>totalevents : int  </summary>

* Total events in schedule  
</details>

<details>
<summary>totalgames : int  </summary>

* Total games in schedule  
</details>

<details>
<summary>totalgamesinprogress : int  </summary>

* Total games in progress in schedule  
</details>

<details>
<summary>dates : ScheduleDates  </summary>

* List of dates with games in schedule. Dataclass: [ScheduleDates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/schedules/attributes.py)

<blockquote>

<details>
<summary>date : str  </summary>

* Date for the group of games  
</details>

<details>
<summary>totalitems : int  </summary>

* Total amount of items for this date  
</details>

<details>
<summary>totalevents : int  </summary>

* The number of events for this date  
</details>

<details>
<summary>totalgames : int  </summary>

* The number of games for this date  
</details>

<details>
<summary>totalgamesinprogress : int  </summary>

* The number of games that are currently in progress for this date  
</details>

<details>
<summary>games : List[ScheduleGames]  </summary>

* A list of games for this date. Dataclass: [ScheduleGames](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/schedules/attributes.py)

<blockquote>

<details>
<summary>gamepk : int  </summary>

* The games id number  
</details>

<details>
<summary>link : str  </summary>

* The link for this game  
</details>

<details>
<summary>gametype : str  </summary>

* This games game type  
</details>

<details>
<summary>season : str  </summary>

* The season this game takes place in  
</details>

<details>
<summary>gamedate : str  </summary>

* The date for this game  
</details>

<details>
<summary>officialdate : str  </summary>

* The official date for this game  
</details>

<details>
<summary>status : GameStatus  </summary>

* The status of this game. Dataclass: [GameStatus](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

<blockquote>

<details>
<summary>abstractgamestate : str  </summary>

* The abstract game state  
</details>

<details>
<summary>codedgamestate : str  </summary>

* The coded game state  
</details>

<details>
<summary>detailedstate : str  </summary>

* The detailed game state  
</details>

<details>
<summary>statuscode : str  </summary>

* Status code for this game  
</details>

<details>
<summary>starttimetbd : bool  </summary>

* If the start time is TBD  
</details>

<details>
<summary>abstractgamecode : str  </summary>

* The abstract game code  
</details>

<details>
<summary>reason : str  </summary>

* reason for a state. Usually used for delays or cancellations  
</details>

</blockquote>

</details>

<details>
<summary>teams : ScheduleHomeAndAway  </summary>

* Holds teams and thier info for this game. Dataclass: [ScheduleHomeAndAway](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/schedules/attributes.py)

<blockquote>

<details>
<summary>home : ScheduleGameTeam  </summary>

* Home team info for this game. Dataclass: [ScheduleGameTeam](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/schedules/attributes.py)

<blockquote>

<details>
<summary>leaguerecord : LeagueRecord  </summary>

* League record for this team. Dataclass: [LeagueRecord](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

<blockquote>

<details>
<summary>wins : int  </summary>

* number of wins in leaguerecord  
</details>

<details>
<summary>losses : int  </summary>

* number of losses in leaguerecord  
</details>

<details>
<summary>ties : int  </summary>

* number of ties in leaguerecord  
</details>

<details>
<summary>pct : str  </summary>

* winning pct of leaguerecord  
</details>

</blockquote>

</details>

<details>
<summary>score : int  </summary>

* Current score for this team in this game  
</details>

<details>
<summary>team : Team  </summary>

* Team info for this game. Dataclass: [ScheduleGameTeamInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)  

<blockquote>

<details>
<summary>id : int  </summary>

* Team id  
</details>

<details>
<summary>name : str  </summary>

* The teams name  
</details>

<details>
<summary>link : str  </summary>

* The link for this team  
</details>

</blockquote>

</details>

<details>
<summary>iswinner : bool  </summary>

* If this team is the winner of this game  
</details>

<details>
<summary>splitsquad : bool  </summary>

* Split squad  
</details>

<details>
<summary>seriesnumber : int  </summary>

* Series number   
</details>

</blockquote>

</details>

<details>
<summary>away : ScheduleGameTeam  </summary>

* Away team info for this game. Dataclass: [ScheduleGameTeam](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/schedules/attributes.py)

<blockquote>

<details>
<summary>leaguerecord : LeagueRecord  </summary>

* League record for this team. Dataclass: [LeagueRecord](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

<blockquote>

<details>
<summary>wins : int  </summary>

* number of wins in leaguerecord  
</details>

<details>
<summary>losses : int  </summary>

* number of losses in leaguerecord  
</details>

<details>
<summary>ties : int  </summary>

* number of ties in leaguerecord  
</details>

<details>
<summary>pct : str  </summary>

* winning pct of leaguerecord  
</details>

</blockquote>

</details>

<details>
<summary>score : int  </summary>

* Current score for this team in this game  
</details>

<details>
<summary>team : Team  </summary>

* Team info for this game. Dataclass: [ScheduleGameTeamInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)  

<blockquote>

<details>
<summary>id : int  </summary>

* Team id  
</details>

<details>
<summary>name : str  </summary>

* The teams name  
</details>

<details>
<summary>link : str  </summary>

* The link for this team  
</details>

</blockquote>

</details>

<details>
<summary>iswinner : bool  </summary>

* If this team is the winner of this game  
</details>

<details>
<summary>splitsquad : bool  </summary>

* Split squad  
</details>

<details>
<summary>seriesnumber : int  </summary>

* Series number   
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>venue : Venue    </summary>

* The venue this game takes place in. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id for this venue   
</details>

<details>
<summary>name : str = None  </summary>

* Name for this venue   
</details>

<details>
<summary>link : str  </summary>

* Link to venues endpoint   
</details>

</blockquote>

</details>

<details>
<summary>content : dict  </summary>

* Content for this game. Havent found a populated reference yet. Stays as dict  
</details>

<details>
<summary>istie : bool  </summary>

* If this game is a tie  
</details>

<details>
<summary>gamenumber : int  </summary>

* Game number for this game  
</details>

<details>
<summary>publicfacing : bool  </summary>

* Is this game public facing  
</details>

<details>
<summary>doubleheader : str  </summary>

* The double header status for this game, "n','y'?  
</details>

<details>
<summary>gamedaytype : str  </summary>

* The type of gameday for this game  
</details>

<details>
<summary>tiebreaker : str  </summary>

* Tie breaker for this game, 'n','y'?  
</details>

<details>
<summary>calendareventid : str  </summary>

* Calender event Id for this game  
</details>

<details>
<summary>seasondisplay : str  </summary>

* Displayed season for this game  
</details>

<details>
<summary>daynight : str  </summary>

* Day or night game as a string, 'am','pm'?  
</details>

<details>
<summary>scheduledinnings : int  </summary>

* Number of scheduled inning for the game  
</details>

<details>
<summary>reversehomeawaystatus : bool  </summary>

* If reverse home and away?  
</details>

<details>
<summary>inningbreaklength : int  </summary>

* Length of break between innings  
</details>

<details>
<summary>gamesinseries : int  </summary>

* Number of games in current series  
</details>

<details>
<summary>seriesgamenumber : int  </summary>

* Game number in the current series  
</details>

<details>
<summary>seriesdescription : str  </summary>

* Description of this current series  
</details>

<details>
<summary>recordsource : str  </summary>

* Record source   
</details>

<details>
<summary>ifnecessary : str  </summary>

* If necessary  
</details>

<details>
<summary>ifnecessarydescription : str  </summary>

* If necessary description  
</details>

<details>
<summary>rescheduledate : str  </summary>

* If game is rescheduled, this is the rescheduled date  
</details>

<details>
<summary>reschedulegamedate : str  </summary>

* rescheduled game date  
</details>

<details>
<summary>rescheduledfrom : str  </summary>

* rescheduled from  
</details>

<details>
<summary>rescheduledfromdate : str  </summary>

* rescheduled from date  
</details>

<details>
<summary>istie : bool  </summary>

* Is tie  
</details>

</blockquote>

</details>

<details>
<summary>events : list  </summary>

* A list of events for this date. Need to handle this but cant find a populated reference for this object. It stays as a list for now.  
</details>

</blockquote>

</details>


</blockquote>


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/schedule?sportId=1```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_schedule()
```