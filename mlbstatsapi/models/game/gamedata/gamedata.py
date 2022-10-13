from typing import Union, List, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.people import Person

from mlbstatsapi.models.game.gamedata.gameteams import GameTeams
from mlbstatsapi.models.game.gamedata.gamereview import GameReview

@dataclass
class GameDataGame:
    """
    A class to represent the this game's game info.

    Attributes
    ----------
    pk : int
        This game's game id
    type : str
        This game's game type code
    doubleHeader : str
        Represents if this game is a double header or not
    id : str
        An unknown Id
    gamedayType : str
        This game's gameday type code
    tiebreaker : str
        Is this game a tie breaker
    gameNumber : int
        The game number for this game. If double header will be 2.
    calendarEventID : str
        The id for this calendar event
    season : str
        This game's season year
    seasonDisplay : str
        This game's displayed season
    """
    pk:                 int
    type:               str
    doubleHeader:       str
    id:                 str
    gamedayType:        str
    tiebreaker:         str
    gameNumber:         int
    calendarEventID:    str
    season:             str
    seasonDisplay:      str

@dataclass
class GameDatetime:
    """
    A class to represent the date time for this game.

    Attributes
    ----------
    dateTime : str
        Date time for this game
    originalDate : str
        The original scheduled date for this game
    officialDate : str
        The current scheduled date for this game
    dayNight : str
        The current lighting condition game type
    time : str
        The time
    ampm : str
        The games am or pm code
    """
    dateTime:       str
    originalDate:   str
    officialDate:   str
    dayNight:       str
    time:           str
    ampm:           str

@dataclass
class GameStatus:
    """
    A class to represent this game's game status.

    Attributes
    ----------
    abstractGameState : str
        The abstract game state
    codedGameState : str
        The coded game state
    detailedState : str
        The detailed game state
    statusCode : str
        Status code for this game
    startTimeTBD : bool
        If the start time is TBD
    abstractGameCode : str
        The abstract game code
    reason : str
        reason for game reschedule
    """
    abstractGameState:  str
    codedGameState:     str
    detailedState:      str
    statusCode:         str
    startTimeTBD:       bool
    abstractGameCode:   str
    reason: str = None

@dataclass
class GameWeather:
    """
    A class to represent the weather for this game.

    Attributes
    ----------
    condition : str
        The weather condition
    temp : str
        The temperature in F
    wind : str
        The wind in MPH and the direction
    """
    condition:  str
    temp:       str
    wind:       str

@dataclass
class GameInfo:
    """
    A class to represent the game info for this game.

    Attributes
    ----------
    attendance : int
        The attendance for this game
    firstPitch : str
        The time of the first pitch
    gameDurationMinutes : int
        The duration of the game in minutes
    delayDurationMinutes : int
        The length of delay for the game in minutes
    """
    attendance:             int
    firstPitch:             str
    gameDurationMinutes:    int
    delayDurationMinutes:   int

@dataclass
class GameFlags:
    """
    A class to represent the flags for this game.

    Attributes
    ----------
    noHitter : bool
        If there is a no hitter in this game
    perfectGame :  bool
        If there this game is a perfect game
    awayTeamNoHitter : bool
        If the away team has a no hitter
    awayTeamPerfectGame : bool
        If the away team has a perfect game
    homeTeamNoHitter : bool
        If the home team has a no hitter
    homeTeamPerfectGame : bool
        If the home team has a perfect game
    """
    noHitter:               bool
    perfectGame:            bool
    awayTeamNoHitter:       bool
    awayTeamPerfectGame:    bool
    homeTeamNoHitter:       bool
    homeTeamPerfectGame:    bool

@dataclass
class GameProbablePitchers:
    """
    A class to represent the home and away probable pitchers for this game.

    Attributes
    ----------
    home : Person
        Home team probable pitcher
    away : Person
        Away team probable pitcher
    """
    away: Union[Person, Dict]
    home: Union[Person, Dict]

    def __post_init__(self):
        self.away = Person(**self.away)
        self.home = Person(**self.home)

@dataclass
class GameData:
    """
    A class to represent a games game data.

    Attributes
    ----------
    game : GameDataGame
        game information about this game
    datetime : GameDatetime
        Time and dates for this game
    status : GameStatus
        information on this game's status
    teams : GameTeams
        Our two teams for this game, home and away
    players : List[Person]
        A list of all the players for this game
    venue : GameVenue
        Venue information for this game
    officialVenue : Venue
        The official venue for this game
    weather : GameWeather
        The weather for this game.
    gameInfo : GameInfo
        information on this game
    review : GameReview
        Game review info and team challenges
    flags : GameFlags
        Flag bools for this game
    alerts : List[]
        Alerts
    probablePitchers : GameProbablePitchers
        Home and away probable pitchers for this game
    officialScorer : Person
        The official scorer for this game
    primaryDatacaster : Person
        The official dataCaster for this game
    """
    game:               Union[GameDataGame, Dict[str, Any]]
    datetime:           Union[GameDatetime, Dict[str, Any]]
    status:             Union[GameStatus, Dict[str, Any]]
    teams:              Union[GameTeams, Dict[str, Any]]
    players:            Union[List[Person], Dict]
    venue:              Union[Venue, Dict[str, Any]]
    officialVenue:      Union[Venue, Dict[str, Any]]
    weather:            Union[GameWeather, Dict[str, Any]]
    gameInfo:           Union[GameInfo, Dict[str, Any]]
    review:             Union[GameReview, Dict[str, Any]]
    flags:              Union[GameFlags, Dict[str, Any]]
    alerts:             List
    probablePitchers:   Union[GameProbablePitchers, Dict]
    officialScorer:     Union[Person, Dict[str, Any]]
    primaryDatacaster:  Union[Person, Dict[str, Any]]

    def __post_init__(self):
        self.game = GameDataGame(**self.game)
        self.datetime = GameDatetime(**self.datetime)
        self.status = GameStatus(**self.status)
        self.teams = GameTeams(**self.teams)
        # self.players
        # tempPlayers = self.players
        self.players = [Person(**(self.players[key])) for key in self.players]
        self.venue = Venue(**self.venue)
        self.officialVenue = Venue(**self.officialVenue)
        self.weather = GameWeather(**self.weather)
        self.gameInfo = GameInfo(**self.gameInfo)
        self.review = GameReview(**self.review)
        self.flags = GameFlags(**self.flags)
        self.probablePitchers = GameProbablePitchers(**self.probablePitchers)
        self.officialScorer = Person(**self.officialScorer)
        self.primaryDatacaster = Person(**self.primaryDatacaster)
