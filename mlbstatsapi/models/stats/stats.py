from dataclasses import dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person, Batter, Position
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.data import CodeDesc

@dataclass
class PitchArsenalSplit:
    """
    A class to represent a pitching pitch arsenal split 

    Attributes
    ----------
    percentage : float
    count : int
    totalPitches : int
    averageSpeed : float
    type : Union[CodeDesc, dict]
    """
    percentage: float
    count: int
    totalpitches: int
    averagespeed: float
    type: Union[CodeDesc, dict]

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

@dataclass(repr=False)
class Sabermetrics:
    """
    a class to hold a code and a description

    Attributes
    ----------
    woba : float
    wRaa : float
    wRc : float
    wRcPlus : float
    rar : float
    war : float
    batting : float
    fielding : float
    baseRunning : float
    positional : float
    wLeague : float
    replacement : float
    spd : float
    ubr : float
    wGdp : float
    wSb : float
    """

    woba: Optional[float] = None
    wraa: Optional[float] = None
    wrc: Optional[float] = None
    wrcplus: Optional[float] = None
    rar: Optional[float] = None
    war: Optional[float] = None
    batting: Optional[float] = None
    fielding: Optional[float] = None
    baserunning: Optional[float] = None
    positional: Optional[float] = None
    wleague: Optional[float] = None
    replacement: Optional[float] = None
    spd: Optional[float] = None
    ubr: Optional[float] = None
    wgdp: Optional[float] = None
    wsb: Optional[float] = None


    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(kw_only=True, repr=False)
class Split:
    """
    Base class for splits

    Attributes
    ----------
    season : str
    numteams : int
    gametype : str
    rank : int
    position : Position
    team : Team
    player : Person
    sport : Sport
    league : League
    """
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
        self.team = Team(**self.team) if self.team else self.team
        self.sport = Sport(**self.sport) if self.sport else self.sport
        self.league = League(**self.league) if self.league else self.league
        self.player = Person(**self.player) if self.player else self.player

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))


@dataclass(kw_only=True, repr=False)
class Stat:
    """
    Base class for stats

    Attributes
    ----------
    group : str
        type of the stat group
    type : str
        type of the stat 
    totalsplits : int
        The number of split objects
    exemptions : list
        not sure what this is
    splits : list
        a list of split objects
    """
    group: str
    type: str
    totalsplits: int
    exemptions: Optional[List] = field(default_factory=list)
    splits: Optional[List] = field(default_factory=list)

    def __repr__(self):
        return f'Stat(group={self.group}, type={self.type})'

@dataclass(kw_only=True)
class PitchArsenal(Split):
    """
    A class to represent a pitcharsenal stat for a hitter and pitcher

    Attributes
    ----------
    """
    _stat = ['pitchArsenal']
    stat: Union[PitchArsenalSplit, dict]

    def __post_init__(self):
        self.stat = PitchArsenalSplit(**self.stat)


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
class Zones:
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

    def __post_init__(self):
        self.zones = [ZoneCodes(**zone) for zone in self.zones]

@dataclass(kw_only=True)
class HotColdZones(Split):
    """
    A class to represent a hotcoldzone statistic

    Attributes
    ----------
    stat : Zones
        the holdcoldzones for the stat
    """
    stat: Zones
    _stat = ['hotColdZones']

    def __post_init__(self):
        self.stat = Zones(**self.stat)

@dataclass
class Chart:
    """
    A class to represent a chart for SprayCharts

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

@dataclass(kw_only=True)
class SprayCharts(Split):


    _stat = ['sprayChart']
    stat: Union[Chart, dict]
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.batter = Batter(**self.batter) if self.batter else self.batter
        self.stat = Chart(**self.stat)

@dataclass(kw_only=True)
class OutsAboveAverage(Split):
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


#
# These dataclasses are for the game stats end point only
# url: https://statsapi.mlb.com/api/v1/people/663728/stats/game/715757
# The gamelog stats in this JSON have different keys set for their stat
# and group. This breaks my logic of handling stat classes
#

@dataclass
class PlayerGameLogStat(Split):
    """
    A class to represent a chart for SprayCharts

    Attributes
    ----------
    """
    type: str
    group: str
    stat: dict
    _stat = ['gameLog']
