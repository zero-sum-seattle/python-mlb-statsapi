from dataclasses import dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

from .stats import Splits, CodeDesc, Count

@dataclass
class AdvancedHittingStat:
    """
    A class to represent a advanced hitting statistics
    """
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
class SimpleHittingStat:
    """
    A class to represent a simple hitting statistics
    """
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
    groundintotripleplay: Optional[int] = None
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

@dataclass(kw_only=True)
class HittingWinLoss(Splits, SimpleHittingStat):
    """
    A class to represent a hitting winLoss statistic

    Attributes
    ----------
    iswin : bool
        the bool to hold if a win or not for hitting winLoss
    """
    _stat = [ 'winLoss' ]
    iswin: bool

@dataclass(kw_only=True)
class HittingWinLossPlayoffs(Splits, SimpleHittingStat):
    """
    A class to represent a hitting winLoss statistic

    Attributes
    ----------
    iswin : bool
        the bool to hold if a win or not for hitting winLoss
    """
    _stat = [ 'winLossPlayoffs' ]
    iswin: bool

@dataclass(kw_only=True)
class HittingHomeAndAway(Splits, SimpleHittingStat):
    """
    A class to represent a hitting homeAndAway statistic

    Attributes
    ----------
    ishome : bool
        the bool to hold if it ishome hitting homeAndAway
    """
    _stat = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class HittingHomeAndAwayPlayoffs(Splits, SimpleHittingStat):
    """
    A class to represent a hitting homeAndAway statistic

    Attributes
    ----------
    ishome : bool
        the bool to hold if it ishome hitting homeAndAway
    """
    _stat = [ 'homeAndAwayPlayoffs' ]
    ishome: bool

@dataclass(kw_only=True)
class HittingCareer(Splits, SimpleHittingStat):
    """
    A class to represent a hitting career or careerPlayoffs statistic

    Attributes
    ----------
    """
    _stat = [ 'career' ]

@dataclass(kw_only=True)
class HittingCareerRegularSeason(Splits, SimpleHittingStat):
    """
    A class to represent a hitting career or careerPlayoffs statistic

    Attributes
    ----------
    """
    _stat = [ 'careerRegularSeason' ]


@dataclass(kw_only=True)
class HittingCareerPlayoffs(Splits, SimpleHittingStat):
    """
    A class to represent a hitting careerPlayoffs statistic

    Attributes
    ----------
    """
    _stat = [ 'careerPlayoffs' ]

