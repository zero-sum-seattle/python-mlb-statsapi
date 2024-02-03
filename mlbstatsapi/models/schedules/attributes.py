from dataclasses import dataclass, field
from typing import Optional, Union, List, Any
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.game.gamedata import GameStatus
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import LeagueRecord


class ScheduleGameTeam(BaseModel):
    """
    A class to represent the sheduled games teams shedule information in a Scheduled Dates game.

    Attributes
    ----------
    leaguerecord : LeagueRecord
        League record for this team
    score : int
        Current score for this team in this game
    team : Team
        Team info for this game
    iswinner : bool
        If this team is the winner of this game
    splitsquad : bool
        Split squad
    seriesnumber : int
        Series number 
    """
    leagueRecord: Union[LeagueRecord, dict]
    team: Union[Team, dict]
    splitSquad: bool
    seriesNumber: Optional[int]
    score: Optional[int]
    isWinner: Optional[bool]


class ScheduleHomeAndAway(BaseModel):
    """
    A class to represent both away and home teams in a Schedules Dates game.

    Attributes
    ----------
    home : ScheduleGameTeam
        Home team info for this game
    away : ScheduleGameTeam
        Away team info for this game
    """
    home: Union[ScheduleGameTeam, dict]
    away: Union[ScheduleGameTeam, dict]

    def __post_init__(self):
        self.home = ScheduleGameTeam(**self.home)
        self.away = ScheduleGameTeam(**self.away)


class ScheduleGames(BaseModel):
    """
    A class to represent a Game in a Schedules Dates.

    Attributes
    ----------
    gamepk : int
        The games id number
    link : str
        The link for this game
    gametype : str
        This games game type
    season : str
        The season this game takes place in
    gamedate : str
        The date for this game
    officialdate : str
        The official date for this game
    status : GameStatus
        The status of this game
    teams : ScheduleHomeAndAway
        Holds teams and thier info for this game
    venue : Venue  
        The venue this game takes place in
    content : dict
        Content for this game. Havent found a populated reference yet. Stays as dict
    istie : bool
        If this game is a tie
    gamenumber : int
        Game number for this game
    publicfacing : bool
        Is this game public facing
    doubleheader : str
        The double header status for this game, "n','y'?
    gamedaytype : str
        The type of gameday for this game
    tiebreaker : str
        Tie breaker for this game, 'n','y'?
    calendareventid : str
        Calender event Id for this game
    seasondisplay : str
        Displayed season for this game
    daynight : str
        Day or night game as a string, 'am','pm'?
    scheduledinnings : int
        Number of scheduled inning for the game
    reversehomeawaystatus : bool
        If reverse home and away?
    gameguid : str = None
        The games guid
    inningbreaklength : int
        Length of break between innings
    gamesinseries : int
        Number of games in current series
    seriesgamenumber : int
        Game number in the current series
    seriesdescription : str
        Description of this current series
    recordsource : str
        Record source 
    ifnecessary : str
        If necessary
    ifnecessarydescription : str
        If necessary description
    rescheduledate : str = None
        If game is rescheduled, this is the rescheduled date
    reschedulegamedate : str = None
        rescheduled game date
    rescheduledfrom : str = None
        rescheduled from
    rescheduledfromdate : str = None
        rescheduled from date
    istie : bool = None
        Is tie
    """
    gamePk: int
    link: str
    gameType: str
    season: str
    gameDate: str
    officialDate: str
    venue: Union[Venue, dict[str, Any]]
    content: dict
    gameNumber: int
    publicFacing: bool
    doubleHeader: str
    gamedayType: str
    tiebreaker: str
    calendarEventID: str
    seasonDisplay: str
    dayNight: str
    scheduledInnings: int
    reverseHomeAwayStatus: bool
    seriesDescription: str
    recordSource: str
    ifNecessary: str
    ifNecessaryDescription: str
    status: Union[GameStatus, dict[str, Any]]
    teams: Union[ScheduleHomeAndAway, dict[str, Any]]
    gameGuid: Optional[str]
    description: Optional[str]
    inningBreakLength: Optional[int]
    rescheduleDate: Optional[str]
    rescheduleGameDate: Optional[str]
    rescheduledFrom: Optional[str]
    rescheduledFromDate: Optional[str]
    isTie: Optional[bool]
    resumeDate: Optional[str]
    resumeGameDate: Optional[str]
    resumedFrom: Optional[str]
    resumedFromDate: Optional[str]
    seriesGameNumber: Optional[int]
    gamesInSeries: Optional[int]


@dataclass(repr=False)
class ScheduleDates:
    """
    A class to represent a Schedules Dates.

    Attributes
    ----------
    date : str
        Date for the group of games
    totalitems : int
        Total amount of items for this date
    totalevents : int
        The number of events for this date
    totalgames : int
        The number of games for this date
    totalgamesinprogress : int
        The number of games that are currently in progress for this date
    games : List[ScheduleGames]
        A list of games for this date
    events : list
        A list of events for this date. Need to handle this but cant find a populated 
        reference for this object. It stays as a list for now.
    """
    date: str
    totalItems: int
    totalEvents: int
    totalGames: int
    totalGamesInProgress: int
    events: List[None] # empty
    games: List[ScheduleGames]

