from dataclasses import dataclass, field
from typing import Optional, Union, List

import mlbstatsapi

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team

from .stats import Stats, CodeDesc, Count

@dataclass
class AdvancedHitting(Stats):
    """
    A class to represent a advanced hitting statistics

    Used for the following stat types:
    seasonAdvanced, careerAdvanced
    """
    type_ = [ 'seasonAdvanced', 'careerAdvanced', 'yearByYearAdvanced', 'statsSingleSeasonAdvanced' ]
    plateappearances: Optional[int] = None
    totalbases: Optional[int] = None
    leftonbase: Optional[int] = None
    sacbunts: Optional[int] = None
    sacflies: Optional[int] = None
    babip: Optional[str] = None
    extrabasehits: Optional[int] = None
    hitbypitch: Optional[int] = None
    gidp: Optional[int] = None
    gidpopp: Optional[int] = None
    numberofpitches: Optional[int] = None
    pitchesperplateappearance: Optional[str] = None
    walksperplateappearance: Optional[str] = None
    strikeoutsperplateappearance: Optional[str] = None
    homerunsperplateappearance: Optional[str] = None
    walksperstrikeout: Optional[str]= None
    iso: Optional[str] = None
    reachedonerror: Optional[int] = None
    walkoffs: Optional[int] = None
    flyouts: Optional[int] = None
    totalswings: Optional[int] = None
    swingandmisses: Optional[int] = None
    ballsinplay: Optional[int] = None
    popouts: Optional[int] = None
    lineouts: Optional[int] = None
    groundouts: Optional[int] = None
    flyhits: Optional[int] = None
    pophits: Optional[int] = None
    groundhits: Optional[int] = None
    linehits: Optional[int] = None

@dataclass
class SimpleHitting(Stats):
    """
    A class to represent a simple hitting statistics

    Used for the following stat types:
    yearByYear, projectedros, season, projectedros, projected, career, careerPlayoffs, yearByYearPlayoffs
    """
    type_ = [ 'yearByYear', 'projectedros', 'season', 'projectedros', 'projected', 'career', 
    'careerPlayoffs', 'yearByYearPlayoffs', 'careerRegularSeason', 'homeAndAway', 'homeAndAwayPlayoffs'
    'winLoss', 'winLossPlayoffs', 'statsSingleSeason' ]
    gamesplayed: Optional[int] = None
    groundouts: Optional[int] = None
    airouts: Optional[int] = None
    runs: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    homeruns: Optional[int] = None
    strikeouts: Optional[int] = None
    baseonballs: Optional[int] = None
    intentionalwalks: Optional[int] = None
    hits: Optional[int] = None
    hitbypitch: Optional[int] = None
    avg: Optional[str] = None
    atbats: Optional[int] = None
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    caughtstealing: Optional[int] = None
    stolenbases: Optional[int] = None
    stolenbasepercentage: Optional[int] = None
    groundintodoubleplay: Optional[int] = None
    numberofpitches: Optional[int] = None
    plateappearances: Optional[int] = None
    totalbases: Optional[int] = None
    rbi: Optional[int] = None
    leftonbase: Optional[int] = None
    sacbunts: Optional[int] = None
    sacflies: Optional[int] = None
    babip: Optional[str] = None
    groundoutstoairouts: Optional[int] = None
    catchersinterference: Optional[int] = None
    atbatsperhomerun: Optional[int] = None

@dataclass
class OpponentsFacedHitting(Stats):
    """
    A class to represent a hitting sabermetric statistic

    Used for the following stat types:
    opponentsFaced

    Attributes
    ----------
    batter : Person
        the batter of that stat object
    fieldingteam : Team
        the defence team of the stat object
    pitcher : Person
        the pitcher of that stat object
    """
    batter: Union[Person, dict]
    fieldingteam: Union[Team, dict]
    pitcher: Union[Person, dict]
    type_ = [ 'opponentsFaced' ]

    def __post_init__(self):
        self.batter = Person(**self.batter) if self.batter else self.batter
        self.pitcher = Person(**self.pitcher) if self.pitcher else self.pitcher
        self.fieldingteam = Team(**self.fieldingteam) if self.fieldingteam else self.fieldingteam


@dataclass
class HittingSabermetrics(Stats):
    """
    A class to represent a hitting sabermetric statistic

    Used for the following stat types:
    sabermetrics
    """
    type_ = [ 'sabermetrics' ]
    woba: float
    wrc: float
    wrcplus: float
    rar: float
    war: float

