from typing import Optional, Union
from dataclasses import dataclass
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team

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
    pk: int
    type: str
    doubleHeader: str
    id: str
    gamedayType: str
    tiebreaker: str
    gameNumber: int
    calendarEventID: str
    season: str
    seasonDisplay: str

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
    dateTime: str
    originalDate: str
    officialDate: str
    dayNight: str
    time: str
    ampm: str

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
        reason for a state. Usually used for delays or cancellations
    """
    abstractGameState: str
    codedGameState: str
    detailedState: str
    statusCode: str
    startTimeTBD: bool
    abstractGameCode: str
    reason: Optional[str] = None

@dataclass
class GameTeams:
    """
    A class to represent the home and away teams.

    Attributes
    ----------
    away : GameTeam
        Away team
    home : GameTeam
        Home team
    """
    away: Union[Team, dict]
    home: Union[Team, dict]

    def __post_init__(self):
        self.away = Team(**self.away)
        self.home = Team(**self.home)

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
    condition: str
    temp: str
    wind: str

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
    attendance: int
    firstPitch: str
    gameDurationMinutes: int
    delayDurationMinutes: int

@dataclass
class ReviewInfo:
    """
    A class to represent reviewInfo for each team in this game.

    Attributes
    ----------
    used : int
        How many challenges used
    remaining : int
        How many challenges are remaining
    """
    used: int
    remaining: int

@dataclass
class GameReview:
    """
    A class to represent the Game Reviews for this game.

    Attributes
    ----------
    hasChallenges : bool
        If their are challenges
    away : ReviewInfo
        Away team review info
    home : ReviewInfo
        Home team review info
    """
    hasChallenges:  bool
    away:           Union[ReviewInfo, dict]
    home:           Union[ReviewInfo, dict]

    def __post_init__(self):
        self.away = ReviewInfo(**self.away)
        self.home = ReviewInfo(**self.home)

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
    noHitter: bool
    perfectGame: bool
    awayTeamNoHitter: bool
    awayTeamPerfectGame: bool
    homeTeamNoHitter: bool
    homeTeamPerfectGame: bool

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
    away: Union[Person, dict]
    home: Union[Person, dict]

    def __post_init__(self):
        self.away = Person(**self.away)
        self.home = Person(**self.home)