@dataclass(kw_only=True)
class HittingSeason(Splits, SimpleHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = [ 'season' ]


@dataclass(kw_only=True)
class HittingSingleSeason(Splits, SimpleHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = [ 'statsSingleSeason' ]

@dataclass(kw_only=True)
class HittingSeasonAdvanced(Splits, AdvancedHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = ['seasonAdvanced' ]

@dataclass(kw_only=True)
class HittingCareerAdvanced(Splits, AdvancedHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = [ 'careerAdvanced' ]


@dataclass(kw_only=True)
class HittingYearByYear(Splits, SimpleHittingStat):
    """
    A class to represent a hitting yearbyyear or yearByYearPlayoffs statistic

    Attributes
    ----------
    """
    _stat = [ 'yearByYear' ]

@dataclass(kw_only=True)
class HittingYearByYearPlayoffs(Splits, SimpleHittingStat):
    """
    A class to represent a hitting yearByYearPlayoffs statistic

    Attributes
    ----------
    """
    _stat = [ 'yearByYearPlayoffs' ]

@dataclass
class OpponentsFacedHitting(Splits):
    """
    A class to represent a hitting opponentsFaced statistic

    Attributes
    ----------
    batter : Person
        the batter of that stat object
    fieldingteam : Team
        the defence team of the stat object
    pitcher : Person
        the pitcher of that stat object
    group : str
        stat group
    """
    _stat = [ 'opponentsFaced' ]
    group: str
    batter: Union[Person, dict]
    fieldingteam: Union[Team, dict]
    pitcher: Union[Person, dict]

@dataclass
class HittingSabermetrics(Splits):
    """
    A class to represent a hitting sabermetric statistic

    """
    _stat = [ 'sabermetrics' ]
    woba: float
    wrc: float
    wrcplus: float
    rar: float
    war: float

@dataclass(kw_only=True)
class HittingGameLog(Splits, SimpleHittingStat):
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    positionsplayed : List[Position]
    stat : SimpleHittingStat
    ishome : bool
        bool to hold ishome
    iswin : bool
        bool to hold iswin
    game : Game
        Game of the log
    date : str
        date of the log
    gametype : str
        type of game
    opponent : Team
        Team of the opponent
    sport : Sport
        Sport of the stat
    league : League
        League of the stat
    player : Person
        Player of the stat
    """
    ishome: bool
    iswin: bool
    game: Union[Game, dict]
    date: str
    opponent: Union[Team, dict]
    _stat = [ 'gameLog' ]
    positionsplayed: Optional[List[Position]] = field(default_factory=list)

    def __post_init__(self):
        if self.positionsplayed:
            self.positionsplayed = [ Position(**position) for position in self.positionsplayed ]
        
@dataclass
class PlayDetails:
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    call : dict
        play call code and description
    description : str
        description of the play
    event : str
        type of event
    eventtype : str
        type of event
    isinplay : bool
        is the ball in play true or false
    isstrike : bool
        is the ball a strike true or false
    isball : bool
        is it a ball true or false
    isbasehit : bool
        is the event a base hit true or false
    isatbat : bool
        is the event at bat true or false
    isplateappearance : bool
        is the event a at play appears true or false
    type : dict
        type of pitch code and description
    batside : dict
        bat side code and description
    pitchhand : dict
        pitch hand code and description
    """
    call: Union[CodeDesc, dict]
    event: str
    eventtype: str
    isinplay: bool
    isstrike: bool
    isball: bool
    isbasehit: bool
    isatbat: bool
    isplateappearance: bool
    batside: Union[CodeDesc, dict]
    pitchhand: Union[CodeDesc, dict]
    description: Optional[str] = None
    type: Optional[Union[CodeDesc, dict]] = field(default_factory=dict)


@dataclass(kw_only=True)
class HittingPlayLog(Splits):
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    season : str
        season for the stat
    opponent : Team
        opponent
    date : str
        date of log
    gametype : str
        game type code
    ishome : bool
        is the game at home bool
    pitcher : Person
        pitcher of the log
    batter : Person
        batter of the log
    game : Game
        the game of the log

    """
    opponent: Union[Team, dict]
    date: str
    ishome: bool
    pitcher: Union[Person, dict]
    batter: Union[Person, dict]
    game: Union[Game, dict]
    details: Union[PlayDetails, dict]
    count: Union[Count, dict]
    pitchnumber: int
    atbatnumber: int
    ispitch: bool
    playid: Optional[str] = None
    _stat = [ 'playLog' ]

    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count)

@dataclass(kw_only=True)
class HittingPitchLog(Splits):
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    season : str
        season for the stat
    stat : PlayLog
        information regarding the play for the stat
    opponent : Team
        opponent
    date : str
        date of log
    gametype : str
        game type code
    ishome : bool
        is the game at home bool
    pitcher : Person
        pitcher of the log
    batter : Person
        batter of the log
    game : Game
        the game of the log

    """
    _stat = [ 'pitchLog' ]
    opponent: Union[Team, dict]
    date: str
    ishome: bool
    pitcher: Union[Person, dict]
    batter: Union[Person, dict]
    game: Union[Game, dict]
    details: Union[PlayDetails, dict]
    count: Union[Count, dict]
    pitchnumber: int
    atbatnumber: int
    ispitch: bool
    playid: Optional[str] = None 
    
    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count)

@dataclass(kw_only=True)
class HittingLastXGames(Splits, SimpleHittingStat):
    """
    A class to represent a lastXGames statistic

    Attributes
    ----------
    """
    _stat = [ 'lastXGames' ]

@dataclass(kw_only=True)
class HittingDateRange(Splits, SimpleHittingStat):
    """
    A class to represent a byDateRange statistic

    Attributes
    ----------
    """
    _stat = [ 'byDateRange' ]

@dataclass(kw_only=True)
class HittingDateRangeAdvanced(Splits, AdvancedHittingStat):
    """
    A class to represent a byDateRangeAdvanced statistic

    Attributes
    ----------
    """
    _stat = [ 'byDateRangeAdvanced' ]

@dataclass(kw_only=True)
class HittingByMonth(Splits, SimpleHittingStat):
    """
    A class to represent a byMonth hitting statistic

    Attributes
    ----------
    """
    _stat = [ 'byMonth' ]
    month: int
    gamesplayed: int

@dataclass(kw_only=True)
class HittingByMonthPlayoffs(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    month : str
        the month of the stat
    """
    _stat = [ 'byMonthPlayoffs' ]
    month: int
    gamesplayed: int

@dataclass(kw_only=True)
class HittingDayOfWeek(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    dayofweek : int
        the day of the week
    """
    _stat = [ 'byDayOfWeek' ]
    dayofweek: int

@dataclass(kw_only=True)
class HittingDayOfWeekPlayoffs(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    dayofweek : int
        the day of the week
    """
    _stat = [ 'byDayOfWeekPlayoffs' ]
    dayofweek: int

@dataclass(kw_only=True)
class HittingExpectedStatistics(Splits):
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
    _stat = [ 'expectedStatistics' ]
    avg : str
    slg : str
    woba : str
    wobacon : str
    gametype: str
    rank : Optional[int] = None

@dataclass(kw_only=True)
class HittingVsTeam(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    dayofweek : int
        the day of the week
    """
    _stat = [ 'vsTeam' ]
    opponent: Union[Person, dict]
    rank: int
    batter: Optional[Union[Person, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Person, dict]] = field(default_factory=dict)

@dataclass(kw_only=True)
class HittingVsTeamTotal(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    """
    _stat = [ 'vsTeamTotal' ]
    opponent: Union[Person, dict]
    rank: int
    batter: Optional[Union[Person, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Person, dict]] = field(default_factory=dict)

@dataclass(kw_only=True)
class HittingVsTeam5Y(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    """
    _stat = [ 'vsTeam5Y' ]
    opponent: Union[Person, dict]
    rank: int
    batter: Optional[Union[Person, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Person, dict]] = field(default_factory=dict)

@dataclass(kw_only=True)
class HittingVsPlayer(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    """
    _stat = [ 'vsPlayer' ]

@dataclass(kw_only=True)
class HittingVsPlayerTotal(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    """
    _stat = [ 'vsPlayerTotal' ]

@dataclass(kw_only=True)
class HittingVsPlayer5Y(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    """
    _stat = [ 'vsPlayer5Y' ]




# class HittingStats:
#     group: str
#     vsplayer5y: list = []
#     vsplayertotal: list = []
#     vsplayer: list = []
#     vsteam5y: list = []
#     vsteamtotal: list = []
#     vsteam: list = []
#     expectedstatistics: list = []
#     bydayofweekplayoffs: list = []
#     bydayofweek: list = []
#     bymonthplayoffs: list = []
#     bymonth: list = []
#     bydaterangeadvanced: list = []
#     bydaterange: list = []
#     lastxgames: list = []
#     pitchlog: list = []
#     playlog: list = []
#     gamelog: list = []
#     sabermetrics: list = []
#     opponentsfaced: list = []
#     yearbyyearplayoffs: list = []
#     yearbyyear: list = []
#     careeradvanced: list = []
#     seasonadvanced: list = []
#     statssingleseason: list = []
#     season: list = []
#     careerplayoffs: list = []
#     careerregularseason: list = []
#     career: list = []
#     homeandawayplayoffs: list = []
#     homeandaway: list = []
#     winloss: list = []

#     def __init__(self) -> None:
#         self.group = 'hitting'

#     def add_stats(self, stat_type, splits) -> None:

#         # loop through splits
#         for split in splits:
            
#             # there is a value so we need to append a new list item to it
#             if getattr(self, stat_type):
#                 # this is easy but we need the egg to make a chicken
#                 pass
#             else:
#                 # now we need to set it, we will use setattr for that
#                 setattr(self, stat_type, # TODO we need to build a object first)
