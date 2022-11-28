from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.people import Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

from .stats import Stat


@dataclass
class SimpleFieldingSplit:
    """
    A class to represent a simple fielding split

    gamesplayed: int
        The number of games played 
    gamesstarted: int
        The number of games started
    caughtstealing: int
        The number of runners caught stealing
    stolenbases: int
        The number of stolen bases 
    stolenbasepercentage: str
        The stolen base percentage
    assists: int
        The number of assists
    putouts: int
        The number of put outs
    errors: int
        The number of errors commited
    chances: int
        The number of chances
    fielding: str
        The number of fielding
    rangefactorpergame: str
        Range rating per game.
        see also: https://www.mlb.com/glossary/advanced-stats/range-factor
    rangefactorper9inn: str
        Range factor per 9 innings.
        see also: https://www.mlb.com/glossary/advanced-stats/range-factor
    innings: str
        The number of innings played.
    games: int
        The number of games played.
    passedball: int
        The number of passed balls.
    doubleplays: int
        The number of double plays.
    tripleplays: int
        The number of triple plays.
    catcherera: str
        The catcher ERA of the fielding stat.
    catchersinterference: int
        The number of times catchers interfence was commited.
    wildpitches: int
        The number of wild pitches.
    throwingerrors: int
        The number of throwing errors.
    pickoffs: int
        The number of pick offs.
    """
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    gamesplayed: Optional[int] = None
    gamesstarted: Optional[int] = None
    caughtstealing: Optional[int] = None
    stolenbases: Optional[int] = None
    stolenbasepercentage: Optional[str] = None
    assists: Optional[int] = None
    putouts: Optional[int] = None
    errors: Optional[int] = None
    chances: Optional[int] = None
    fielding: Optional[str] = None
    rangefactorpergame: Optional[str] = None
    rangefactorper9inn: Optional[str] = None
    innings: Optional[str] = None
    games: Optional[int] = None
    passedball: Optional[int] = None
    doubleplays: Optional[int] = None
    tripleplays: Optional[int] = None
    catcherera: Optional[str] = None
    catchersinterference: Optional[int] = None
    wildpitches: Optional[int] = None
    throwingerrors: Optional[int] = None
    pickoffs: Optional[int] = None


@dataclass(kw_only=True)
class FieldingSeasonAdvanced(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding season Advanced statistic
    Attributes
    ----------
    position : Position
        The position of the player
    """
    _stat = ['seasonAdvanced']
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        self.position = Position(**self.position) if self.position else self.position


@dataclass(kw_only=True)
class FieldingCareerAdvanced(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding career Advanced statistic
    Attributes
    ----------
    position : Position
        The position of the player
    """
    _stat = ['careerAdvanced']
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        self.position = Position(**self.position) if self.position else self.position


@dataclass(kw_only=True)
class FieldingSingleSeasonAdvanced(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    position : Position
        The position of the player
    """
    _stat = ['statsSingleSeasonAdvanced']
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        self.position = Position(**self.position) if self.position else self.position


@dataclass(kw_only=True)
class FieldingSeason(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    position : Position
        The position of the player
    """
    _stat = ['season']
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        self.position = Position(**self.position) if self.position else self.position


@dataclass(kw_only=True)
class FieldingSingleSeason(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    position : Position
        The position of the player
    """
    _stat = ['statsSingleSeason']
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        self.position = Position(**self.position) if self.position else self.position


@dataclass(kw_only=True)
class FieldingCareer(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding career statistic

    Attributes
    ----------
    position : Position
        The position of the player
    """
    _stat = ['career', 'careerRegularSeason']
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        self.position = Position(**self.position) if self.position else self.position   


@dataclass(kw_only=True)
class FieldingCareerPlayoffs(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding career playoff statistic

    Attributes
    ----------
    position : Position
        The position of the player
    """
    _stat = ['careerPlayoffs']
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        self.position = Position(**self.position) if self.position else self.position


@dataclass(kw_only=True)
class FieldingHomeAndAway(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding homeAndAway statistic

    Attributes
    ----------
    ishome : bool
        A bool value for is the game at home
    """
    _stat = ['homeAndAway']
    ishome: bool
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingHomeAndAwayPlayoffs(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding homeAndAwayPlayoffs statistic

    Attributes
    ----------
    ishome : bool
        A bool value for is the game at home
    """
    _stat = ['homeAndAwayPlayoffs']
    ishome: bool
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingYearByYear(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding yearByYear statistic

    Attributes
    ----------
    """
    _stat = ['yearByYear']
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingYearByYearAdvanced(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding yearByYearAdvanced statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearAdvanced']
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingYearByYearPlayoffs(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearPlayoffs']
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingWinLoss(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding winLoss statistic

    Attributes
    ----------
    iswin : bool
        is the game a win
    """
    _stat = ['winLoss']
    iswin: bool
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingWinLossPlayoffs(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding winLossPlayoffs statistic

    Attributes
    ----------
    iswin : bool
        is the game a win
    """
    _stat = ['winLossPlayoffs']
    iswin: bool
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingByDayOfWeek(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding byDayOfWeek statistic

    Attributes
    ----------
    """
    _stat = ['byDayOfWeek']
    dayofweek: str
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingByDateRangeAdvanced(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding byMonth stat

    Attributes
    ----------
    position : Position
        The position of the player
    """
    _stat = ['byDateRangeAdvanced']
    position: Union[Position, dict] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingByMonth(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding byMonth stat

    Attributes
    ----------
    month : int
        the month of the stat
    """
    _stat = ['byMonth']
    month: int
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingByMonthPlayoffs(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding byMonthPlayoffs stat

    Attributes
    ----------
    month : int
        the month of the stat
    """
    _stat = ['byMonthPlayoffs']
    month: int
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingLastXGames(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding lastXGames stat

    Attributes
    ----------
    """
    _stat = ['lastXGames']
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True)
class FieldingGameLog(Stat, SimpleFieldingSplit):
    """
    A class to represent a fielding gameLog stats

    Attributes
    ----------
    """
    _stat = ['gameLog']
    opponent: Union[Team, dict] = field(default_factory=dict)
    date: str
    ishome: bool
    iswin: bool
    position: Union[Position, dict] = field(default_factory=dict)
    game: Union[Game, dict] = field(default_factory=dict)
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)


#
# These dataclasses are for the game stats end point only
# url: https://statsapi.mlb.com/api/v1/people/663728/stats/game/715757
# The gamelog stats in this JSON have different keys set for their stat
# and group. This breaks my logic of handling stat classes
#

@dataclass
class FieldingSplit:
    """
    A dataclass to handle a fielding gamelog stat for the game player stats endpoint

    Attributes
    ----------
    gamesstarted : int
    caughtstealing : int
    stolenbases : int
    stolenbasepercentage : str
    assists : int
    putouts : int
    errors : int
    chances : int
    fielding : str
    passedball : int
    pickoffs : int
    """
    gamesstarted : int
    caughtstealing : int
    stolenbases : int
    stolenbasepercentage : str
    assists : int
    putouts : int
    errors : int
    chances : int
    fielding : str
    passedball : int
    pickoffs : int


@dataclass
class FieldingGameLogStat:
    type: str
    group: str
    stat: Union[FieldingSplit, dict]
    _type = ['fielding']

    def __post_init__(self):
        self.stat = FieldingSplit(**self.stat)