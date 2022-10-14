from dataclasses import dataclass, field
from typing import Optional, Union, List
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.game.gamedata import GameStatus
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import LeagueRecord

@dataclass
class ScheduleGameTeam:
    """
    A class to represent the sheduled games teams shedule information in a Scheduled Dates game.

    Attributes
    ----------
    leagueRecord : LeagueRecord
        League record for this team
    score : int
        Current score for this team in this game
    team : ScheduleGameTeamInfo
        Team info for this game
    isWinner : bool
        If this team is the winner of this game
    splitSquad : bool
        Split squad
    seriesNumber : int
        Series number 
    """
    leagueRecord: Union[LeagueRecord, dict]
    team: Union[Team, dict]
    splitSquad: bool
    seriesNumber: int
    score: Optional[int] = False
    isWinner: Optional[bool] = False

    def __post_init__(self):
        self.leagueRecord = LeagueRecord(**self.leagueRecord)
        self.team = Team(**self.team)

@dataclass
class ScheduleHomeAndAway:
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

@dataclass
class ScheduleGames:
    """
    A class to represent a Game in a Schedules Dates.

    Attributes
    ----------
    gamePk : int
        The games id number
    link : str
        The link for this game
    gameType : str
        This games game type
    season : str
        The season this game takes place in
    gameDate : str
        The date for this game
    officialDate : str
        The official date for this game
    status : GameStatus
        The status of this game
    teams : ScheduleGameTeams
        Holds teams and thier info for this game
    venue : Venue  
        The venue this game takes place in
    content : dict
        Content for this game. Havent found a populated reference yet. Stays as dict
    isTie : bool
        If this game is a tie
    gameNumber : int
        Game number for this game
    publicFacing : bool
        Is this game public facing
    doubleHeader : str
        The double header status for this game, "n','y'?
    gamedayType : str
        The type of gameday for this game
    tiebreaker : str
        Tie breaker for this game, 'n','y'?
    calendarEventID : str
        Calender event Id for this game
    seasonDisplay : str
        Displayed season for this game
    dayNight : str
        Day or night game as a string, 'am','pm'?
    scheduledInnings : int
        Number of scheduled inning for the game
    reverseHomeAwayStatus : bool
        If reverse home and away?
    inningBreakLength : int
        Length of break between innings
    gamesInSeries : int
        Number of games in current series
    seriesGameNumber : int
        Game number in the current series
    seriesDescription : str
        Description of this current series
    recordSource : str
        Record source 
    ifNecessary : str
        If necessary
    ifNecessaryDescription : str
        If necessary description
    rescheduleDate : str = None
        If game is rescheduled, this is the rescheduled date
    rescheduleGameDate : str = None
        rescheduled game date
    isTie : bool = None
        Is tie
    """
    gamePk: int
    link: str
    gameType: str
    season: str
    gameDate: str
    officialDate: str
    status: Union[GameStatus, dict]
    teams: Union[ScheduleHomeAndAway, dict]
    venue: Venue
    content: dict
    gameNumber: int
    publicFacing: bool
    doubleHeader: str
    gamedayType: str
    tiebreaker: str
    calendarEventID: str
    seasonDisplay: str
    dayNight: str
    description: str
    scheduledInnings: int
    reverseHomeAwayStatus: bool
    inningBreakLength: int
    gamesInSeries: int
    seriesGameNumber: int
    seriesDescription: str
    recordSource: str
    ifNecessary: str
    ifNecessaryDescription: str
    rescheduleDate: str = None
    rescheduleGameDate: str = None
    isTie: Optional[bool] = None

    def __post_init__(self):
        self.status = GameStatus(**self.status)
        self.teams = ScheduleHomeAndAway(**self.teams)


@dataclass
class ScheduleDates:
    """
    A class to represent a Schedules Dates.

    Attributes
    ----------
    date : str
        Date for the group of games
    totalItems : int
        Total amount of items for this date
    totalEvents : int
        The number of events for this date
    totalGames : int
        The number of games for this date
    totalGamesInProgress : int
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
    events: List
    games: List[ScheduleGames] = field(default_factory=list)

    def __post_init__(self):
        self.games = [ScheduleGames(**game) for game in self.games if self.games]