from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.people import Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

from .stats import Splits

@dataclass
class SimpleFielding:
    """
    A class to represent a simple fielding statistics

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
class FieldingSeasonAdvanced(Splits, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    _stat = ['seasonAdvanced' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingSingleSeasonAdvanced(Splits, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    _stat = [ 'statsSingleSeasonAdvanced' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingSeason(Splits, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    _stat = [ 'season' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingSingleSeason(Splits, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    _stat = [ 'statsSingleSeason' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingCareer(Splits, SimpleFielding):
    """
    A class to represent a fielding career statistic

    Attributes
    ----------
    """
    _stat = [ 'career' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position    

@dataclass(kw_only=True)
class FieldingCareerRegularSeason(Splits, SimpleFielding):
    """
    A class to represent a fielding career statistic

    Attributes
    ----------
    """
    _stat = [ 'careerRegularSeason' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position 

@dataclass(kw_only=True)
class FieldingCareerPlayoffs(Splits, SimpleFielding):
    """
    A class to represent a fielding career playoff statistic

    Attributes
    ----------
    """
    _stat = [ 'careerPlayoffs' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingHomeAndAway(Splits, SimpleFielding):
    """
    A class to represent a fielding homeAndAway statistic

    Attributes
    ----------
    """
    _stat = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class FieldingHomeAndAwayPlayoffs(Splits, SimpleFielding):
    """
    A class to represent a fielding homeAndAwayPlayoffs statistic

    Attributes
    ----------
    """
    _stat = [ 'homeAndAwayPlayoffs' ]
    ishome: bool

@dataclass(kw_only=True)
class FieldingYearByYear(Splits, SimpleFielding):
    """
    A class to represent a fielding yearByYear statistic

    Attributes
    ----------
    """
    _stat = [ 'yearByYear' ]

@dataclass(kw_only=True)
class FieldingYearByYearAdvanced(Splits, SimpleFielding):
    """
    A class to represent a fielding yearByYearAdvanced statistic

    Attributes
    ----------
    """
    _stat = [ 'yearByYearAdvanced']

@dataclass(kw_only=True)
class FieldingYearByYearPlayoffs(Splits, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    _stat = [ 'yearByYearPlayoffs' ]

@dataclass(kw_only=True)
class FieldingWinLoss(Splits, SimpleFielding):
    """
    A class to represent a fielding winLoss statistic

    Attributes
    ----------
    """
    _stat = ['winLoss' ]
    iswin: bool

@dataclass(kw_only=True)
class FieldingWinLossPlayoffs(Splits, SimpleFielding):
    """
    A class to represent a fielding winLossPlayoffs statistic

    Attributes
    ----------
    """
    _stat = [ 'winLossPlayoffs' ]
    iswin: bool

@dataclass(kw_only=True)
class FieldingByDayOfWeek(Splits, SimpleFielding):
    """
    A class to represent a fielding byDayOfWeek statistic

    Attributes
    ----------
    """
    _stat = [ 'byDayOfWeek' ]
    dayofweek: str

@dataclass(kw_only=True)
class FieldingByDateRangeAdvanced(Splits, SimpleFielding):
    """
    A class to represent a fielding byMonth stat

    Attributes
    ----------
    """
    _stat = [ 'byDateRangeAdvanced' ]
    position: Union[Position, dict] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingByMonth(Splits, SimpleFielding):
    """
    A class to represent a fielding byMonth stat

    Attributes
    ----------
    """
    _stat = [ 'byMonth' ]
    month: int

@dataclass(kw_only=True)
class FieldingByMonthPlayoffs(Splits, SimpleFielding):
    """
    A class to represent a fielding byMonthPlayoffs stat

    Attributes
    ----------
    """
    _stat = [ 'byMonthPlayoffs' ]
    month: int

@dataclass(kw_only=True)
class FieldingLastXGames(Splits, SimpleFielding):
    """
    A class to represent a fielding lastXGames stat

    Attributes
    ----------
    """
    _stat = [ 'lastXGames' ]

@dataclass(kw_only=True)
class FieldingGameLog(Splits, SimpleFielding):
    """
    A class to represent a fielding gameLog stats

    Attributes
    ----------
    """
    _stat = [ 'gameLog' ]
    opponent: Union[Team, dict] = field(default_factory=dict)
    date: str
    ishome: bool
    iswin: bool
    position: Union[Position, dict] = field(default_factory=dict)
    game: Union[Game, dict] = field(default_factory=dict)
