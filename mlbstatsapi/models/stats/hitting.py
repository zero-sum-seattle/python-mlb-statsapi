from dataclasses import dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.people import Person, Position, Batter, Pitcher
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game
from mlbstatsapi.mlb_module import merge_keys
from mlbstatsapi.models.data import (
    PitchData,
    HitData,
    Count,
    PlayDetails
)
from .stats import (
    Sabermetrics,
    ExpectedStatistics,
    Split
)
@dataclass(repr=False)
class AdvancedHittingSplit:
    """
    A class to represent a advanced hitting statistics

    Attributes
    ----------
    plateappearances : int
        The number of plate appearances.
    totalbases : int
        The total number of bases.
    leftonbase : int
        The amount of runners left on base.
    sacbunts : int
        The amount of sac bunts.
    sacflies : int
        The amount of sac flies.
    babip : str
        Batting Average on Balls in Play.
        see here: https://www.mlb.com/glossary/advanced-stats/babip
    extrabasehits : int
        The amount of extra base hits. e.g doubles, triples, homeruns
        see here: https://www.mlb.com/glossary/standard-stats/extra-base-hit
    hitbypitch : int
        The amount of times the batter has been hit by a pitch.
    gidp : int
        The amount of hits that lead to a double play.
        see here: https://www.mlb.com/glossary/standard-stats/ground-into-double-play
    gidpopp : int
        The amount of GIDP opportunities. 
    numberofpitches : int
        The number of pitches the batter has faced.
        see here: https://www.mlb.com/glossary/standard-stats/number-of-pitches
    pitchesperplateappearance : str
        The avg amount of pitches per plate appearance for the hitter.
        see here: https://www.mlb.com/glossary/advanced-stats/pitches-per-plate-appearance
    walksperplateappearance : str
        The avg walks per plate appearance.
        see here: https://www.mlb.com/glossary/advanced-stats/walk-rate
    strikeoutsperplateappearance : str
        The amount of strike outs per plate appearance.
        see here: https://www.mlb.com/glossary/advanced-stats/plate-appearances-per-strikeout
    homerunsperplateappearance : str
        The amount of home runs per plate appearance.
        see here: https://en.wikipedia.org/wiki/At_bats_per_home_run
    walksperstrikeout : str
        The amount of walks per strike out.
        see here: https://www.mlb.com/glossary/advanced-stats/strikeout-to-walk-ratio
    iso : str
        Isolasted power.
        see also: https://www.mlb.com/glossary/advanced-stats/isolated-power
    reachedonerror : int
        The amount of times the batter has reached base on a error.
        see also: https://www.mlb.com/glossary/standard-stats/reached-on-error
    walkoffs : int
        The amount of times the batter has walked off a game.
        see also: https://www.mlb.com/glossary/standard-stats/walk-off
    flyouts : int
        The amount of flyouts for the batter.
        see also: https://www.mlb.com/glossary/standard-stats/flyout
    totalswings : int
        The amount of swings the batter has taken at the plate.
    swingandmisses : int
        The amount of swing and misses the batter has taken at the plate.
    ballsinplay : int
        The amount of balls the batter has put in play.
    popouts : int
        The amount of popouts the batter has put in play.
    lineouts : int
        The amount of lineouts the batter has put in play.
    groundouts : int
        The amount of groundouts the batter has hit into.
    flyhits : int
        The amount of fly hits the batter has hit.
    pophits : int
        The amount of pop hits the batter has hit.
    groundhits : int
        The amount of ground hits the batter has hit.
    linehits : int
        The amount of line hits the the batter has hit.
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

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class SimpleHittingSplit:
    """
    A class to represent a simple hitting statistics
    
    gamesplayed : int
        The number of games played by the batter.
    groundouts : int
        The amount of groundouts hit by the batter.
    airouts : int
        The amount of air hits by the batter.
    runs : int
        The amount of runs plated by the batter.
    doubles : int
        The amount of doubles hit by the batter.
    triples : int
        The amount of triples hit by the batter.
    homeruns : int
        The amount of homeruns hit by the batter.
    strikeouts : int
        The amount of strikeouts for the batter.
    baseonballs : int
        The amount of base on balls (walks) for the batter. 
    intentionalwalks : int
        The number of intentional walks for the batter.
    hits : int
        The number of hits for the batter.
    hitbypitch : int
        The number of pitches the batter has been hit by.
    avg : str
        The batting avg of the batter.
    atbats : int
        The number of at bats of the batter.
    obp : str
        The on base percentage of the batter.
        see also: https://www.mlb.com/glossary/standard-stats/on-base-percentage
    slg : str
        The slugging percentage of the batter.
        see also: https://www.mlb.com/glossary/standard-stats/slugging-percentage
    ops : str
        The on-base plug slugging of the batter.
        see also: https://www.mlb.com/glossary/standard-stats/on-base-plus-slugging
    caughtstealing : int
        The amount of times the batter has been caught stealing.
    stolenbases : int
        The amount of stolen bases acheived by the batter.
    stolenbasepercentage : int
        The stolen base percentage of the batter.
    groundintodoubleplay : int
        The number of times the batter has hit into a double play.
    groundintotripleplay : int
        The number of times the batter has hit into a triple play.
    numberofpitches : int
        The number of pitches the batter has faced. 
    plateappearances : int
        The number of plate appearances of the batter. 
    totalbases : int
        The number of bases acheived by batter.
    rbi : int
        The number of Runs Batted In by the batter.
        see also: https://www.mlb.com/glossary/standard-stats/runs-batted-in
    leftonbase : int
        The number of runners left on base by the batter.
    sacbunts : int
        The number of sac bunts performed by the batter.
    sacflies : int
        The number of sac flies performed by the batter.
    babip : str
        The batting average of balls in play of the batter.
        see also: https://www.mlb.com/glossary/advanced-stats/babip
    groundoutstoairouts : int
        The groundout-to-airout ratio of the batter.
        see also: https://www.mlb.com/glossary/advanced-stats/babip
    catchersinterference : int
        The number of times the batter has reached base due to catchers interference.
        see also: https://www.mlb.com/glossary/rules/catcher-interference
    atbatsperhomerun : int
        The number of bats per home run of the batter.
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

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(kw_only=True, repr=False)
class HittingWinLoss(Split):
    """
    A class to represent a hitting winLoss statistic

    Attributes
    ----------
    iswin : bool
        the bool to hold if a win or not for hitting winLoss
    stat : dict
        the hitting split stat
    """
    _stat = ['winLoss']
    iswin: bool
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingWinLossPlayoffs(Split):
    """
    A class to represent a hitting winLossPlayoffs statistic

    Attributes
    ----------
    iswin : bool
        the bool to hold if a win or not for hitting winLoss
    stat : dict
        the hitting split stat
    """
    _stat = ['winLossPlayoffs']
    iswin: bool
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingHomeAndAway(Split):
    """
    A class to represent a hitting homeAndAway statistic

    Attributes
    ----------
    ishome : bool
        the bool to hold if it ishome hitting homeAndAway
    stat : dict
        the hitting split stat
    """
    _stat = ['homeAndAway']
    ishome: bool
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingHomeAndAwayPlayoffs(Split):
    """
    A class to represent a hitting homeAndAway Playoff statistic

    Attributes
    ----------
    ishome : bool
        the bool to hold if it ishome hitting homeAndAway
    stat : dict
        the hitting split stat
    """
    _stat = ['homeAndAwayPlayoffs']
    ishome: bool
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingCareer(Split):
    """
    A class to represent a hitting career, careerRegularSeason or careerPlayoffs statistic

    Attributes
    ----------
    stat : dict
        the hitting split stat
    """
    _stat = ['career', 'careerRegularSeason', 'careerPlayoffs']
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        super().__post_init__()
        self.stat = SimpleHittingSplit(**self.stat)


