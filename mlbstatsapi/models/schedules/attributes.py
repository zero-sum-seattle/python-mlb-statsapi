from dataclasses import dataclass, field
from typing import Optional, Union, List
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.game.gamedata import GameStatus
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import LeagueRecord


@dataclass(repr=False)
class ScheduleGameTeam:
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
    leaguerecord: Union[LeagueRecord, dict]
    team: Union[Team, dict]
    splitsquad: bool
    seriesnumber: Optional[int] = None
    score: Optional[int] = None
    iswinner: Optional[bool] = False

    def __post_init__(self):
        self.leaguerecord = LeagueRecord(**self.leaguerecord)
        self.team = Team(**self.team)

    def __repr__(self):
        return f'ScheduleGameTeam(gamepk={self.leaguerecord}, team={self.team})'

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


@dataclass(repr=False)
class ScheduleGames:
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
    gamepk: int
    link: str
    gametype: str
    season: str
    gamedate: str
    officialdate: str
    venue: Venue
    content: dict
    gamenumber: int
    publicfacing: bool
    doubleheader: str
    gamedaytype: str
    tiebreaker: str
    calendareventid: str
    seasondisplay: str
    daynight: str
    scheduledinnings: int
    reversehomeawaystatus: bool
    seriesdescription: str
    recordsource: str
    ifnecessary: str
    ifnecessarydescription: str
    status: Union[GameStatus, dict] = field(default_factory=dict)
    teams: Union[ScheduleHomeAndAway, dict] = field(default_factory=dict)
    description: Optional[str] = None
    inningbreaklength: Optional[int] = None
    rescheduledate: Optional[str] = None
    reschedulegamedate: Optional[str] = None
    rescheduledfrom: Optional[str] = None
    rescheduledfromdate: Optional[str] = None
    istie: Optional[bool] = None
    resumedate: Optional[str] = None
    resumegamedate: Optional[str] = None
    resumedfrom: Optional[str] = None
    resumedfromdate: Optional[str] = None
    seriesgamenumber: Optional[int] = None
    gamesinseries: Optional[int] = None

    def __post_init__(self):
        self.status = GameStatus(**self.status) if self.status else self.status
        self.teams = ScheduleHomeAndAway(**self.teams) if self.teams else self.teams
        self.venue = Venue(**self.venue) if self.venue else self.venue

    def __repr__(self):
        return f'ScheduleGames(gamepk={self.gamepk}, link={self.link})'

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
    totalitems: int
    totalevents: int
    totalgames: int
    totalgamesinprogress: int
    events: List
    games: List[ScheduleGames] = field(default_factory=list)

    def __post_init__(self):
        self.games = [ScheduleGames(**game) for game in self.games ] if self.games else self.games

    def __repr__(self):
        return f'ScheduleDates(date={self.date}, totalgames={self.totalgames})'