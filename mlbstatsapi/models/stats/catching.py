from dataclasses import dataclass
from typing import Optional, Union

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

from .stats import Split


@dataclass
class SimpleCatchingSplit:
    """
    A class to represent a simple catching split

    gamesplayed : int
        The number of games played by the catcher
    runs : int
        The number of runs given up while catching.
    homeruns : int
        The number of home runs given up while catching.
    strikeouts : int
        The number of strike outs while catching.
    baseonballs : int
        The number of base on balls while catching.
    intentionalwalks : int
        The number of intentional walks while catching.
    hits : int
        The number of hits while catching.
    hitbypitch : int
        The number of batters hit by a pitch while catching.
    avg : str
        The batting average while catching.
    atbats : int
        The number of at bats while catching.
    obp : str
        The on base percentage while catching.
    slg : str
        The slugging percentage while catching.
    ops : str
        The on-base slugging while catching.
        see also: https://www.mlb.com/glossary/standard-stats/on-base-plus-slugging
    caughtstealing : int
        The number of runners caught stealing by the catcher.
    stolenbases : int
        The number of stolen bases while catching.
    stolenbasepercentage : str
        The stolen base percentage against the catcher. 
    earnedruns : int
        The earned run amount against the catcher.
    battersfaced : int
        The number of batters faced while catching.
    gamespitched : int
        The number of games pitched while catching.
    hitbatsmen : int
        The number of batters hit by pitches while catching.
    wildpitches : int
        The number of wild pitches while catching.
    pickoffs : int
        The number of pick offs while catching.
    totalbases : int
        The total number of bases
    strikeoutwalkratio : str
        The strike out to walk ratio while catching.
    catchersinterference : int
        The number of times catcher interference commited
    sacbunts : int
        The number of sac bunts performed while catching.
    sacflies : int
        The number of sac flies while catching.
    passedball : int
        The number of passed balls while catching.
    """
    gamesplayed: Optional[int] = None
    runs: Optional[int] = None
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
    stolenbasepercentage: Optional[str] = None
    earnedruns: Optional[int] = None
    battersfaced: Optional[int] = None
    gamespitched: Optional[int] = None
    hitbatsmen: Optional[int] = None
    wildpitches: Optional[int] = None
    pickoffs: Optional[int] = None
    totalbases: Optional[int] = None
    strikeoutwalkratio: Optional[str] = None
    catchersinterference: Optional[int] = None
    sacbunts: Optional[int] = None
    sacflies: Optional[int] = None
    passedball: Optional[int] = None


@dataclass(kw_only=True)
class CatchingSeason(Split):
    """
    A class to represent a catching season statistic

    Attributes
    ----------
    """
    _stat = ['season']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)


@dataclass(kw_only=True)
class CatchingSingleSeason(Split):
    """
    A class to represent a catching statsSingleSeason statistic

    Attributes
    ----------
    """
    _stat = ['statsSingleSeason']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingYearByYearPlayoffs(Split):
    """
    A class to represent a catching yearByYearPlayoffs statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearPlayoffs']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingYearByYear(Split):
    """
    A class to represent a catching yearByYear statistic

    Attributes
    ----------
    """
    _stat = ['yearByYear']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingProjected(Split):
    """
    A class to represent a catching projectedRos statistic

    Attributes
    ----------
    """
    _stat = ['projectedRos']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingCareer(Split):
    """
    A class to represent a catching career statistic

    Attributes
    ----------
    """
    _stat = ['career']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingCareerRegularSeason(Split):
    """
    A class to represent a catching careerRegularSeason statistic

    Attributes
    ----------
    """
    _stat = ['careerRegularSeason']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingGameLog(Split):
    """
    A class to represent a catching gameLog statistic

    Attributes
    ----------
    """
    _stat = ['gameLog']
    ishome: bool
    iswin: bool
    date: str
    game: Union[Game, dict]
    opponent: Union[Team, dict]

@dataclass(kw_only=True)
class CatchingLastXGames(Split):
    """
    A class to represent a catching lastXGames statistic

    Attributes
    ----------
    """
    _stat = ['lastXGames']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingByDateRange(Split):
    """
    A class to represent a catching byDateRange statistic

    Attributes
    ----------
    """
    _stat = ['byDateRange']
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingByDayOfWeek(Split):
    """
    A class to represent a catching byDayOfWeek statistic

    Attributes
    ----------
    """
    _stat = ['byDayOfWeek']
    dayofweek: int
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingHomeAndAway(Split):
    """
    A class to represent a catching homeAndAway statistic

    Attributes
    ----------
    """
    _stat = ['homeAndAway']
    ishome: bool
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)

@dataclass(kw_only=True)
class CatchingWinLoss(Split):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['winLoss']
    iswin: bool
    stat: Union[SimpleCatchingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleCatchingSplit(**self.stat)
