from typing import Optional, Union
from dataclasses import dataclass, field
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
    doubleheader : str
        Represents if this game is a double header or not
    id : str
        An unknown Id
    gamedaytype : str
        This game's gameday type code
    tiebreaker : str
        Is this game a tie breaker
    gamenumber : int
        The game number for this game. If double header will be 2.
    calendareventid : str
        The id for this calendar event
    season : str
        This game's season year
    seasondisplay : str
        This game's displayed season
    """
    pk: int
    type: str
    doubleheader: str
    id: str
    gamedaytype: str
    tiebreaker: str
    gamenumber: int
    calendareventid: str
    season: str
    seasondisplay: str


@dataclass(repr=False)
class GameDatetime:
    """
    A class to represent the date time for this game.

    Attributes
    ----------
    datetime : str
        Date time for this game
    originaldate : str
        The original scheduled date for this game
    officialdate : str
        The current scheduled date for this game
    daynight : str
        The current lighting condition game type
    time : str
        The time
    ampm : str
        The games am or pm code
    """
    datetime: str
    originaldate: str
    officialdate: str
    daynight: str
    time: str
    ampm: str
    resumedate: Optional[str] = None
    resumedatetime: Optional[str] = None
    resumedfromdate: Optional[str] = None
    resumedfromdatetime: Optional[str] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass
class GameStatus:
    """
    A class to represent this game's game status.

    Attributes
    ----------
    abstractgamestate : str
        The abstract game state
    codedgamestate : str
        The coded game state
    detailedstate : str
        The detailed game state
    statuscode : str
        Status code for this game
    starttimetbd : bool
        If the start time is TBD
    abstractgamecode : str
        The abstract game code
    reason : str
        reason for a state. Usually used for delays or cancellations
    """
    abstractgamestate: str
    codedgamestate: str
    detailedstate: str
    statuscode: str
    starttimetbd: bool
    abstractgamecode: str
    reason: Optional[str] = None


@dataclass
class GameTeams:
    """
    A class to represent the home and away teams.

    Attributes
    ----------
    away : Team
        Away team
    home : Team
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
    wind: Optional[str] = None


@dataclass
class GameInfo:
    """
    A class to represent the game info for this game.

    Attributes
    ----------
    attendance : int
        The attendance for this game
    firstpitch : str
        The time of the first pitch
    gamedurationminutes : int
        The duration of the game in minutes
    delaydurationminutes : int
        The length of delay for the game in minutes
    """
    attendance: int
    firstpitch: str
    gamedurationminutes: int
    delaydurationminutes: Optional[int] = None


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
    haschallenges : bool
        If their are challenges
    away : ReviewInfo
        Away team review info
    home : ReviewInfo
        Home team review info
    """
    haschallenges: bool
    away: Union[ReviewInfo, dict]
    home: Union[ReviewInfo, dict]

    def __post_init__(self):
        self.away = ReviewInfo(**self.away)
        self.home = ReviewInfo(**self.home)


@dataclass
class GameFlags:
    """
    A class to represent the flags for this game.

    Attributes
    ----------
    nohitter : bool
        If there is a no hitter in this game
    perfectgame :  bool
        If there this game is a perfect game
    awayteamnohitter : bool
        If the away team has a no hitter
    awayteamperfectgame : bool
        If the away team has a perfect game
    hometeamnohitter : bool
        If the home team has a no hitter
    hometeamperfectgame : bool
        If the home team has a perfect game
    """
    nohitter: bool
    perfectgame: bool
    awayteamnohitter: bool
    awayteamperfectgame: bool
    hometeamnohitter: bool
    hometeamperfectgame: bool


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
    away: Union[Person, dict] = field(default_factory=dict)
    home: Union[Person, dict] = field(default_factory=dict)

    def __post_init__(self):
        self.away = Person(**self.away) if self.away else self.away
        self.home = Person(**self.home) if self.home else self.home
