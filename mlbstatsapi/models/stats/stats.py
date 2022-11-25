from dataclasses import dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person, Batter, Position
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League

@dataclass
class ExpectedStatistics:
    """
    a class to hold a code and a description

    Attributes
    ----------
    """
    avg: str
    slg: str
    woba: str
    wobacon: str

@dataclass
class Sabermetrics:
    """
    a class to hold a code and a description

    Attributes
    ----------
    """
    woba: float
    wrc: float
    wrcplus: float
    rar: float
    war: float

@dataclass
class CodeDesc:
    """
    a class to hold a code and a description

    Attributes
    ----------
    code : str
        the pitch code to reference the pitch
    description : str
        the description of the pitch
    """
    code: str
    description: Optional[str] = None


@dataclass
class Count:
    """
    a class to hold a pitch count and base runners

    Attributes
    ----------
    code : str
        code
    balls : int
        number of balls
    inning : int
        inning number
    istopinning : bool
        bool to hold status of top inning
    outs : int
        number of outs
    runneron1b : bool
        bool to hold 1b runner status
    runneron2b : bool
        bool to hold 2b runner status
    runneron3b : bool
        bool to hold 3b runner status
    strikes : int
        strike count
    """
    balls: int
    inning: int
    istopinning: bool
    outs: int
    runneron1b: bool
    runneron2b: bool
    runneron3b: bool
    strikes: int


@dataclass(kw_only=True)
class Stat:
    """
    Base class for stats

    Attributes
    ----------
    gametype : str
        type of game for stat
    numteams : str
        number of teams inolved in this stat
    season : str
        season of the stat
    dayofweek : str
        day of the week of the stat
    iswin : bool
        bool to hold if stat is a win
    ishome : bool
        bool to hold if stat is at home
    date : str
        date of game
    group : str 
        type of stat group
    _group : str
        type of the stat group
    _type : str
        type of the stat 
    """
    _group: str
    _type: str
    season: Optional[str] = None
    numteams: Optional[int] = None
    gametype: Optional[str] = None
    rank: Optional[int] = None
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    team: Optional[Union[Team, dict]] = field(default_factory=dict)
    player: Optional[Union[Person, dict]] = field(default_factory=dict)
    sport: Optional[Union[Sport, dict]] = field(default_factory=dict)
    league: Optional[Union[League, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position


@dataclass(kw_only=True)
class PitchArsenal(Stat):
    """
    A class to represent a pitcharsenal stat for a hitter and pitcher

    Attributes
    ----------
    """
    _stat = ['pitchArsenal']
    averagespeed: float
    count:  int
    percentage: float
    totalpitches: int
    type: Union[CodeDesc, dict]

    def __post_init__(self):
        self.type = CodeDesc(**self.type) if self.type else self.type


@dataclass(kw_only=True)
class ZoneCodes:
    """
    A class to represent a zone code statistic used in hot cold zones

    Attributes
    ----------
    zone : str
        zone code location
    color : str
        rgba code for the color of zone
    temp : str
        temp description of the zone
    value : str
        batting percentage of the zone
    """
    zone: str
    value: str
    color: Optional[str] = None
    temp: Optional[str] = None


@dataclass(kw_only=True)
class HotColdZones(Stat):
    """
    A class to represent a hot cold zone statistic

    Attributes
    ----------
    name : str
        name of the hot cold zone 
    zones : List[ZoneCodes]
        a list of zone codes to describe the zone
    """
    name: str
    zones: List[ZoneCodes]
    _stat = ['hotColdZones']

    def __post_init__(self):
        self.zones = [ZoneCodes(**zone) for zone in self.zones]


@dataclass(kw_only=True)
class SprayCharts(Stat):
    """
    A class to represent a spraychart statistic

    Attributes
    ----------
    leftfield : int
        percentage
    leftcenterfield : int
        percentage
    centerfield : int
        percentage
    rightcenterfield : int
        percentage
    rightfield : int
        percentage
    """
    leftfield: int
    leftcenterfield: int
    centerfield: int
    rightcenterfield: int
    rightfield: int
    _stat = ['sprayChart']
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.batter = Batter(**self.batter) if self.batter else self.batter


@dataclass(kw_only=True)
class OutsAboveAverage(Stat):
    """
    A class to represent a outs above average statistic

    NOTE: This stat type returns a empty list, or keys with with the value 0
    """
    _stat = ['outsAboveAverage']
    attempts: int
    totaloutsaboveaverageback: int
    totaloutsaboveaveragebackunrounded: int
    outsaboveaveragebackstraight: int
    outsaboveaveragebackstraightunrounded: int
    outsaboveaveragebackleft: int
    outsaboveaveragebackleftunrounded: int
    outsaboveaveragebackright: int
    outsaboveaveragebackrightunrounded: int
    totaloutsaboveaveragein: int
    totaloutsaboveaverageinunrounded: int
    outsaboveaverageinstraight: int
    outsaboveaverageinstraightunrounded: int
    outsaboveaverageinleft: int
    outsaboveaverageinleftunrounded: int
    outsaboveaverageinright: int
    outsaboveaverageinrightunrounded: int
    player: Union[Person, dict]
    gametype: str