@dataclass
class HittingLog(Stats):
    """
    A class to represent a gamelog stat for a hitter

    Used for the following stat types:
    gameLog
    """
    positionsplayed: List[Position]
    type_ = [ 'gameLog' ]
    gamesplayed: Optional[int] = None
    groundouts: Optional[int] = None
    airouts: Optional[int] = None
    runs: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    homeruns: Optional[int] = None
    strikeouts: Optional[int] = None
    baseonballs: Optional[int] = None
    intentionalwalks: Optional[int] = None
    hits: Optional[int] = None
    hitbypitch: Optional[int] = None
    avg: Optional[str] = None
    atbats: Optional[int] = None
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    caughtstealing: Optional[int] = None
    stolenbases: Optional[int] = None
    stolenbasepercentage: Optional[int] = None
    groundintodoubleplay: Optional[int] = None
    numberofpitches: Optional[int] = None
    plateappearances: Optional[int] = None
    totalbases: Optional[int] = None
    rbi: Optional[int] = None
    leftonbase: Optional[int] = None
    sacbunts: Optional[int] = None
    sacflies: Optional[int] = None
    babip: Optional[str] = None
    groundoutstoairouts: Optional[int] = None
    catchersinterference: Optional[int] = None
    atbatsperhomerun: Optional[int] = None

    def __post_init__(self):
        self.positionsplayed = [ Position(**position) for position in self.positionsplayed if self.position]
         
@dataclass
class PlayLog:
    """development object that holds imformation related to the play"""
    atbatnumber: int
    batside: CodeDesc
    call: CodeDesc
    description: str
    event: str
    eventtype: str
    isatbat: bool
    isball: bool
    isbasehit: bool
    isinplay: bool
    isplateappearance: bool
    isstrike: bool
    pitchhand: CodeDesc
    type: CodeDesc

    def __post_init__(self):
        self.type = CodeDesc(**self.type) if self.type else self.type
        self.pitchhand = CodeDesc(**self.pitchhand) if self.pitchhand else self.pitchhand
        self.batsite = CodeDesc(**self.batside) if self.batside else self.batside
        self.call = CodeDesc(**self.call) if self.call else self.call

@dataclass
class HittingLog(Stats):
    """A development class for stat type Playlog pitchLog """
    ispitch: bool
    pitchnumber: int
    playid: str
    count: Union[Count, dict]
    batter: Union[Person, dict]
    pitcher: Union[Person, dict]
    play: Union[PlayLog, dict]
    type_ = [ 'playLog', 'pitchLog' ]

    def __post_init__(self):
        self.play = PlayLog(**mlbstatsapi._transform_mlbdata(self.play, ['details'])) if self.play else self.play
        self.count = Count(**self.count) if self.count else self.count
        self.pitcher = Person(**self.pitcher) if self.pitcher else self.pitcher
        self.batter = Person(**self.batter) if self.batter else self.batter

@dataclass
class SprayChart(Stats):
    centerfield: float
    leftcenterfield: float
    leftfield: float
    rightcenterfield: float
    rightfield: float
    batter: Union[Person, dict]

    def __post_init__(self):
        self.batter = Person(**self.batter) if self.batter else self.batter

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


    # "standard", # doesnt work
    # "advanced", # doesnt work
    # "careerStatSplits", returns 500
    # "gameLog", # started TODO 
    # "playLog", # this is a tough one
    # "pitchLog", # similiar to playlog
    # "metricLog", # returns 500
    # "metricAverages", # returns 500
    # "pitchArsenal", # works
    # "outsAboveAverage", # returns nothing
    # "expectedStatistics", # done
    # "sprayChart", # easy 
    # "tracking", # returns 200 but nothing
    # "vsPlayer", # these must need a param passed with them
    # "vsPlayerTotal", # these must need a param passed with them
    # "vsPlayer5Y", # these must need a param passed with them
    # "vsTeam", # these must need a param passed with them
    # "vsTeam5Y", # these must need a param passed with them
    # "vsTeamTotal", # these must need a param passed with them
    # "lastXGames", # TODO
    # "byDateRange", # TODO
    # "byDateRangeAdvanced" # TODO
    # "byMonth", # TODO 
    # "byMonthPlayoffs", # TODO
    # "byDayOfWeek", # TODO
    # "byDayOfWeekPlayoffs", # TODO
    # "homeAndAway",
    # "homeAndAwayPlayoffs", 
    # "winLoss", # simple
    # "winLossPlayoffs" # simple
    # "rankings", # need to look?
    # "rankingsByYear", # need to look?
    # "statsSingleSeason", # simple
    # "statsSingleSeasonAdvanced", # advanced
    # "hotColdZones", # zones
    # "availableStats", # TODO I think this will help?
    # "opponentsFaced", # done
    # "gameTypeStats", # null
    # "firstYearStats", # null
    # "lastYearStats", # null
    # "statSplits", # null
    # "statSplitsAdvanced" # null,
    # "atGameStart",# null
    # "vsOpponents" # null ]