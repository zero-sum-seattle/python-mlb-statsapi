from dataclasses import dataclass, field
from typing import Optional, Union, List

import mlbstatsapi

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.game import Game

from .stats import Stats, CodeDesc, Count

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
class HittingWL(Stats, SimpleHittingStat):
    """
    A class to represent a hitting winLoss statistic

    Attributes
    ----------
    iswin : bool
        the bool to hold if a win or not for hitting winLoss
    """
    type_ = [ 'winLoss' ]
    iswin: bool

@dataclass(kw_only=True)
class HittingWLPlayoffs(Stats, SimpleHittingStat):
    """
    A class to represent a hitting winLoss statistic

    Attributes
    ----------
    iswin : bool
        the bool to hold if a win or not for hitting winLoss
    """
    type_ = [ 'winLossPlayoffs' ]
    iswin: bool

@dataclass(kw_only=True)
class HittingHAA(Stats, SimpleHittingStat):
    """
    A class to represent a hitting homeAndAway statistic

    Attributes
    ----------
    ishome : bool
        the bool to hold if it ishome hitting homeAndAway
    """
    type_ = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class HittingHAAPlayoffs(Stats, SimpleHittingStat):
    """
    A class to represent a hitting homeAndAway statistic

    Attributes
    ----------
    ishome : bool
        the bool to hold if it ishome hitting homeAndAway
    """
    type_ = [ 'homeAndAwayPlayoffs' ]
    ishome: bool

@dataclass(kw_only=True)
class HittingCareer(Stats, SimpleHittingStat):
    """
    A class to represent a hitting career or careerPlayoffs statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the hitting career 
    numteams : str
        the number of teams for the hitting career
    """
    type_ = [ 'career', 'careerRegularSeason' ]
    gametype: str
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class HittingCareerPlayoffs(Stats, SimpleHittingStat):
    """
    A class to represent a hitting careerPlayoffs statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the hitting career 
    numteams : str
        the number of teams for the hitting career
    """
    type_ = [ 'careerPlayoffs' ]
    gametype: str
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class HittingSeason(Stats, SimpleHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    gametype : str
        the gametype code of the hitting season 
    numteams : str
        the number of teams for the hitting season
    """
    type_ = [ 'season', 'statsSingleSeason' ]
    gametype: Optional[str] = None
    numteams: Optional[str] = None


@dataclass(kw_only=True)
class HittingAdvancedSeason(Stats, AdvancedHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the hitting season 
    numteams : str
        the number of teams for the hitting season
    """
    type_ = [ 'careerAdvanced', 'seasonAdvanced' ]
    gametype: Optional[str] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class HittingYBY(Stats, SimpleHittingStat):
    """
    A class to represent a hitting yearbyyear or yearByYearPlayoffs statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the hitting yearbyyear 
    numteams : str
        the number of teams for the hitting yearbyyear
    """
    type_ = [ 'yearByYear' ]
    gametype: Optional[str] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class HittingYBYPlayoffs(Stats, SimpleHittingStat):
    """
    A class to represent a hitting yearByYearPlayoffs statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the hitting yearbyyear 
    numteams : str
        the number of teams for the hitting yearbyyear
    """
    type_ = [ 'yearByYearPlayoffs' ]
    gametype: Optional[str] = None
    numteams: Optional[str] = None

@dataclass
class OpponentsFacedHitting(Stats):
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
    type_ = [ 'opponentsFaced' ]
    group: str
    batter: Union[Person, dict]
    fieldingteam: Union[Team, dict]
    pitcher: Union[Person, dict]
    gametype: Optional[str]

@dataclass
class HittingSabermetrics(Stats):
    """
    A class to represent a hitting sabermetric statistic

    """
    type_ = [ 'sabermetrics' ]
    gametype: str
    woba: float
    wrc: float
    wrcplus: float
    rar: float
    war: float
    numteams: Optional[int] = None

@dataclass(kw_only=True)
class HittingLog(Stats, SimpleHittingStat):
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
    type_ = [ 'gameLog' ]
    positionsplayed: List[Position]
    ishome: bool
    iswin: bool
    game: Union[Game, dict]
    date: str
    gametype: str
    opponent: Union[Team, dict]

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
class HittingLog(Stats):
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
    type_ = [ 'playLog' ]
    opponent: Union[Team, dict]
    date: str
    gametype: str
    ishome: bool
    pitcher: Union[Person, dict]
    batter: Union[Person, dict]
    game: Union[Game, dict]
    details: Union[PlayDetails, dict]
    count: Union[Count, dict]
    playid: Optional[str]
    pitchnumber: int
    atbatnumber: int
    ispitch: bool

    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count)

@dataclass(kw_only=True)
class HittingPitchLog(Stats):
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
    type_ = [ 'pitchLog' ]
    opponent: Union[Team, dict]
    date: str
    gametype: str
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

@dataclass
class SprayChart(Stats):
    """
    centerfield : float
    leftcenterfield : float 
    leftfield : float
    rightcenterfield : float
    rightfield
    batter
    
    """
    type_ = [ 'sprayChart' ]
    batter: Union[Person, dict]
    centerfield: float
    leftcenterfield: float
    leftfield: float
    rightcenterfield: float
    rightfield: float

@dataclass(kw_only=True)
class HittingLastXGames(Stats, SimpleHittingStat):
    """
    A class to represent a lastXGames statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'lastXGames' ]
    numteams: int

@dataclass(kw_only=True)
class HittingDateRange(Stats, SimpleHittingStat):
    """
    A class to represent a byDateRange statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'byDateRange' ]
    numteams: int

@dataclass(kw_only=True)
class HittingDateRangeAdvanced(Stats, AdvancedHittingStat):
    """
    A class to represent a byDateRangeAdvanced statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'byDateRangeAdvanced' ]
    numteams: int

@dataclass(kw_only=True)
class HittingByMonth(Stats, AdvancedHittingStat):
    """
    A class to represent a byMonth hitting statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'byMonth' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class HittingByMonthPlayoffs(Stats, AdvancedHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    month : str
        the month of the stat
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'byMonthPlayoffs' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class HittingDayOfWeek(Stats, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    month : str
        the month of the stat
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'byDayOfWeek' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class HittingDayOfWeekPlayoffs(Stats, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    month : str
        the month of the stat
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'byDayOfWeekPlayoffs' ]
    month: int
    numteams: int



