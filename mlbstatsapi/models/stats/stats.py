from dataclasses import dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.game import Game

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
    code: str
    balls: int
    inning: int
    istopinning: bool
    outs: int
    runneron1b: bool
    runneron2b: bool
    runneron3b: bool
    strikes: int


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
    description: str

@dataclass(kw_only=True)
class Stats:
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
    stat_group : str
        type of the stat group
    stat_type : str
        type of the stat 
    """
    # team: Optional[Union[Team, dict]] = field(default_factory=dict)
    # league: Optional[Union[League, dict]] = field(default_factory=dict)
    # sport: Optional[Union[Sport, dict]] = field(default_factory=dict)
    # position: Optional[Union[Position, dict]] = field(default_factory=dict) 
    # game: Optional[Union[Game, dict]] = field(default_factory=dict)
    # gametype: Optional[str] = None
    # numteams: Optional[str] = None
    # season: Optional[str] = None
    # dayofweek: Optional[str] = None
    # iswin: Optional[bool] = None
    # ishome: Optional[bool] = None
    # date: Optional[str] = None
    # group: Optional[str] = None
    # player: Optional[Person] = None
    # opponent: Union[Team, dict] = None
    stat_group: str
    stat_type: str

    # def __post_init__(self):
    #     self.team = Team(**self.team) if self.team else self.team
    #     self.player = Person(**self.player) if self.player else self.player
    #     self.league = League(**self.league) if self.league else self.league
    #     self.position = Position(**self.position) if self.position else self.position
    #     self.sport = Sport(**self.sport) if self.sport else self.sport
    #     self.opponent = Team(**self.opponent) if self.opponent else self.opponent
   
@dataclass
class HittingExpected(Stats):
    """
    A class to represent a excepted statistics statType: expectedStatistics.
    """
    """
    Attributes
    ----------
    avg : str
    slg : str
    woba : str
    wobaCon : str
    rank : int
    """
    type_ = [ 'expectedStatistics' ]
    avg : str
    slg : str
    woba : str
    wobaCon : str
    season: str
    player: Union[Person, dict]
    sport: Union[Sport, dict]
    gametype: str
    rank : Optional[int] = None


@dataclass
class PitchArsenal(Stats):
    """
    A class to represent a pitcharsenal stat for a hitter

    Used for the following stat types:
    pitchArsenal
    """
    type_ = [ 'pitchArsenal' ]
    averagespeed: float
    count:  int
    percentage: float
    totalpitches: int
    type: Union[CodeDesc, dict]

@dataclass
class ZoneCodes:
    """
    A class to represent a hitting sabermetric statistic

    Used for the following stat types:
    opponentsFaced

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
    color: str
    temp: str
    value: str

@dataclass
class HotColdZones(Stats):
    """
    A class to represent a hot cold zone statistic

    Used for the following stat types:
    opponentsFaced

    Attributes
    ----------
    name : str
        name of the hot cold zone 
    zones : List[ZoneCodes]
        a list of zone codes to describe the zone
    """
    name: str 
    zones: List[ZoneCodes]
    type_ = [ 'hotColdZones' ]

    def __post_init__(self):
        self.zones = [ ZoneCodes(**zone) for zone in self.zones ]