@dataclass(kw_only=True, repr=False)
class HittingSeason(Split):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    stat : dict
        the hitting split stat
    """
    _stat = ['season']
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        super().__post_init__()
        self.stat = SimpleHittingSplit(**self.stat)

@dataclass(kw_only=True, repr=False)
class HittingSingleSeason(Split):
    """
    A class to represent a hitting statsSingleSeason statistic

    Attributes
    ----------
    stat : dict
        the hitting split stat
    """
    _stat = ['statsSingleSeason']
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        super().__post_init__()
        self.stat = SimpleHittingSplit(**self.stat)

@dataclass(kw_only=True, repr=False)
class HittingSeasonAdvanced(Split):
    """
    A class to represent a hitting seasonAdvanced statistic

    Attributes
    ----------
    stat : dict
        the hitting split stat
    """
    _stat = ['seasonAdvanced']
    stat: Union[AdvancedHittingSplit, dict]

    def __post_init__(self):
        super().__post_init__()
        self.stat = AdvancedHittingSplit(**self.stat)

@dataclass(kw_only=True, repr=False)
class HittingCareerAdvanced(Split):
    """
    A class to represent a hitting season statistic

    Attributes
    ----------
    """
    _stat = ['careerAdvanced']
    stat: Union[AdvancedHittingSplit, dict]

    def __post_init__(self):
        self.stat = AdvancedHittingSplit(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingYearByYear(Split):
    """
    A class to represent a hitting yearbyyear or yearByYearPlayoffs statistic

    Attributes
    ----------
    """
    _stat = ['yearByYear']
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingYearByYearPlayoffs(Split):
    """
    A class to represent a hitting yearByYearPlayoffs statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearPlayoffs']
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class OpponentsFacedHitting(Split):
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
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingSabermetrics(Split):
    """
    A class to represent a hitting sabermetric statistic

    """
    _stat = ['sabermetrics']
    stat: Union[Sabermetrics, dict]

    def __post_init__(self):
        self.stat = Sabermetrics(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingGameLog(Split):
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    positionsplayed : List[Position]
    stat : SimpleHittingSplit
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
    stat: Union[SimpleHittingSplit, dict] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.positionsplayed:
            self.positionsplayed = [Position(**position) for position in self.positionsplayed]
        self.stat = SimpleHittingSplit(**self.stat) if self.stat else self.stat
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingPlay:
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    """
    details: Union[PlayDetails, dict]
    count: Union[Count, dict]
    ispitch: bool
    pitchnumber: Optional[int] = None
    atbatnumber: Optional[int] = None
    index: Optional[str] = None
    playid: Optional[str] = None
    pitchdata: Optional[Union[PitchData, dict]] = field(default_factory=dict)
    hitdata: Optional[Union[HitData, dict]] = field(default_factory=dict)
    starttime: Optional[str] = None
    endtime: Optional[str] = None
    type: Optional[str] = None


    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count)

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))
        
@dataclass(kw_only=True, repr=False)
class HittingPlayLog(Split):
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
    stat: Union[HittingPlay, dict]
    opponent: Optional[Union[Team, dict]] = field(default_factory=dict)
    date: Optional[str] = None
    ishome: Optional[bool] = None
    pitcher: Optional[Union[Pitcher, dict]] = field(default_factory=dict)
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)
    game: Optional[Union[Game, dict]] = field(default_factory=dict)

    _stat = ['playLog']

    def __post_init__(self):
        self.stat = HittingPlay(**self.stat['play'])
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingPitchLog(Split):
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
    stat: PlayDetails
    _stat = ['pitchLog']
    opponent: Union[Team, dict]
    date: str
    ishome: bool
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    game: Union[Game, dict]
    playid: Optional[str] = None

    def __post_init__(self):
        self.stat = HittingPlay(**self.stat['play'])
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingLastXGames(Split):
    """
    A class to represent a lastXGames statistic

    Attributes
    ----------
    """
    _stat = ['lastXGames']
    stat: Union[SimpleHittingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingDateRange(Split):
    """
    A class to represent a byDateRange statistic

    Attributes
    ----------
    """
    _stat = ['byDateRange']
    stat: Union[SimpleHittingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingDateRangeAdvanced(Split):
    """
    A class to represent a byDateRangeAdvanced statistic

    Attributes
    ----------
    """
    _stat = ['byDateRangeAdvanced']
    stat: Union[AdvancedHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = AdvancedHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingDateRangeAdvancedByMonth(Split):
    """
    A class to represent a byDateRangeAdvanced statistic

    Attributes
    ----------
    """
    _stat = ['byDateRangeAdvancedbyMonth']
    stat: Union[AdvancedHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = AdvancedHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingByMonth(Split):
    """
    A class to represent a byMonth hitting statistic

    Attributes
    ----------
    """
    _stat = ['byMonth']
    month: int
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingByMonthPlayoffs(Split):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    month : str
        the month of the stat
    """
    _stat = ['byMonthPlayoffs']
    month: int
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingDayOfWeek(Split):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    dayofweek : int
        the day of the week
    """
    _stat = ['byDayOfWeek']
    dayofweek: int
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)


@dataclass(kw_only=True, repr=False)
class HittingDayOfWeekPlayoffs(Split):
    """
    A class to represent a yearByYear hitting statistic

    Attributes
    ----------
    dayofweek : int
        the day of the week
    """
    _stat = ['byDayOfWeekPlayoffs']
    dayofweek: int
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingExpectedStatistics(Split):
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
    stat: Union[ExpectedStatistics, dict]

    def __post_init__(self):
        self.stat = ExpectedStatistics(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class HittingVsTeam(Split):
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
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Pitcher, dict]] = field(default_factory=dict)
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingVsTeamTotal(Split):
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
    batter: Optional[Union[Batter, dict]] = field(default_factory=dict)
    pitcher: Optional[Union[Pitcher, dict]] = field(default_factory=dict)
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingVsTeam5Y(Split):
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
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingVsPlayer(Split):
    """
    A class to represent a yearByYear hitting statistic

    This class is for the stat type vsPlayer*
    
    Requires the param opposingPlayerId set 

    Attributes
    ----------
    pitcher : Pitcher
        The pitcher of the hitting vsplayer stat
    batter : Batter
        The batter of the hitting vsplayer stat
    opponent : Team
        The team of the hitting vsplayer stat
    """
    _stat = ['vsPlayer']
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    opponent: Optional[Union[Team, dict]] = field(default_factory=dict)
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingVsPlayerTotal(Split):
    """
    A class to represent a yearByYear hitting statistic

    This class is for the stat type vsPlayer*

    Requires the param opposingPlayerId set

    Attributes
    ----------
    pitcher : Pitcher
        The pitcher of the hitting vsplayer stat
    batter : Batter
        The batter of the hitting vsplayer stat
    opponent : Team
        The team of the hitting vsplayer stat
    """
    _stat = ['vsPlayerTotal']
    pitcher: Union[Pitcher, dict]
    batter: Union[Batter, dict]
    opponent: Optional[Union[Team, dict]] = field(default_factory=dict)
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()

@dataclass(kw_only=True, repr=False)
class HittingVsPlayer5Y(Split):
    """
    A class to represent a yearByYear hitting statistic

    This class is for the stat type vsPlayer*

    Requires the param opposingPlayerId set

    Attributes
    ----------
    pitcher : Pitcher
        The pitcher of the hitting vsplayer stat
    batter : Batter
        The batter of the hitting vsplayer stat
    opponent : Team
        The team of the hitting vsplayer stat
    """
    _stat = ['vsPlayer5Y']
    pitcher: Union[Pitcher, dict]
    batter: Union[Person, dict]
    opponent: Optional[Union[Team, dict]] = field(default_factory=dict)
    stat: Union[SimpleHittingSplit, dict]
    
    def __post_init__(self):
        self.stat = SimpleHittingSplit(**self.stat)
        super().__post_init__()
