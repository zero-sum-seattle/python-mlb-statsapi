﻿from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.people import Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

from .stats import Stats

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
class FieldingSeasonAdvanced(Stats, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    type_ = ['seasonAdvanced' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingSingleSeasonAdvanced(Stats, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    type_ = [ 'statsSingleSeasonAdvanced' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingSeason(Stats, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    type_ = [ 'season' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingSingleSeason(Stats, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    type_ = [ 'statsSingleSeason' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingCareer(Stats, SimpleFielding):
    """
    A class to represent a fielding career statistic

    Attributes
    ----------
    """
    type_ = [ 'career' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position    

@dataclass(kw_only=True)
class FieldingCareerRegularSeason(Stats, SimpleFielding):
    """
    A class to represent a fielding career statistic

    Attributes
    ----------
    """
    type_ = [ 'careerRegularSeason' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position 

@dataclass(kw_only=True)
class FieldingCareerPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding career playoff statistic

    Attributes
    ----------
    """
    type_ = [ 'careerPlayoffs' ]
    position: Optional[Union[Position, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingHomeAndAway(Stats, SimpleFielding):
    """
    A class to represent a fielding homeAndAway statistic

    Attributes
    ----------
    """
    type_ = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class FieldingHomeAndAwayPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding homeAndAwayPlayoffs statistic

    Attributes
    ----------
    """
    type_ = [ 'homeAndAwayPlayoffs' ]
    ishome: bool

@dataclass(kw_only=True)
class FieldingYearByYear(Stats, SimpleFielding):
    """
    A class to represent a fielding yearByYear statistic

    Attributes
    ----------
    """
    type_ = [ 'yearByYear' ]

@dataclass(kw_only=True)
class FieldingYearByYearAdvanced(Stats, SimpleFielding):
    """
    A class to represent a fielding yearByYearAdvanced statistic

    Attributes
    ----------
    """
    type_ = [ 'yearByYearAdvanced']

@dataclass(kw_only=True)
class FieldingYearByYearPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    """
    type_ = [ 'yearByYearPlayoffs' ]

@dataclass(kw_only=True)
class FieldingWinLoss(Stats, SimpleFielding):
    """
    A class to represent a fielding winLoss statistic

    Attributes
    ----------
    """
    type_ = ['winLoss' ]
    iswin: bool

@dataclass(kw_only=True)
class FieldingWinLossPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding winLossPlayoffs statistic

    Attributes
    ----------
    """
    type_ = [ 'winLossPlayoffs' ]
    iswin: bool

@dataclass(kw_only=True)
class FieldingByDayOfWeek(Stats, SimpleFielding):
    """
    A class to represent a fielding byDayOfWeek statistic

    Attributes
    ----------
    """
    type_ = [ 'byDayOfWeek' ]
    dayofweek: str

@dataclass(kw_only=True)
class FieldingByDateRangeAdvanced(Stats, SimpleFielding):
    type_ = [ 'byDateRangeAdvanced' ]
    position: Union[Position, dict] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingByMonth(Stats, SimpleFielding):
    """
    A class to represent a fielding byMonth stat

    Attributes
    ----------
    """
    type_ = [ 'byMonth' ]
    month: int

@dataclass(kw_only=True)
class FieldingByMonthPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding byMonthPlayoffs stat

    Attributes
    ----------
    """
    type_ = [ 'byMonthPlayoffs' ]
    month: int

@dataclass(kw_only=True)
class FieldingLastXGames(Stats, SimpleFielding):
    """
    A class to represent a fielding lastXGames stat

    Attributes
    ----------
    """
    type_ = [ 'lastXGames' ]

@dataclass(kw_only=True)
class FieldingGameLog(Stats, SimpleFielding):
    """
    A class to represent a fielding gameLog stats

    Attributes
    ----------
    """
    type_ = [ 'gameLog' ]
    opponent: Union[Team, dict] = field(default_factory=dict)
    date: str
    ishome: bool
    iswin: bool
    position: Union[Position, dict] = field(default_factory=dict)
    game: Union[Game, dict] = field(default_factory=dict)


