## Game Structure

**Attributes are expandable and collapsable - [Link to Game dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/game.py)**

<blockquote>

<details>
<summary>gamepk : int  </summary>

* id number of this game  
</details>

<details>
<summary>link : str  </summary>

* link to the api address for this game  
</details>

<details>
<summary>copyright : str  </summary>

* MLB AM copyright information  
</details>

<details>
<summary>metadata : MetaData  </summary>

* metaData of this game. Dataclass: [MetaData](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/attributes.py) 

<blockquote>

<details>
<summary>wait : int  </summary>

* No idea what this wait signifies  
</details>

<details>
<summary>timestamp : str  </summary>

* The timeStamp  
</details>

<details>
<summary>gameevents : List[str]  </summary>

* Current game events for this game  
</details>

<details>
<summary>logicalevents : List[str]  </summary>

* Current logical events for this game  
</details>


</blockquote>

</details>

<details>
<summary>gamedata : GameData  </summary>

* gameData of this game. Dataclass: [GameData](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/gamedata.py) 

<blockquote>

<details>
<summary>game : GameDataGame  </summary>

* game information about this game. Dataclass: [GameDataGame](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)  

<blockquote>

<details>
<summary>pk : int  </summary>

* This game's game id  
</details>

<details>
<summary>type : str  </summary>

* This game's game type code  
</details>

<details>
<summary>doubleheader : str  </summary>

* Represents if this game is a double header or not  
</details>

<details>
<summary>id : str  </summary>

* An unknown Id  
</details>

<details>
<summary>gamedaytype : str  </summary>

* This game's gameday type code  
</details>

<details>
<summary>tiebreaker : str  </summary>

* Is this game a tie breaker  
</details>

<details>
<summary>gamenumber : int  </summary>

* The game number for this game. If double header will be 2.  
</details>

<details>
<summary>calendareventid : str  </summary>

* The id for this calendar event  
</details>

<details>
<summary>season : str  </summary>

* This game's season year  
</details>

<details>
<summary>seasondisplay : str  </summary>

* This game's displayed season  
</details>


</blockquote>

</details>

<details>
<summary>datetime : GameDatetime  </summary>

