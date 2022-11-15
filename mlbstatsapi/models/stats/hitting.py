from dataclasses import dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.people import Person, Position, Batter, Pitcher
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
    walksperstrikeout: Optional[str] = None
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
    _stat = ['winLoss']
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
    _stat = ['winLossPlayoffs']
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
    _stat = ['homeAndAway']
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
    _stat = ['homeAndAwayPlayoffs']
    ishome: bool


@dataclass(kw_only=True)
class HittingCareer(Splits, SimpleHittingStat):
    """
    A class to represent a hitting career or careerPlayoffs statistic

    #TODO Note that stat types career and careerregularseason, and careerplayoffs return same stat type of career
    Attributes
    ----------
    """
    _stat = ['career', 'careerRegularSeason', 'careerPlayoffs']


@dataclass(kw_only=True)
class HittingSeason(Splits, SimpleHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = ['season']


@dataclass(kw_only=True)
class HittingSingleSeason(Splits, SimpleHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = ['statsSingleSeason']


@dataclass(kw_only=True)
class HittingSeasonAdvanced(Splits, AdvancedHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = ['seasonAdvanced']


@dataclass(kw_only=True)
class HittingCareerAdvanced(Splits, AdvancedHittingStat):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = ['careerAdvanced']


@dataclass(kw_only=True)
class HittingYearByYear(Splits, SimpleHittingStat):
    """
    A class to represent a hitting yearbyyear or yearByYearPlayoffs statistic

    Attributes
    ----------
    """
    _stat = ['yearByYear']


@dataclass(kw_only=True)
class HittingYearByYearPlayoffs(Splits, SimpleHittingStat):
    """
    A class to represent a hitting yearByYearPlayoffs statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearPlayoffs']


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
    _stat = ['opponentsFaced']
    group: str
    batter: Union[Batter, dict]
    fieldingteam: Union[Team, dict]
    pitcher: Union[Pitcher, dict]

    def __post_init__(self):
        self.batter = Batter(**self.batter) if self.batter else self.batter
        self.pitcher = Pitcher(**self.pitcher) if self.pitcher else self.pitcher


@dataclass
class HittingSabermetrics(Splits):
    """
    A class to represent a hitting sabermetric statistic

    """
    _stat = ['sabermetrics']
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
    _stat = ['gameLog']
    positionsplayed: Optional[List[Position]] = field(default_factory=list)

    def __post_init__(self):
        if self.positionsplayed:
            self.positionsplayed = [Position(**position) for position in self.positionsplayed]


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

    def __post_init__(self):
        self.call = CodeDesc(**self.call)
        self.batside = CodeDesc(**self.batside)
        self.pitchhand = CodeDesc(**self.pitchhand) 
        self.type = CodeDesc(**self.type) if self.type else self.type


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
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    game: Union[Game, dict]
    details: Union[PlayDetails, dict]
    count: Union[Count, dict]
    pitchnumber: int
    atbatnumber: int
    ispitch: bool
    playid: Optional[str] = None
    _stat = ['playLog']

    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count)
        self.pitcher = Pitcher(**self.pitcher)
        self.batter = Batter(**self.batter)
        self.opponent = Team(**self.opponent)


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
    _stat = ['pitchLog']
    opponent: Union[Team, dict]
    date: str
    ishome: bool
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
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
        self.pitcher = Pitcher(**self.pitcher)
        self.batter = Batter(**self.batter)
        self.opponent = Team(**self.opponent)


@dataclass(kw_only=True)
class HittingLastXGames(Splits, SimpleHittingStat):
    """
    A class to represent a lastXGames statistic

    Attributes
    ----------
    """
    _stat = ['lastXGames']


@dataclass(kw_only=True)
class HittingDateRange(Splits, SimpleHittingStat):
    """
    A class to represent a byDateRange statistic

    Attributes
    ----------
    """
    _stat = ['byDateRange']


@dataclass(kw_only=True)
class HittingDateRangeAdvanced(Splits, AdvancedHittingStat):
    """
    A class to represent a byDateRangeAdvanced statistic

    Attributes
    ----------
    """
    _stat = ['byDateRangeAdvanced']


@dataclass(kw_only=True)
class HittingDateRangeAdvancedByMonth(Splits, AdvancedHittingStat):
    """
    A class to represent a byDateRangeAdvanced statistic

    Attributes
    ----------
    """
    _stat = ['byDateRangeAdvancedbyMonth']


@dataclass(kw_only=True)
class HittingByMonth(Splits, SimpleHittingStat):
    """
    A class to represent a byMonth hitting statistic

    Attributes
    ----------
    """
    _stat = ['byMonth']
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
    _stat = ['byMonthPlayoffs']
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
    _stat = ['byDayOfWeek']
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
    _stat = ['byDayOfWeekPlayoffs']
    dayofweek: int


@dataclass(kw_only=True)
class HittingExpectedStatistics(Splits):
    """
    A class to represent a excepted statistics statType: expectedStatistics.
    Attributes
    ----------
    avg : str
    slg : str
    woba : str
    wobaCon : str
    rank : int
    """
    _stat = ['expectedStatistics']
    avg: str
    slg: str
    woba: str
    wobacon: str
    gametype: str
    rank: Optional[int] = None


@dataclass(kw_only=True)
class HittingVsTeam(Splits, SimpleHittingStat):
    """
    A class to represent a vsTeam hitting statistic

    requires the use of the opposingTeamId parameter 
    Attributes
    ----------
    dayofweek : int
        the day of the week
    """
    _stat = ['vsTeam']
    opponent: Union[Team, dict]
    batter: Optional[Union[Person, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Person, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.pitcher = Pitcher(**self.pitcher) if self.pitcher else self.pitcher
        self.batter = Batter(**self.batter) if self.batter else self.batter
        self.opponent = Team(**self.opponent)


@dataclass(kw_only=True)
class HittingVsTeamTotal(Splits, SimpleHittingStat):
    """
    A class to represent a vsTeamTotal hitting statistic

    requires the use of the opposingTeamId parameter 

    Attributes
    ----------
    opponent: Team
        opponent team
    batter: Person
        batting person
    pitcher: Person
        pitching person
    """
    _stat = ['vsTeamTotal']
    opponent: Union[Team, dict]
    batter: Optional[Union[Person, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Person, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.pitcher = Pitcher(**self.pitcher) if self.pitcher else self.pitcher
        self.batter = Batter(**self.batter) if self.batter else self.batter
        self.opponent = Team(**self.opponent)


@dataclass(kw_only=True)
class HittingVsTeam5Y(Splits, SimpleHittingStat):
    """
    A class to represent a vsTeam5Y hitting statistic

    requires the use of the opposingTeamId parameter 

    Attributes
    ----------
    """
    _stat = ['vsTeam5Y']
    opponent: Union[Team, dict]
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Pitcher, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.pitcher = Pitcher(**self.pitcher) if self.pitcher else self.pitcher
        self.batter = Batter(**self.batter) if self.batter else self.batter
        self.opponent = Team(**self.opponent)


@dataclass(kw_only=True)
class HittingVsPlayer(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    This class is for the stat type vsPlayer*
    
    Requires the param opposingPlayerId set 

    Attributes
    ----------
    """
    _stat = ['vsPlayer']
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    opponent: Optional[Union[Team, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.pitcher = Pitcher(**self.pitcher)
        self.batter = Batter(**self.batter)
        self.opponent = Team(**self.opponent) if self.opponent else self.opponent


@dataclass(kw_only=True)
class HittingVsPlayerTotal(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    This class is for the stat type vsPlayer*

    Requires the param opposingPlayerId set

    Attributes
    ----------
    """
    _stat = ['vsPlayerTotal']
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    opponent: Optional[Union[Team, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.pitcher = Pitcher(**self.pitcher)
        self.batter = Batter(**self.batter)
        self.opponent = Team(**self.opponent) if self.opponent else self.opponent


@dataclass(kw_only=True)
class HittingVsPlayer5Y(Splits, SimpleHittingStat):
    """
    A class to represent a yearByYear hitting statistic

    This class is for the stat type vsPlayer*

    Requires the param opposingPlayerId set
    Attributes
    ----------
    """
    _stat = ['vsPlayer5Y']
    pitcher: Union[Pitcher, dict]
    batter: Union[Person, dict]
    opponent: Optional[Union[Team, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.pitcher = Pitcher(**self.pitcher)
        self.batter = Batter(**self.batter)
        self.opponent = Team(**self.opponent) if self.opponent else self.opponent