* Time and dates for this game. Dataclass: [GameDatetime](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

<blockquote>

<details>
<summary>datetime : str  </summary>

* Date time for this game  
</details>

<details>
<summary>originaldate : str  </summary>

* The original scheduled date for this game  
</details>

<details>
<summary>officialdate : str  </summary>

* The current scheduled date for this game  
</details>

<details>
<summary>daynight : str  </summary>

* The current lighting condition game type  
</details>

<details>
<summary>time : str  </summary>

* The time  
</details>

<details>
<summary>ampm : str  </summary>

* The games am or pm code  
</details>


</blockquote>

</details>

<details>
<summary>status : GameStatus  </summary>

* information on this game's status. Dataclass: [GameStatus](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

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
<summary>teams : GameTeams  </summary>

* Our two teams for this game, home and away. Dataclass: [GameTeams](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

<blockquote>

<details>
<summary>away : Team  </summary>

* Away team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

<blockquote>

<details>
<summary>springleague : League  </summary>

* The spring league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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


</blockquote>

</details>

<details>
<summary>allstarstatus : str  </summary>

* The all status status of the team  
</details>

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

* The API link for the team  
</details>

<details>
<summary>season : str  </summary>

* The team's current season  
</details>

<details>
<summary>venue : Venue  </summary>

* The team's home venue. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id for this venue  
</details>

<details>
<summary>name : str  </summary>

* Name for this venue  
</details>

<details>
<summary>link : str  </summary>

* Link to venues endpoint  
</details>


</blockquote>

</details>

<details>
<summary>springvenue : Venue  </summary>

* The team's spring venue. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id for this venue  
</details>

<details>
<summary>link : str  </summary>

* Link to venues endpoint  
</details>

</blockquote>

</details>

<details>
<summary>teamcode : str  </summary>

* team code   
</details>

<details>
<summary>filecode : str  </summary>

* filecode name of the team  
</details>

<details>
<summary>abbreviation : str  </summary>

* The abbreviation of the team name  
</details>

<details>
<summary>teamname : str  </summary>

* The team name   
</details>

<details>
<summary>locationname : str  </summary>

* The location of the team  
</details>

<details>
<summary>firstyearofplay : str  </summary>

* The first year the team began play  
</details>

<details>
<summary>league : League  </summary>

* The league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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
<summary>division : Division  </summary>

* The division the team is in. Dataclass: [Division](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/divisions/division.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the divison  
</details>

<details>
<summary>name : str  </summary>

* name of the division  
</details>

<details>
<summary>link : str  </summary>

* link of the division  
</details>


</blockquote>

</details>

<details>
<summary>sport : Sport  </summary>

* The sport of the team. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the sport  
</details>

<details>
<summary>name : str  </summary>

* name the sport  
</details>

<details>
<summary>link : str </summary>

* link of the sport  
</details>


</blockquote>

</details>

<details>
<summary>shortname : str  </summary>

* The shortname of the team  
</details>

<details>
<summary>record : TeamRecord  </summary>

* The record of the team. Dataclass: [TeamRecord](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/attributes.py)

<blockquote>

<details>
<summary>gamesplayed : int  </summary>

* Number of game played by team  
</details>

<details>
<summary>wildcardgamesback : str  </summary>

* Number of game back from wildcard  
</details>

<details>
<summary>leaguegamesback : str  </summary>

* Number of league games back  
</details>

<details>
<summary>springleaguegamesback : str  </summary>

* Number of game back in spring league  
</details>

<details>
<summary>sportgamesback : str  </summary>

* Number of games back in sport  
</details>

<details>
<summary>divisiongamesback : str  </summary>

* Number of games back in division  
</details>

<details>
<summary>conferencegamesback : str  </summary>

* Number of games back in conference  
</details>

<details>
<summary>leaguerecord : Dict  </summary>

* Record in league  
</details>

<details>
<summary>records : Dict  </summary>

* Records  
</details>

<details>
<summary>divisionleader : bool  </summary>

* Is this team a divison leader  
</details>

<details>
<summary>wins : int  </summary>

* Number of wins  
</details>

<details>
<summary>losses : int  </summary>

* Number of losses  
</details>

<details>
<summary>winningpercentage : str  </summary>

* Winning percentage  
</details>


</blockquote>

</details>

<details>
<summary>franchisename : str  </summary>

* The franchisename of the team  
</details>

<details>
<summary>clubname : str  </summary>

* The clubname of the team  
</details>

<details>
<summary>active : str  </summary>

* Active status of the team  
</details>


</blockquote>

</details>

<details>
<summary>home : Team  </summary>

* Home team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)


<blockquote>

<details>
<summary>springleague : League  </summary>

* The spring league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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


</blockquote>

</details>

<details>
<summary>allstarstatus : str  </summary>

* The all status status of the team  
</details>

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

* The API link for the team  
</details>

<details>
<summary>season : str  </summary>

* The team's current season  
</details>

<details>
<summary>venue : Venue  </summary>

* The team's home venue. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id for this venue  
</details>

<details>
<summary>name : str  </summary>

* Name for this venue  
</details>

<details>
<summary>link : str  </summary>

* Link to venues endpoint  
</details>


</blockquote>

</details>

<details>
<summary>springvenue : Venue  </summary>

* The team's spring venue. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id for this venue  
</details>

<details>
<summary>link : str  </summary>

* Link to venues endpoint  
</details>

</blockquote>

</details>

<details>
<summary>teamcode : str  </summary>

* team code   
</details>

<details>
<summary>filecode : str  </summary>

* filecode name of the team  
</details>

<details>
<summary>abbreviation : str  </summary>

* The abbreviation of the team name  
</details>

<details>
<summary>teamname : str  </summary>

* The team name   
</details>

<details>
<summary>locationname : str  </summary>

* The location of the team  
</details>

<details>
<summary>firstyearofplay : str  </summary>

* The first year the team began play  
</details>

<details>
<summary>league : League  </summary>

* The league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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
<summary>division : Division  </summary>

* The division the team is in. Dataclass: [Division](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/divisions/division.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the divison  
</details>

<details>
<summary>name : str  </summary>

* name of the division  
</details>

<details>
<summary>link : str  </summary>

* link of the division  
</details>


</blockquote>

</details>

<details>
<summary>sport : Sport  </summary>

* The sport of the team. Dataclass: [Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the sport  
</details>

<details>
<summary>name : str  </summary>

* name the sport  
</details>

<details>
<summary>link : str </summary>

* link of the sport  
</details>


</blockquote>

</details>

<details>
<summary>shortname : str  </summary>

* The shortname of the team  
</details>

<details>
<summary>record : TeamRecord  </summary>

* The record of the team. Dataclass: [TeamRecord](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/attributes.py)

<blockquote>

<details>
<summary>gamesplayed : int  </summary>

* Number of game played by team  
</details>

<details>
<summary>wildcardgamesback : str  </summary>

* Number of game back from wildcard  
</details>

<details>
<summary>leaguegamesback : str  </summary>

* Number of league games back  
</details>

<details>
<summary>springleaguegamesback : str  </summary>

* Number of game back in spring league  
</details>

<details>
<summary>sportgamesback : str  </summary>

* Number of games back in sport  
</details>

<details>
<summary>divisiongamesback : str  </summary>

* Number of games back in division  
</details>

<details>
<summary>conferencegamesback : str  </summary>

* Number of games back in conference  
</details>

<details>
<summary>leaguerecord : Dict  </summary>

* Record in league  
</details>

<details>
<summary>records : Dict  </summary>

* Records  
</details>

<details>
<summary>divisionleader : bool  </summary>

* Is this team a divison leader  
</details>

<details>
<summary>wins : int  </summary>

* Number of wins  
</details>

<details>
<summary>losses : int  </summary>

* Number of losses  
</details>

<details>
<summary>winningpercentage : str  </summary>

* Winning percentage  
</details>


</blockquote>

</details>

<details>
<summary>franchisename : str  </summary>

* The franchisename of the team  
</details>

<details>
<summary>clubname : str  </summary>

* The clubname of the team  
</details>

<details>
<summary>active : str  </summary>

* Active status of the team  
</details>


</blockquote>

</details>


</blockquote>

</details>

<details>
<summary>players : List[Person]  </summary>

* A list of all the players for this game. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person  
</details>

<details>
<summary>primaryposition : str  </summary>

* PrimaryPosition of the Person  
</details>

<details>
<summary>pitchhand : str  </summary>

* PitchHand of the Person  
</details>

<details>
<summary>batside : str  </summary>

* BatSide of the Person  
</details>

<details>
<summary>fullname : str  </summary>

* full name of the Person  
</details>

<details>
<summary>firstname : str  </summary>

* First name of the Person  
</details>

<details>
<summary>lastname : str  </summary>

* Last name of the Person  
</details>

<details>
<summary>primarynumber : str  </summary>

* Primary number of the Person  
</details>

<details>
<summary>birthdate : str  </summary>

* Birth date of the Person  
</details>

<details>
<summary>currentteam : str  </summary>

* The current Team of the Person  
</details>

<details>
<summary>currentage : str  </summary>

* The current age of the Person  
</details>

<details>
<summary>birthcity : str  </summary>

* The birthcity of the Person  
</details>

<details>
<summary>birthstateprovince : str  </summary>

* The province of the birth state  
</details>

<details>
<summary>height : str  </summary>

* The height of the Person  
</details>

<details>
<summary>weight : str  </summary>

* The weight of the Person  
</details>

<details>
<summary>active : str  </summary>

* The active status of the Person  
</details>

<details>
<summary>usename : str  </summary>

* The use name of the Person  
</details>

<details>
<summary>middlename : str  </summary>

* The middle name of the Person  
</details>

<details>
<summary>boxscorename : str  </summary>

* The box score name of the Person  
</details>

<details>
<summary>nickname : str  </summary>

* The nickname of the Person  
</details>

<details>
<summary>draftyear : int  </summary>

* The draft year of the Person  
</details>

<details>
<summary>mlbdebutdate : str  </summary>

* The MLB debut date of the Person  
</details>

<details>
<summary>namefirstlast : str  </summary>

* The first and last name of the Person  
</details>

<details>
<summary>nameslug : str  </summary>

* The name slug of the Person  
</details>

<details>
<summary>firstlastname : str  </summary>

* The first and last name of the Person  
</details>

<details>
<summary>lastfirstname : str  </summary>

* The last and first name of the Person  
</details>

<details>
<summary>lastinitname : str  </summary>

* The last init name of the Person  
</details>

<details>
<summary>initlastname : str  </summary>

* The init last name of the Person  
</details>

<details>
<summary>fullfmlname : str  </summary>

* The full fml name of the Person  
</details>

<details>
<summary>fulllfmname : str  </summary>

* The full lfm name of the Person  
</details>

<details>
<summary>uselastname : str  </summary>

* The last name of the  
</details>

<details>
<summary>birthcountry : str  </summary>

* The birth country of the Person  
</details>

<details>
<summary>pronunciation : str  </summary>

* The pronuciation of the Person's name  
</details>

<details>
<summary>strikezonetop : float  </summary>

* The strike zone top of the Person  
</details>

<details>
<summary>strikezonebottom : float  </summary>

* The strike zone bottom of the Person  
</details>

<details>
<summary>nametitle : str  </summary>

* The name title of the Person  
</details>

<details>
<summary>gender : str  </summary>

* The gender of the Person  
</details>

<details>
<summary>isplayer : bool  </summary>

* The player status of the Person  
</details>

<details>
<summary>isverified : bool  </summary>

* The verification of the Person  
</details>

<details>
<summary>namematrilineal : str  </summary>

* The name matrilineal of the Person  
</details>

<details>
<summary>deathdate : str  </summary>

* The death date of the Person  
</details>

<details>
<summary>deathcity : str  </summary>

* The death city of the Person  
</details>

<details>
<summary>deathcountry : str  </summary>

* The death country of the Person  
</details>

<details>
<summary>lastplayeddate : str  </summary>

* The last played date of the Person  
</details>

<details>
<summary>namesuffix : str  </summary>

* The namesuffix of the Person  
</details>

</blockquote>

</details>

<details>
<summary>venue : Venue  </summary>

* Venue information for this game. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id for this venue  
</details>

<details>
<summary>name : str  </summary>

* Name for this venue  
</details>

<details>
<summary>link : str  </summary>

* Link to venues endpoint  
</details>

<details>
<summary>location : Location  </summary>

* Location for this venue. Dataclass: [Location](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/attributes.py)

<blockquote>

<details>
<summary>address1 : str  </summary>

* Venues first address line  
</details>

<details>
<summary>address2 : str  </summary>

* Venues second address line  
</details>

<details>
<summary>city : str  </summary>

* City the venue is in  
</details>

<details>
<summary>state : str  </summary>

* The State the venue is in  
</details>

<details>
<summary>stateAbbrev : str  </summary>

* The staes abbreviation  
</details>

<details>
<summary>postalCode : str  </summary>

* Postal code for this venue  
</details>

<details>
<summary>defaultCoordinates : VenueDefaultCoordinates  </summary>

* Long and lat for this venues location. Dataclass: [VenueDefaultCoordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/attributes.py)

<blockquote>

<details>
<summary>latitude : float </summary>

* The latatude coordinate for this venue  
</details>

<details>
<summary>longitude : float </summary>

* The longitude coordinate for this venue  
</details>

</blockquote>

</details>

<details>
<summary>country : str  </summary>

* What country this venue is in  
</details>

<details>
<summary>phone : str  </summary>

* Phone number for this venue  
</details>

</blockquote>

</details>

<details>
<summary>timezone : TimeZone  </summary>

* Timezone for this venue. Dataclass: [VenueTimeZone](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/attributes.py)

<blockquote>

<details>
<summary>id : str  </summary>

* id string for a venues timezone  
</details>

<details>
<summary>offset : int  </summary>

* The offset for this timezone from  
</details>

<details>
<summary>tz : str  </summary>

* Timezone string  
</details>

</blockquote>

</details>

<details>
<summary>fieldinfo :  FieldInfo  </summary>

* Info on this venue's field. Dataclass: [FieldInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/attributes.py)

<blockquote>

<details>
<summary>capacity : int  </summary>

* Capacity for this venue  
</details>

<details>
<summary>turfType : str  </summary>

* The type of turf in this venue  
</details>

<details>
<summary>roofType : str  </summary>

* What kind of roof for this venue  
</details>

<details>
<summary>leftLine : int  </summary>

* Distance down the left line  
</details>

<details>
<summary>left : int  </summary>

* Distance to left  
</details>

<details>
<summary>leftCenter : int  </summary>

* Distance to left center  
</details>

<details>
<summary>center : int  </summary>

* Distance to center  
</details>

<details>
<summary>rightCenter : int  </summary>

* Distance to right center  
</details>

<details>
<summary>right : int  </summary>

* Distance to right  
</details>

<details>
<summary>rightLine : int  </summary>

* Distance to right line  
</details>

</blockquote>

</details>

<details>
<summary>active : bool  </summary>

* Is this field currently active  
</details>


</blockquote>

</details>

<details>
<summary>officialvenue : Venue  </summary>

* The official venue for this game. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venues/venue.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id for this venue  
</details>

<details>
<summary>link : str  </summary>

* Link to venues endpoint  
</details>

</blockquote>

</details>

<details>
<summary>weather : GameWeather  </summary>

* The weather for this game. Dataclass: [GameWeather](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

<blockquote>

<details>
<summary>condition : str  </summary>

* The weather condition  
</details>

<details>
<summary>temp : str  </summary>

* The temperature in F  
</details>

<details>
<summary>wind : str  </summary>

* The wind in MPH and the direction  
</details>

</blockquote>

</details>

<details>
<summary>gameinfo : GameInfo  </summary>

* information on this game. Dataclass: [GameInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

<blockquote>

<details>
<summary>attendance : int  </summary>

* The attendance for this game  
</details>

<details>
<summary>firstpitch : str  </summary>

* The time of the first pitch  
</details>

<details>
<summary>gamedurationminutes : int  </summary>

* The duration of the game in minutes  
</details>

<details>
<summary>delaydurationminutes : int  </summary>

* The length of delay for the game in minutes  
</details>

</blockquote>

</details>

<details>
<summary>review : GameReview  </summary>

* Game review info and team challenges. Dataclass: [GameReview](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

<blockquote>

<details>
<summary>haschallenges : bool  </summary>

* If their are challenges  
</details>

<details>
<summary>away : ReviewInfo  </summary>

* Away team review info. Dataclass: [ReviewInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)  

<blockquote>

<details>
<summary>used : int  </summary>

* How many challenges used  
</details>

<details>
<summary>remaining : int  </summary>

* How many challenges are remaining  
</details>

</blockquote>

</details>

<details>
<summary>home : ReviewInfo  </summary>

* Home team review info. Dataclass: [ReviewInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)    

<blockquote>

<details>
<summary>used : int  </summary>

* How many challenges used  
</details>

<details>
<summary>remaining : int  </summary>

* How many challenges are remaining  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>flags : GameFlags  </summary>

* Flag bools for this game. Dataclass: [GameFlags](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

<blockquote>

<details>
<summary>nohitter : bool  </summary>

* If there is a no hitter in this game  
</details>

<details>
<summary>perfectgame :  bool  </summary>

* If there this game is a perfect game  
</details>

<details>
<summary>awayteamnohitter : bool  </summary>

* If the away team has a no hitter  
</details>

<details>
<summary>awayteamperfectgame : bool  </summary>

* If the away team has a perfect game  
</details>

<details>
<summary>hometeamnohitter : bool  </summary>

* If the home team has a no hitter  
</details>

<details>
<summary>hometeamperfectgame : bool  </summary>

* If the home team has a perfect game  
</details>

</blockquote>

</details>

<details>
<summary>alerts : List[]  </summary>

* Alerts  
</details>

<details>
<summary>probablepitchers : GameProbablePitchers  </summary>

* Home and away probable pitchers for this game. Dataclass: [GameProbablePitchers](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/gamedata/attributes.py)

<blockquote>

<details>
<summary>home : Person  </summary>

* Home team probable pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person  
</details>

<details>
<summary>link : str  </summary>

* Link to person  
</details>

</blockquote>

</details>

<details>
<summary>away : Person  </summary>

* Away team probable pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person  
</details>

<details>
<summary>link : str  </summary>

* Link to person  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>officialscorer : Person  </summary>

* The official scorer for this game. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person  
</details>

<details>
<summary>link : str  </summary>

* Link to person  
</details>

</blockquote>

</details>

<details>
<summary>primarydatacaster : Person  </summary>

* The official dataCaster for this game. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person  
</details>

<details>
<summary>link : str  </summary>

* Link to person  
</details>

</blockquote>

</details>


</blockquote>

</details>

<details>
<summary>livedata : LiveData  </summary>

* liveData of this game. Dataclass: [LiveData](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/livedata.py)

<blockquote>

<details>
<summary>plays : Plays  </summary>

* Has the plays for this game. Dataclass: [Plays](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/plays.py)  

<blockquote>

<details>
<summary>allplays : List[Play] </summary>

* All the plays in this game. Dataclass: [Play](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/play.py)

<blockquote>

<details>
<summary>result : PlayResult </summary>

* Play result. Dataclass: [PlayResult](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/attributes.py)

<blockquote>

<details>
<summary>type : str </summary>

* Play result type  
</details>

<details>
<summary>event : str </summary>

* Play event  
</details>

<details>
<summary>eventtype : str </summary>

* Event type  
</details>

<details>
<summary>description : str </summary>

* Event description  
</details>

<details>
<summary>rbi : int </summary>

* Number of RBI's  
</details>

<details>
<summary>awayscore : int </summary>

* Score for away team  
</details>

<details>
<summary>homescore : int </summary>

* Score for home team  
</details>

<details>
<summary>isout : bool </summary>

* If the play was an out  
</details>

</blockquote>

</details>

<details>
<summary>about : PlayAbout </summary>

* Information about this play. Dataclass: [PlayAbout](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/attributes.py)

<blockquote>

<details>
<summary>atbatindex : int </summary>

* Current at bat index  
</details>

<details>
<summary>halfinning : str </summary>

* What side of the inning  
</details>

<details>
<summary>istopinning : bool </summary>

* Is this inning the top of the inning  
</details>

<details>
<summary>inning : int </summary>

* What number of inning we are in  
</details>

<details>
<summary>starttime : str </summary>

* The start time for this play  
</details>

<details>
<summary>endtime : str </summary>

* The end time for this play  
</details>

<details>
<summary>iscomplete : bool </summary>

* Is this play complete  
</details>

<details>
<summary>isscoringplay : bool </summary>

* is this play a scoring play  
</details>

<details>
<summary>hasreview : bool </summary>

* Dose this play have a review  
</details>

<details>
<summary>hasout : bool </summary>

* Does this play have a out  
</details>

<details>
<summary>captivatingindex : int </summary>

* What is the captivating index for this play  
</details>

</blockquote>

</details>

<details>
<summary>count : PlayCount </summary>

* This plays count. Dataclass: [PlayCount](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>balls : int </summary>

* Number of balls  
</details>

<details>
<summary>strikes : int </summary>

* Strike count  
</details>

<details>
<summary>outs : int </summary>

* Number of outs  
</details>

</blockquote>

</details>

<details>
<summary>matchup : PlayMatchup </summary>

* This plays matchup. Dataclass: [PlayMatchup](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/matchup/matchup.py)

<blockquote>

<details>
<summary>batter : Person </summary>

* Matchup batter. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>

</details>

<details>
<summary>batside : CodeDesc </summary>

* batters batside. [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* Code to reference batside  
</details>

<details>
<summary>description : str </summary>

* Description of the batside  
</details>

</blockquote>

</details>

<details>
<summary>pitcher : Person </summary>

* Matchup pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>

</details>

<details>
<summary>pitchhand : PlayMatchupSide </summary>

* Pitchers side. [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* Code to reference pitchside  
</details>

<details>
<summary>description : str </summary>

* Description of the pitchside  
</details>

</blockquote>
  
</details>

<details>
<summary>batterhotcoldzones : List </summary>

* Batter hot and cold zones  
</details>

<details>
<summary>pitcherhotcoldzones : List </summary>

* Pitcher hot and cold zones  
</details>

<details>
<summary>splits : PlayMatchupSplits </summary>

* PlayMatchupSplits. Dataclass: [PlayMatchupSplits](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/matchup/attributes.py)  

<blockquote>

<details>
<summary>batter : str </summary>

* Batter play split  
</details>

<details>
<summary>pitcher : str </summary>

* Pitcher  play split  
</details>

<details>
<summary>menonbase : str </summary>

* Menonbase play split  
</details>

</blockquote>

</details>

<details>
<summary>postonfirst : Person </summary>

* Runner on first if on base. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>

</details>

<details>
<summary>postonsecond : Person </summary>

* Runner on second if on base. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>

</details>

<details>
<summary>postonthird : Person </summary>

* Runner on third if on base. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>
  
</details>

</blockquote>


</details>

<details>
<summary>pitchindex : List[int] </summary>

* Pitch index for this play, indexing playEvents  
</details>

<details>
<summary>actionindex : List[int] </summary>

* Action index for this play, indexing playEvents  
</details>

<details>
<summary>runnerindex : List[int] </summary>

* Runner index for this play, indexing runners  
</details>

<details>
<summary>runners : List[PlayRunner] </summary>

* Runners. Dataclass: [PlayRunner](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playrunner/playrunner.py)

<blockquote>

<details>
<summary>movement: RunnerMovement </summary>

* Runner movements. Dataclass: [RunnerMovement](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playrunner/attributes.py) 

<blockquote>

<details>
<summary>isout: bool </summary>

* Was the running movement an out  
</details>

<details>
<summary>outnumber: int </summary>

* What is the outnumber  
</details>

<details>
<summary>originbase: str </summary>

* Original base  
</details>

<details>
<summary>start: str </summary>

* What base the runner started from  
</details>

<details>
<summary>end: str </summary>

* What base the runner ended at  
</details>

<details>
<summary>outbase: str </summary>

* Base runner was made out  
</details>

</blockquote>

</details>

<details>
<summary>details: RunnerDetails </summary>

* Runner details. Dataclass: [RunnerDetails](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playrunner/attributes.py)  

<blockquote>

<details>
<summary>event: str </summary>

* Runner event  
</details>

<details>
<summary>eventtype: str </summary>

* Runner event type  
</details>

<details>
<summary>runner: Person </summary>

* Who the runner is. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* full_name of the person  
</details>

<details>
<summary>link : str </summary>

* Link to person  
</details>

</blockquote>

</details>

<details>
<summary>isscoringevent:  bool </summary>

* Was this a scoring events  
</details>

<details>
<summary>rbi: bool </summary>

* Was this a rbi  
</details>

<details>
<summary>earned: bool </summary>

* Was it earned  
</details>

<details>
<summary>teamunearned: bool </summary>

* Was it unearned  
</details>

<details>
<summary>playindex: int </summary>

* Play index  
</details>

<details>
<summary>movementreason: str </summary>

* Reason for the movement  
</details>

<details>
<summary>responsiblepitcher: Person </summary>

* Who was the responsible pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>link : str </summary>

* Link to person  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>credits: List[RunnerCredits] </summary>

* Runner credits. Dataclass: [RunnerCredits](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playrunner/attributes.py)

<blockquote>

<details>
<summary>player: Person </summary>

* The player. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>link : str </summary>

* Link to person  
</details>

</blockquote>

</details>

<details>
<summary>position: RunnerCreditsPosition </summary>

* The position. Dataclass: [RunnerCreditsPosition](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

<blockquote>

<details>
<summary>code: str </summary>

* code number of the Position  
</details>

<details>
<summary>name: str </summary>

* the name of the Position  
</details>

<details>
<summary>type: str </summary>

* the type of the Position  
</details>

<details>
<summary>abbreviation: str </summary>

* the abbreviation of the Position  
</details>

</blockquote>

</details>

<details>
<summary>credit: str </summary>

* The credit  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>playevents : List[PlayEvent] </summary>

* Play events. Dataclass: [PlayEvent](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playevent/playevent.py)

<blockquote>

<details>
<summary>details : PlayDetails </summary>

* Event details. Dataclass: [PlayDetails](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>call : CodeDesc </summary>

* play call code and description. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code in reference to the call  
</details>

<details>
<summary>description : str </summary>

* the description of the call  
</details>

</blockquote>

</details>

<details>
<summary>description : str </summary>

* description of the play  
</details>

<details>
<summary>event : str </summary>

* type of event  
</details>

<details>
<summary>eventtype : str </summary>

* type of event  
</details>

<details>
<summary>isinplay : bool </summary>

* is the ball in play true or false  
</details>

<details>
<summary>isstrike : bool </summary>

* is the ball a strike true or false  
</details>

<details>
<summary>isball : bool </summary>

* is it a ball true or false  
</details>

<details>
<summary>isbasehit : bool </summary>

* is the event a base hit true or false  
</details>

<details>
<summary>isatbat : bool </summary>

* is the event at bat true or false  
</details>

<details>
<summary>isplateappearance : bool </summary>

* is the event a at play appears true or false  
</details>

<details>
<summary>type : CodeDesc </summary>

* type of pitch code and description. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code in reference to the type  
</details>

<details>
<summary>description : str </summary>

* the description of the type  
</details>

</blockquote>
  
</details>

<details>
<summary>batside : CodeDesc </summary>

* bat side code and description. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code in reference to the batside  
</details>

<details>
<summary>description : str </summary>

* the description of the batside  
</details>

</blockquote>
  
</details>

<details>
<summary>pitchhand : CodeDesc </summary>

* pitch hand code and description. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code in reference to the pitchhand  
</details>

<details>
<summary>description : str </summary>

* the description of the pitchhand  
</details>

</blockquote>
  
</details>

<details>
<summary>fromcatcher : bool </summary>

* From catcher  
</details>

</blockquote>

</details>

<details>
<summary>index : int </summary>

* Event index  
</details>

<details>
<summary>starttime : str </summary>

* Event start time  
</details>

<details>
<summary>endtime : str </summary>

* Event end time  
</details>

<details>
<summary>ispitch : bool </summary>

* Is this event a pitch  
</details>

<details>
<summary>type : str </summary>

* Type  
</details>

<details>
<summary>playid : str </summary>

* Unique play id ?  
</details>

<details>
<summary>pitchnumber : int </summary>

* Pitch number  
</details>

<details>
<summary>actionplayid : str </summary>

* Unique action play id ?  
</details>

<details>
<summary>isbaserunningplay : bool </summary>

* Is there base running this play  
</details>

<details>
<summary>issubstitution : bool </summary>

* Is this a substitution  
</details>

<details>
<summary>battingorder : str </summary>

* A weird batting order string that only has appeared once  
</details>

<details>
<summary>count : PlayCount </summary>

* Count. Dataclass: [Count](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>balls : int </summary>

* number of balls  
</details>

<details>
<summary>strikes : int </summary>

* strike count  
</details>

<details>
<summary>outs : int </summary>

* number of outs  
</details>


</blockquote>

</details>

<details>
<summary>pitchdata : PitchData </summary>

* Pitch data. Dataclass: [PitchData](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>startspeed : float </summary>

* The starting speed of the pitch.  
</details>

<details>
<summary>endspeed : float </summary>

* The ending speed of the pitch.  
</details>

<details>
<summary>strikezonetop : float </summary>

* The top of the strike zone.  
</details>

<details>
<summary>strikezonebottom : float </summary>

* The bottom of the strike zone.  
</details>

<details>
<summary>coordinates : PitchCoordinates </summary>

* The coordinates of the pitch. Dataclass: [PitchCoordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py) 

<blockquote>

<details>
<summary>ay : float </summary>

* Ball acceleration on the y axis  
</details>

<details>
<summary>az : float </summary>

* Ball acceleration on the z axis  
</details>

<details>
<summary>pfxx : float </summary>

* horizontal movement of the ball in inches  
</details>

<details>
<summary>pfxz : float </summary>

* Vertical movement of the ball in inches  
</details>

<details>
<summary>px : float </summary>

* Horizontal position in feet of the ball as it crosses the front axis of home plate  
</details>

<details>
<summary>pz : float </summary>

* Vertical position in feet of the ball as it crosses the front axis of home plate  
</details>

<details>
<summary>vx0 : float </summary>

* Velocity of the ball from the x-axis  
</details>

<details>
<summary>vy0 : float </summary>

* Velocity of the ball from the y axis, this is negative becuase 0,0,0 is behind the batter and the ball travels from pitcher mound towards 0,0,0  
</details>

<details>
<summary>vz0 : float </summary>

* Velocity of the ball from the z axis  
</details>

<details>
<summary>x0 : float </summary>

* Coordinate location of the ball at the point it was reeased from pitchers hand on the x axis (time=0)  
</details>

<details>
<summary>y0 : float </summary>

* Coordinate location of the ball at the point it was reeased from pitchers hand on the y axis (time=0)  
</details>

<details>
<summary>z0 : float </summary>

* Coordinate location of the ball at the point it was reeased from pitchers hand on the z axis (time=0)  
</details>

<details>
<summary>ax : float </summary>

* Ball acceleration on the x axis  
</details>

<details>
<summary>x : float </summary>

* X coordinate where pitch crossed front of home plate  
</details>

<details>
<summary>y : float </summary>

* Y coordinate where pitch crossed front of home plate  
</details>

</blockquote>

</details>

<details>
<summary>breaks : PitchBreak </summary>

* The break data of the pitch. Dataclass: [PitchBreak](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py) 

<blockquote>

<details>
<summary>breakangle : float </summary>

* Degrees clockwise (batter's view) that the plane of the pitch deviates from the vertical  
</details>

<details>
<summary>breaklength : float </summary>

* Max distance that the pitch separates from the straight line between pitch start and pitch end  
</details>

<details>
<summary>breaky : int </summary>

* Distance from home plate where the break is greatest  
</details>

<details>
<summary>spinrate : int </summary>

* Pitch spinRate  
</details>

<details>
<summary>spindirection : int </summary>

* Pitch spinDirection  
</details>

</blockquote>

</details>

<details>
<summary>zone : float </summary>

* The zone in which the pitch was thrown.  
</details>

<details>
<summary>typeconfidence : float </summary>

* The confidence in the type of pitch thrown.  
</details>

<details>
<summary>platetime : float </summary>

* The amount of time the pitch was in the air.  
</details>

<details>
<summary>extension : float </summary>

* The extension of the pitch.  
</details>

</blockquote>

</details>

<details>
<summary>hitdata : HitData </summary>

* Hit data. Dataclass: [HitData](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>launchspeed : float </summary>

* Hit launch speed  
</details>

<details>
<summary>launchangle : int </summary>

* Hit launch angle  
</details>

<details>
<summary>totaldistance : int </summary>

* Hits total distance  
</details>

<details>
<summary>trajectory : str </summary>

* Hit trajectory  
</details>

<details>
<summary>hardness : str </summary>

* Hit hardness  
</details>

<details>
<summary>location : str </summary>

* Hit location  
</details>

<details>
<summary>coordinates : HitCoordinate </summary>

* Hit coordinates. Dataclass: [HitCoordinate](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>coordx : int </summary>

* X coordinate for hit.   
* Can also get this value with coordinates.x instead of coordinates.coordx
</details>

<details>
<summary>coordy : int </summary>

* Y coordinate for hit.   
* Can also get this value with coordinates.y instead of coordinates.coordy
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>player : Person </summary>

* Player. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>cid : int </summary>

* id number of the person
</details>

<details>
<summary>clink : str </summary>

* Link to person
</details>

</blockquote>

</details>

<details>
<summary>position : Position </summary>

* Position. Dataclass: [PrimaryPosition](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)  

<blockquote>

<details>
<summary>code: str </summary>

* code number of the Position
</details>

<details>
<summary>name: str </summary>

* the name of the Position
</details>

<details>
<summary>type: str </summary>

* the type of the Position
</details>

<details>
<summary>abbreviation: str </summary>

* the abbreviation of the Position
</details>

</blockquote>

</details>

<details>
<summary>replacedplayer : Person </summary>

* Replaced player. Dataclass [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)  

<blockquote>

<details>
<summary>cid : int </summary>

* id number of the person
</details>

<details>
<summary>clink : str </summary>

* Link to person
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>playendtime : str </summary>

* Time this play ends  
</details>

<details>
<summary>atbatindex : int </summary>

* The play index number  
</details>

<details>
<summary>reviewdetails : PlayReviewDetails </summary>

* Information on reviews if present. Dataclass: [PlayReviewDetails](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/attributes.py)

<blockquote>

<details>
<summary>isoverturned : bool </summary>

    Was it overturned  
</details>

<details>
<summary>inprogress : bool </summary>

    Is it in progress  
</details>

<details>
<summary>reviewtype : str </summary>

    What type of review  
</details>

<details>
<summary>challengeteamid : int </summary>

    The team issuing the challenge review  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>currentplay : Play </summary>

* The current play in this game. Dataclass: [Play](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/play.py)

<blockquote>

<details>
<summary>result : PlayResult </summary>

* Play result. Dataclass: [PlayResult](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/attributes.py)

<blockquote>

<details>
<summary>type : str </summary>

* Play result type  
</details>

<details>
<summary>event : str </summary>

* Play event  
</details>

<details>
<summary>eventtype : str </summary>

* Event type  
</details>

<details>
<summary>description : str </summary>

* Event description  
</details>

<details>
<summary>rbi : int </summary>

* Number of RBI's  
</details>

<details>
<summary>awayscore : int </summary>

* Score for away team  
</details>

<details>
<summary>homescore : int </summary>

* Score for home team  
</details>

<details>
<summary>isout : bool </summary>

* If the play was an out  
</details>

</blockquote>

</details>

<details>
<summary>about : PlayAbout </summary>

* Information about this play. Dataclass: [PlayAbout](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/attributes.py)

<blockquote>

<details>
<summary>atbatindex : int </summary>

* Current at bat index  
</details>

<details>
<summary>halfinning : str </summary>

* What side of the inning  
</details>

<details>
<summary>istopinning : bool </summary>

* Is this inning the top of the inning  
</details>

<details>
<summary>inning : int </summary>

* What number of inning we are in  
</details>

<details>
<summary>starttime : str </summary>

* The start time for this play  
</details>

<details>
<summary>endtime : str </summary>

* The end time for this play  
</details>

<details>
<summary>iscomplete : bool </summary>

* Is this play complete  
</details>

<details>
<summary>isscoringplay : bool </summary>

* is this play a scoring play  
</details>

<details>
<summary>hasreview : bool </summary>

* Dose this play have a review  
</details>

<details>
<summary>hasout : bool </summary>

* Does this play have a out  
</details>

<details>
<summary>captivatingindex : int </summary>

* What is the captivating index for this play  
</details>

</blockquote>

</details>

<details>
<summary>count : PlayCount </summary>

* This plays count. Dataclass: [PlayCount](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>balls : int </summary>

* Number of balls  
</details>

<details>
<summary>strikes : int </summary>

* Strike count  
</details>

<details>
<summary>outs : int </summary>

* Number of outs  
</details>

</blockquote>

</details>

<details>
<summary>matchup : PlayMatchup </summary>

* This plays matchup. Dataclass: [PlayMatchup](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/matchup/matchup.py)

<blockquote>

<details>
<summary>batter : Person </summary>

* Matchup batter. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>

</details>

<details>
<summary>batside : CodeDesc </summary>

* batters batside. [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* Code to reference batside  
</details>

<details>
<summary>description : str </summary>

* Description of the batside  
</details>

</blockquote>

</details>

<details>
<summary>pitcher : Person </summary>

* Matchup pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>

</details>

<details>
<summary>pitchhand : PlayMatchupSide </summary>

* Pitchers side. [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* Code to reference pitchside  
</details>

<details>
<summary>description : str </summary>

* Description of the pitchside  
</details>

</blockquote>
  
</details>

<details>
<summary>batterhotcoldzones : List </summary>

* Batter hot and cold zones  
</details>

<details>
<summary>pitcherhotcoldzones : List </summary>

* Pitcher hot and cold zones  
</details>

<details>
<summary>splits : PlayMatchupSplits </summary>

* PlayMatchupSplits. Dataclass: [PlayMatchupSplits](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/matchup/attributes.py)  

<blockquote>

<details>
<summary>batter : str </summary>

* Batter play split  
</details>

<details>
<summary>pitcher : str </summary>

* Pitcher  play split  
</details>

<details>
<summary>menonbase : str </summary>

* Menonbase play split  
</details>

</blockquote>

</details>

<details>
<summary>postonfirst : Person </summary>

* Runner on first if on base. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>

</details>

<details>
<summary>postonsecond : Person </summary>

* Runner on second if on base. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>

</details>

<details>
<summary>postonthird : Person </summary>

* Runner on third if on base. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* Id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* Full_name of the person  
</details>

<details>
<summary>link: str </summary>

* Persons link  
</details>

</blockquote>
  
</details>

</blockquote>


</details>

<details>
<summary>pitchindex : List[int] </summary>

* Pitch index for this play, indexing playEvents  
</details>

<details>
<summary>actionindex : List[int] </summary>

* Action index for this play, indexing playEvents  
</details>

<details>
<summary>runnerindex : List[int] </summary>

* Runner index for this play, indexing runners  
</details>

<details>
<summary>runners : List[PlayRunner] </summary>

* Runners. Dataclass: [PlayRunner](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playrunner/playrunner.py)

<blockquote>

<details>
<summary>movement: RunnerMovement </summary>

* Runner movements. Dataclass: [RunnerMovement](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playrunner/attributes.py) 

<blockquote>

<details>
<summary>isout: bool </summary>

* Was the running movement an out  
</details>

<details>
<summary>outnumber: int </summary>

* What is the outnumber  
</details>

<details>
<summary>originbase: str </summary>

* Original base  
</details>

<details>
<summary>start: str </summary>

* What base the runner started from  
</details>

<details>
<summary>end: str </summary>

* What base the runner ended at  
</details>

<details>
<summary>outbase: str </summary>

* Base runner was made out  
</details>

</blockquote>

</details>

<details>
<summary>details: RunnerDetails </summary>

* Runner details. Dataclass: [RunnerDetails](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playrunner/attributes.py)  

<blockquote>

<details>
<summary>event: str </summary>

* Runner event  
</details>

<details>
<summary>eventtype: str </summary>

* Runner event type  
</details>

<details>
<summary>runner: Person </summary>

* Who the runner is. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* full_name of the person  
</details>

<details>
<summary>link : str </summary>

* Link to person  
</details>

</blockquote>

</details>

<details>
<summary>isscoringevent:  bool </summary>

* Was this a scoring events  
</details>

<details>
<summary>rbi: bool </summary>

* Was this a rbi  
</details>

<details>
<summary>earned: bool </summary>

* Was it earned  
</details>

<details>
<summary>teamunearned: bool </summary>

* Was it unearned  
</details>

<details>
<summary>playindex: int </summary>

* Play index  
</details>

<details>
<summary>movementreason: str </summary>

* Reason for the movement  
</details>

<details>
<summary>responsiblepitcher: Person </summary>

* Who was the responsible pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>link : str </summary>

* Link to person  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>credits: List[RunnerCredits] </summary>

* Runner credits. Dataclass: [RunnerCredits](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playrunner/attributes.py)

<blockquote>

<details>
<summary>player: Person </summary>

* The player. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>link : str </summary>

* Link to person  
</details>

</blockquote>

</details>

<details>
<summary>position: RunnerCreditsPosition </summary>

* The position. Dataclass: [RunnerCreditsPosition](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

<blockquote>

<details>
<summary>code: str </summary>

* code number of the Position  
</details>

<details>
<summary>name: str </summary>

* the name of the Position  
</details>

<details>
<summary>type: str </summary>

* the type of the Position  
</details>

<details>
<summary>abbreviation: str </summary>

* the abbreviation of the Position  
</details>

</blockquote>

</details>

<details>
<summary>credit: str </summary>

* The credit  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>playevents : List[PlayEvent] </summary>

* Play events. Dataclass: [PlayEvent](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/playevent/playevent.py)

<blockquote>

<details>
<summary>details : PlayDetails </summary>

* Event details. Dataclass: [PlayDetails](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>call : CodeDesc </summary>

* play call code and description. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code in reference to the call  
</details>

<details>
<summary>description : str </summary>

* the description of the call  
</details>

</blockquote>

</details>

<details>
<summary>description : str </summary>

* description of the play  
</details>

<details>
<summary>event : str </summary>

* type of event  
</details>

<details>
<summary>eventtype : str </summary>

* type of event  
</details>

<details>
<summary>isinplay : bool </summary>

* is the ball in play true or false  
</details>

<details>
<summary>isstrike : bool </summary>

* is the ball a strike true or false  
</details>

<details>
<summary>isball : bool </summary>

* is it a ball true or false  
</details>

<details>
<summary>isbasehit : bool </summary>

* is the event a base hit true or false  
</details>

<details>
<summary>isatbat : bool </summary>

* is the event at bat true or false  
</details>

<details>
<summary>isplateappearance : bool </summary>

* is the event a at play appears true or false  
</details>

<details>
<summary>type : CodeDesc </summary>

* type of pitch code and description. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code in reference to the type  
</details>

<details>
<summary>description : str </summary>

* the description of the type  
</details>

</blockquote>
  
</details>

<details>
<summary>batside : CodeDesc </summary>

* bat side code and description. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code in reference to the batside  
</details>

<details>
<summary>description : str </summary>

* the description of the batside  
</details>

</blockquote>
  
</details>

<details>
<summary>pitchhand : CodeDesc </summary>

* pitch hand code and description. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code in reference to the pitchhand  
</details>

<details>
<summary>description : str </summary>

* the description of the pitchhand  
</details>

</blockquote>
  
</details>

<details>
<summary>fromcatcher : bool </summary>

* From catcher  
</details>

</blockquote>

</details>

<details>
<summary>index : int </summary>

* Event index  
</details>

<details>
<summary>starttime : str </summary>

* Event start time  
</details>

<details>
<summary>endtime : str </summary>

* Event end time  
</details>

<details>
<summary>ispitch : bool </summary>

* Is this event a pitch  
</details>

<details>
<summary>type : str </summary>

* Type  
</details>

<details>
<summary>playid : str </summary>

* Unique play id ?  
</details>

<details>
<summary>pitchnumber : int </summary>

* Pitch number  
</details>

<details>
<summary>actionplayid : str </summary>

* Unique action play id ?  
</details>

<details>
<summary>isbaserunningplay : bool </summary>

* Is there base running this play  
</details>

<details>
<summary>issubstitution : bool </summary>

* Is this a substitution  
</details>

<details>
<summary>battingorder : str </summary>

* A weird batting order string that only has appeared once  
</details>

<details>
<summary>count : PlayCount </summary>

* Count. Dataclass: [Count](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>balls : int </summary>

* number of balls  
</details>

<details>
<summary>strikes : int </summary>

* strike count  
</details>

<details>
<summary>outs : int </summary>

* number of outs  
</details>


</blockquote>

</details>

<details>
<summary>pitchdata : PitchData </summary>

* Pitch data. Dataclass: [PitchData](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>startspeed : float </summary>

* The starting speed of the pitch.  
</details>

<details>
<summary>endspeed : float </summary>

* The ending speed of the pitch.  
</details>

<details>
<summary>strikezonetop : float </summary>

* The top of the strike zone.  
</details>

<details>
<summary>strikezonebottom : float </summary>

* The bottom of the strike zone.  
</details>

<details>
<summary>coordinates : PitchCoordinates </summary>

* The coordinates of the pitch. Dataclass: [PitchCoordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py) 

<blockquote>

<details>
<summary>ay : float </summary>

* Ball acceleration on the y axis  
</details>

<details>
<summary>az : float </summary>

* Ball acceleration on the z axis  
</details>

<details>
<summary>pfxx : float </summary>

* horizontal movement of the ball in inches  
</details>

<details>
<summary>pfxz : float </summary>

* Vertical movement of the ball in inches  
</details>

<details>
<summary>px : float </summary>

* Horizontal position in feet of the ball as it crosses the front axis of home plate  
</details>

<details>
<summary>pz : float </summary>

* Vertical position in feet of the ball as it crosses the front axis of home plate  
</details>

<details>
<summary>vx0 : float </summary>

* Velocity of the ball from the x-axis  
</details>

<details>
<summary>vy0 : float </summary>

* Velocity of the ball from the y axis, this is negative becuase 0,0,0 is behind the batter and the ball travels from pitcher mound towards 0,0,0  
</details>

<details>
<summary>vz0 : float </summary>

* Velocity of the ball from the z axis  
</details>

<details>
<summary>x0 : float </summary>

* Coordinate location of the ball at the point it was reeased from pitchers hand on the x axis (time=0)  
</details>

<details>
<summary>y0 : float </summary>

* Coordinate location of the ball at the point it was reeased from pitchers hand on the y axis (time=0)  
</details>

<details>
<summary>z0 : float </summary>

* Coordinate location of the ball at the point it was reeased from pitchers hand on the z axis (time=0)  
</details>

<details>
<summary>ax : float </summary>

* Ball acceleration on the x axis  
</details>

<details>
<summary>x : float </summary>

* X coordinate where pitch crossed front of home plate  
</details>

<details>
<summary>y : float </summary>

* Y coordinate where pitch crossed front of home plate  
</details>

</blockquote>

</details>

<details>
<summary>breaks : PitchBreak </summary>

* The break data of the pitch. Dataclass: [PitchBreak](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py) 

<blockquote>

<details>
<summary>breakangle : float </summary>

* Degrees clockwise (batter's view) that the plane of the pitch deviates from the vertical  
</details>

<details>
<summary>breaklength : float </summary>

* Max distance that the pitch separates from the straight line between pitch start and pitch end  
</details>

<details>
<summary>breaky : int </summary>

* Distance from home plate where the break is greatest  
</details>

<details>
<summary>spinrate : int </summary>

* Pitch spinRate  
</details>

<details>
<summary>spindirection : int </summary>

* Pitch spinDirection  
</details>

</blockquote>

</details>

<details>
<summary>zone : float </summary>

* The zone in which the pitch was thrown.  
</details>

<details>
<summary>typeconfidence : float </summary>

* The confidence in the type of pitch thrown.  
</details>

<details>
<summary>platetime : float </summary>

* The amount of time the pitch was in the air.  
</details>

<details>
<summary>extension : float </summary>

* The extension of the pitch.  
</details>

</blockquote>

</details>

<details>
<summary>hitdata : HitData </summary>

* Hit data. Dataclass: [HitData](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>launchspeed : float </summary>

* Hit launch speed  
</details>

<details>
<summary>launchangle : int </summary>

* Hit launch angle  
</details>

<details>
<summary>totaldistance : int </summary>

* Hits total distance  
</details>

<details>
<summary>trajectory : str </summary>

* Hit trajectory  
</details>

<details>
<summary>hardness : str </summary>

* Hit hardness  
</details>

<details>
<summary>location : str </summary>

* Hit location  
</details>

<details>
<summary>coordinates : HitCoordinate </summary>

* Hit coordinates. Dataclass: [HitCoordinate](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>coordx : int </summary>

* X coordinate for hit.   
* Can also get this value with coordinates.x instead of coordinates.coordx
</details>

<details>
<summary>coordy : int </summary>

* Y coordinate for hit.   
* Can also get this value with coordinates.y instead of coordinates.coordy
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>player : Person </summary>

* Player. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>cid : int </summary>

* id number of the person
</details>

<details>
<summary>clink : str </summary>

* Link to person
</details>

</blockquote>

</details>

<details>
<summary>position : Position </summary>

* Position. Dataclass: [PrimaryPosition](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)  

<blockquote>

<details>
<summary>code: str </summary>

* code number of the Position
</details>

<details>
<summary>name: str </summary>

* the name of the Position
</details>

<details>
<summary>type: str </summary>

* the type of the Position
</details>

<details>
<summary>abbreviation: str </summary>

* the abbreviation of the Position
</details>

</blockquote>

</details>

<details>
<summary>replacedplayer : Person </summary>

* Replaced player. Dataclass [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)  

<blockquote>

<details>
<summary>cid : int </summary>

* id number of the person
</details>

<details>
<summary>clink : str </summary>

* Link to person
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>playendtime : str </summary>

* Time this play ends  
</details>

<details>
<summary>atbatindex : int </summary>

* The play index number  
</details>

<details>
<summary>reviewdetails : PlayReviewDetails </summary>

* Information on reviews if present. Dataclass: [PlayReviewDetails](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/play/attributes.py)

<blockquote>

<details>
<summary>isoverturned : bool </summary>

    Was it overturned  
</details>

<details>
<summary>inprogress : bool </summary>

    Is it in progress  
</details>

<details>
<summary>reviewtype : str </summary>

    What type of review  
</details>

<details>
<summary>challengeteamid : int </summary>

    The team issuing the challenge review  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>scoringplays : List[int] </summary>

* Which plays are scoring plays, indexed with allPlays  
</details>

<details>
<summary>playsbyinning : List[PlayByInning] </summary>

* Plays by inning. Dataclass: [PlayByInning](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/playbyinning/playbyinning.py)

<blockquote>

<details>
<summary>startindex : int </summary>

* Starting play index number, indexed with Plays.allPlays  
</details>

<details>
<summary>endindex : int </summary>

* End play index number, indexed with Plays.allPlays  
</details>

<details>
<summary>top : List[int] </summary>

* Play indexes for top of the inning  
</details>

<details>
<summary>bottom : List[int] </summary>

* play indexes for bottom of the inning  
</details>

<details>
<summary>hits : PlayByInningHits </summary>

* Hits for the inning by home and away. Dataclass: [PlayByInningHits](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/playbyinning/attributes.py)

<blockquote>

<details>
<summary>home : List[HitsByTeam] </summary>

* Home team hits. Dataclass: [HitsByTeam](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/playbyinning/attributes.py)

<blockquote>

<details>
<summary>team : Team </summary>

* This team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the team  
</details>

<details>
<summary>name : str </summary>

* name of the team  
</details>

<details>
<summary>link : str </summary>

* The API link for the team  
</details>

<details>
<summary>springleague : League </summary>

* The spring league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the league  
</details>

<details>
<summary>name : str </summary>

* name of the league  
</details>

<details>
<summary>link : str </summary>

* link of the league  
</details>

<details>
<summary>abbreviation : str </summary>

* abbreviation the league  
</details>

</blockquote>

</details>

<details>
<summary>allstarstatus : str </summary>

* The all status status of the team  
</details>

</blockquote>

</details>

<details>
<summary>inning : int </summary>

* This inning number  
</details>

<details>
<summary>pitcher : Person </summary>

* The pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* full_name of the person  
</details>

<details>
<summary>link : str </summary>

* link to person  
</details>

</blockquote>

</details>

<details>
<summary>batter : Person </summary>

* The batter. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* full_name of the person  
</details>

<details>
<summary>link : str </summary>

* link to person  
</details>

</blockquote>

</details>

<details>
<summary>coordinates : HitsByTeamHitCoordinates </summary>

* Hit coordinates. Dataclass: [HitCoordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/playbyinning/attributes.py)

<blockquote>

<details>
<summary>x : float </summary>

* X coordinate for hit  
</details>

<details>
<summary>y : float </summary>

* Y coordinate for hit  
</details>

</blockquote>

</details>

<details>
<summary>type : str </summary>

* Type  
</details>

<details>
<summary>description : str </summary>

* description  
</details>

</blockquote>

</details>

<details>
<summary>away : List[HitsByTeam] </summary>

* Away team hits. Dataclass: [HitsByTeam](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/playbyinning/attributes.py)

<blockquote>

<details>
<summary>team : Team </summary>

* This team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the team  
</details>

<details>
<summary>name : str </summary>

* name of the team  
</details>

<details>
<summary>link : str </summary>

* The API link for the team  
</details>

<details>
<summary>springleague : League </summary>

* The spring league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the league  
</details>

<details>
<summary>name : str </summary>

* name of the league  
</details>

<details>
<summary>link : str </summary>

* link of the league  
</details>

<details>
<summary>abbreviation : str </summary>

* abbreviation the league  
</details>

</blockquote>

</details>

<details>
<summary>allstarstatus : str </summary>

* The all status status of the team  
</details>

</blockquote>

</details>

<details>
<summary>inning : int </summary>

* This inning number  
</details>

<details>
<summary>pitcher : Person </summary>

* The pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* full_name of the person  
</details>

<details>
<summary>link : str </summary>

* link to person  
</details>

</blockquote>

</details>

<details>
<summary>batter : Person </summary>

* The batter. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int </summary>

* id number of the person  
</details>

<details>
<summary>full_name : str </summary>

* full_name of the person  
</details>

<details>
<summary>link : str </summary>

* link to person  
</details>

</blockquote>

</details>

<details>
<summary>coordinates : HitsByTeamHitCoordinates </summary>

* Hit coordinates. Dataclass: [HitCoordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/plays/playbyinning/attributes.py)

<blockquote>

<details>
<summary>x : float </summary>

* X coordinate for hit  
</details>

<details>
<summary>y : float </summary>

* Y coordinate for hit  
</details>

</blockquote>

</details>

<details>
<summary>type : str </summary>

* Type  
</details>

<details>
<summary>description : str </summary>

* description  
</details>

</blockquote>

</details>

</blockquote>

</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>linescore : Linescore  </summary>

* This games linescore. Dataclass: [Linescore](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/linescore/linescore.py)

<blockquote>

<details>
<summary>currentinning : int  </summary>

* The games current inning
</details>

<details>
<summary>currentinningordinal : str  </summary>

* This innings ordinal
</details>

<details>
<summary>inningstate : str  </summary>

* What state this inning is in
</details>

<details>
<summary>inninghalf : str  </summary>

* WHich half of the inning are we in
</details>

<details>
<summary>istopinning : bool  </summary>

* Is this the top of the inning
</details>

<details>
<summary>scheduledinnings : int  </summary>

* How many innings are scheduled for this game
</details>

<details>
<summary>innings : List[LinescoreInning]  </summary>

* Data on each inning. Dataclass: [LinescoreInning](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/linescore/attributes.py)

<blockquote>

<details>
<summary>num : int  </summary>

* Inning number
</details>

<details>
<summary>ordinalnum : str  </summary>

* Inning ordinal
</details>

<details>
<summary>home : LinescoreTeamScoreing  </summary>

* Home team inning info. Dataclass: [LinescoreTeamScoreing](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/linescore/attributes.py)

<blockquote>

<details>
<summary>hits : int  </summary>

* Team hits for this inning
</details>

<details>
<summary>errors : int  </summary>

* Team errors for this inning
</details>

<details>
<summary>leftonbase : int  </summary>

* Player left on base for this inning
</details>

<details>
<summary>runs : int  </summary>

* Team runs for this inning
</details>

<details>
<summary>iswinner : bool  </summary>

* If team is winner
</details>

</blockquote>

</details>

<details>
<summary>away : LinescoreTeamScoreing  </summary>

* Away team inning info. Dataclass: [LinescoreTeamScoreing](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/linescore/attributes.py)

<blockquote>

<details>
<summary>hits : int  </summary>

* Team hits for this inning
</details>

<details>
<summary>errors : int  </summary>

* Team errors for this inning
</details>

<details>
<summary>leftonbase : int  </summary>

* Player left on base for this inning
</details>

<details>
<summary>runs : int  </summary>

* Team runs for this inning
</details>

<details>
<summary>iswinner : bool  </summary>

* If team is winner
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>teams : LinescoreTeams  </summary>

* Line score data on our teams. Dataclas: [LinescoreTeams](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/linescore/attributes.py)

<blockquote>

<details>
<summary>home : LinescoreTeamScoreing  </summary>

* Home team current inning info

<blockquote>

<details>
<summary>hits : int  </summary>

* Team hits for this inning
</details>

<details>
<summary>errors : int  </summary>

* Team errors for this inning
</details>

<details>
<summary>leftonbase : int  </summary>

* Player left on base for this inning
</details>

<details>
<summary>runs : int  </summary>

* Team runs for this inning
</details>

<details>
<summary>iswinner : bool  </summary>

* If team is winner
</details>

</blockquote>

</details>

<details>
<summary>away : LinescoreTeamScoreing  </summary>

* Away team current inning info

<blockquote>

<details>
<summary>hits : int  </summary>

* Team hits for this inning
</details>

<details>
<summary>errors : int  </summary>

* Team errors for this inning
</details>

<details>
<summary>leftonbase : int  </summary>

* Player left on base for this inning
</details>

<details>
<summary>runs : int  </summary>

* Team runs for this inning
</details>

<details>
<summary>iswinner : bool  </summary>

* If team is winner
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>defense : LinescoreDefense  </summary>

* Current defense. Dataclass: [LinescoreDefense](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/linescore/attributes.py)

<blockquote>

<details>
<summary>pitcher : Person  </summary>

* Current pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>catcher : Person  </summary>

* Current catcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>first : Person  </summary>

* Current first. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>second : Person  </summary>

* Current second. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>third : Person  </summary>

* Current third. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>shortstop : Person  </summary>

* Current shortstop. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>left : Person  </summary>

* Current left. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>center : Person  </summary>

* Current center. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>right : Person  </summary>

* Current right. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>batter : Person  </summary>

* The next batter when this team switches to offense. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>ondeck : Person  </summary>

* The next ondeck batter when this team switches to offense. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>inhole : Person  </summary>

* The next inHole batter when this team switches to offense. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>battingorder : int  </summary>

* Number this team is in the batting order
</details>

<details>
<summary>team : Team  </summary>

* The team that is playing defense currently. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

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

* The API link for the team
</details>

</blockquote>

</details>


</blockquote>

</details>

<details>
<summary>offense : LinescoreOffense  </summary>

* Current offense. Dataclass: [LinescoreOffense](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/linescore/attributes.py)

<blockquote>

<details>
<summary>batter : Person  </summary>

* Current batter. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>ondeck : Person  </summary>

* Current on deck batter. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>inhole : Person  </summary>

* Current in the hole batter. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>pitcher : Person  </summary>

* Who is this teams pitcher. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* link to person
</details>

</blockquote>

</details>

<details>
<summary>battingorder : int  </summary>

* Number in the batting order
</details>

<details>
<summary>team : Team  </summary>

* The team currently on offense. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

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

* The API link for the team
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>balls : int  </summary>

* current count balls
</details>

<details>
<summary>strikes : int  </summary>

* current count strikes
</details>

<details>
<summary>outs : int  </summary>

* current count outs
</details>

</blockquote>

</details>

<details>
<summary>boxscore : BoxScore  </summary>

* This games boxscore. Dataclass: [BoxScore](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/boxscore.py)

<blockquote>

<details>
<summary>teams : BoxScoreTeams  </summary>

* Box score data for each team. Dataclass: [BoxScoreTeams](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>home : BoxScoreTeam  </summary>

* Home team boxscore information. Dataclass: [BoxScoreTeam](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>team : Team  </summary>

* This team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

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

* The API link for the team
</details>

<details>
<summary>springleague : League  </summary>

* The spring league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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

</blockquote>

</details>

<details>
<summary>allstarstatus : str  </summary>

* The all status status of the team
</details>

</blockquote>

</details>

<details>
<summary>teamstats : Dict  </summary>

* Team stats.
</details>

<details>
<summary>players : Dict  </summary>

* Players on team.   
* Access Key Format: ID+'player_id' : Person   

<blockquote>

<details>
<summary> Dict object accessed with Player_id.   ex. players[ID623457]</summary>

* Returned Person

<blockquote>

<details>
<summary>person : Person  </summary>

* The person object. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person.
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person.
</details>

<details>
<summary>link : str  </summary>

* Api access link for person.
</details>

</blockquote>

</details>

<details>
<summary>jerseynumber : str  </summary>

* The person's jersey number.
</details>

<details>
<summary>position : Position  </summary>

* The person's position. Dataclass: [Position](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

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
<summary>status : CodeDesc  </summary>

* The person's status. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code to reference the persons status
</details>

<details>
<summary>description : str </summary>

* the description of the status
</details>

</blockquote>

</details>

<details>
<summary>parentteamid : int  </summary>

* The ID of the person's parent team.
</details>

<details>
<summary>stats : dict  </summary>

* A dictionary of the person's stats.
</details>

<details>
<summary>seasonstats : dict  </summary>

* A dictionary of the person's season stats.
</details>

<details>
<summary>gameStatus : GameStatus  </summary>

* The person's game status. Dataclass: [GameStatus](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

<blockquote>

<details>
<summary>iscurrentbatter : bool  </summary>

* Whether the player is the current batter.
</details>

<details>
<summary>iscurrentpitcher : bool  </summary>

* Whether the player is the current pitcher.
</details>

<details>
<summary>isonbench : bool  </summary>

* Whether the player is on the bench.
</details>

<details>
<summary>issubstitute : bool  </summary>

* Whether the player is a substitute.
</details>

</blockquote>

</details>

<details>
<summary>battingorder : int  </summary>

* The persons place in the batting order if avaliable.
</details>

<details>
<summary>allpositions : List[Position]  </summary>

* All of the person's positions if avaliable. Dataclass: [Position](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

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

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>batters : List[int]  </summary>

* List of batters playerid for this team
</details>

<details>
<summary>pitchers : List[int]  </summary>

* List of pitcher playerid for this team
</details>

<details>
<summary>bench : List[int]  </summary>

* List of bench playerid for this team
</details>

<details>
<summary>bullpen : List[int]  </summary>

* Bullpen list of playerid
</details>

<details>
<summary>battingorder : List[int]  </summary>

* Batting order for this team as a list of playerid
</details>

<details>
<summary>info : List[BoxScoreTeamInfo]  </summary>

* Batting and fielding info for team. Dataclass: [BoxScoreTeamInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>title : str  </summary>

* Type of information
</details>

<details>
<summary>fieldlist : List[BoxScoreVL]  </summary>

* List holding the info for this info type. Dataclass: [BoxScoreVL](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>label : str  </summary>

* The label for this peice of info
</details>

<details>
<summary>value : str  </summary>

* The info associated with this label
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>note : List[str]  </summary>

* Team notes
</details>

</blockquote>

</details>

<details>
<summary>away : BoxScoreTeam  </summary>

* Away team boxscore information. Dataclass: [BoxScoreTeam](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>team : Team  </summary>

* This team. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

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

* The API link for the team
</details>

<details>
<summary>springleague : League  </summary>

* The spring league of the team. Dataclass: [League](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/leagues/league.py)

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

</blockquote>

</details>

<details>
<summary>allstarstatus : str  </summary>

* The all status status of the team
</details>

</blockquote>

</details>

<details>
<summary>teamstats : Dict  </summary>

* Team stats.
</details>

<details>
<summary>players : Dict  </summary>

* Players on team.   
* Access Key Format: ID+'player_id' : Person   

<blockquote>

<details>
<summary> Dict object accessed with Player_id.   ex. players[ID623457]</summary>

* Returned Person

<blockquote>

<details>
<summary>person : Person  </summary>

* The person object. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person.
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person.
</details>

<details>
<summary>link : str  </summary>

* Api access link for person.
</details>

</blockquote>

</details>

<details>
<summary>jerseynumber : str  </summary>

* The person's jersey number.
</details>

<details>
<summary>position : Position  </summary>

* The person's position. Dataclass: [Position](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

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
<summary>status : CodeDesc  </summary>

* The person's status. Dataclass: [CodeDesc](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/data/data.py)

<blockquote>

<details>
<summary>code : str </summary>

* the code to reference the persons status
</details>

<details>
<summary>description : str </summary>

* the description of the status
</details>

</blockquote>

</details>

<details>
<summary>parentteamid : int  </summary>

* The ID of the person's parent team.
</details>

<details>
<summary>stats : dict  </summary>

* A dictionary of the person's stats.
</details>

<details>
<summary>seasonstats : dict  </summary>

* A dictionary of the person's season stats.
</details>

<details>
<summary>gameStatus : GameStatus  </summary>

* The person's game status. Dataclass: [GameStatus](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

<blockquote>

<details>
<summary>iscurrentbatter : bool  </summary>

* Whether the player is the current batter.
</details>

<details>
<summary>iscurrentpitcher : bool  </summary>

* Whether the player is the current pitcher.
</details>

<details>
<summary>isonbench : bool  </summary>

* Whether the player is on the bench.
</details>

<details>
<summary>issubstitute : bool  </summary>

* Whether the player is a substitute.
</details>

</blockquote>

</details>

<details>
<summary>battingorder : int  </summary>

* The persons place in the batting order if avaliable.
</details>

<details>
<summary>allpositions : List[Position]  </summary>

* All of the person's positions if avaliable. Dataclass: [Position](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

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

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>batters : List[int]  </summary>

* List of batters playerid for this team
</details>

<details>
<summary>pitchers : List[int]  </summary>

* List of pitcher playerid for this team
</details>

<details>
<summary>bench : List[int]  </summary>

* List of bench playerid for this team
</details>

<details>
<summary>bullpen : List[int]  </summary>

* Bullpen list of playerid
</details>

<details>
<summary>battingorder : List[int]  </summary>

* Batting order for this team as a list of playerid
</details>

<details>
<summary>info : List[BoxScoreTeamInfo]  </summary>

* Batting and fielding info for team. Dataclass: [BoxScoreTeamInfo](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>title : str  </summary>

* Type of information
</details>

<details>
<summary>fieldlist : List[BoxScoreVL]  </summary>

* List holding the info for this info type. Dataclass: [BoxScoreVL](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>label : str  </summary>

* The label for this peice of info
</details>

<details>
<summary>value : str  </summary>

* The info associated with this label
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>note : List[str]  </summary>

* Team notes
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>officials : List[BoxScoreOffical]  </summary>

* The officials for this game. Dataclass: [BoxScoreOffical](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>official : Person  </summary>

* The official person. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* Api link for person
</details>

</blockquote>

</details>

<details>
<summary>officialtype : str  </summary>

* What type of official this person is
</details>

</blockquote>

</details>

<details>
<summary>info : List[BoxScoreVL]  </summary>

* Box score information. Dataclass: [BoxScoreVL](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/boxscore/attributes.py)

<blockquote>

<details>
<summary>label : str  </summary>

* The label for this peice of info
</details>

<details>
<summary>value : str  </summary>

* The info associated with this label
</details>

</blockquote>

</details>

<details>
<summary>pitchingnotes : List[str]  </summary>

* Pitching notes for this game
</details>

</blockquote>

</details>

<details>
<summary>leaders : GameLeaders  </summary>

* The data leaders for this game. Dataclass: [GameLeaders](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/attributes.py)

<blockquote>

<details>
<summary>hitdistance : dict  </summary>

* hit distance
</details>

<details>
<summary>hitspeed : dict  </summary>

* hit speed
</details>

<details>
<summary>pitchspeed : dict  </summary>

* pitch speed
</details>

</blockquote>

</details>

<details>
<summary>decisions : GameDecisions </summary>

* Decisions for this game, Ie a winner or a loser. Dataclass: [GameDecisions](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/game/livedata/attributes.py)

<blockquote>

<details>
<summary>winner : Person  </summary>

* The winning Pitcher person. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* Api link for person
</details>

</blockquote>

</details>

<details>
<summary>loser : Person  </summary>

* The loosing Pitcher person. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* Api link for person
</details>

</blockquote>

</details>

<details>
<summary>Save : Person  </summary>

* The Saving Pitcher person if avaliable. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* Api link for person
</details>

</blockquote>

</details>

</blockquote>

</details>

</blockquote>

</details>

</blockquote>

## Usage that returns Game objects

### `get_game`

Description: Returns a Game

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `game_id` | string/int | Yes      | Game id number |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `timecode` | string | No      | Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS |
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

### `get_game_play_by_play`

Description: Return the playbyplay of a game for a specific game id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `game_id` | string/int | Yes      | Game id number | None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `timecode` | string | No      | Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS | None
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | None

### `get_game_line_score`

Description: Return the Linescore of a game for a specific game id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `game_id` | string/int | Yes      | Game id number | None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `timecode` | string | No      | Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS | None
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | None


### `get_game_box_score`

Description: Return the boxscore of a game for a specific game id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `game_id` | string/int | Yes      | Game id number | None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `timecode` | string | No      | Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS | None
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | None


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1.1/game/534196/feed/live```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_game(game_id = 534196)
```