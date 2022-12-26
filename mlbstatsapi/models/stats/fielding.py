from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.people import Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

from .stats import Stat, Split


@dataclass(repr=False)
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

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(kw_only=True, repr=False)
class FieldingSeasonAdvanced(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingCareerAdvanced(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingSingleSeasonAdvanced(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingSeason(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingSingleSeason(Split):
    """
    A class to represent a fielding statsSingleSeason statistic

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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingCareer(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingCareerPlayoffs(Split):
    """
    A class to represent a fielding careerPlayoffs statistic

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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingHomeAndAway(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingHomeAndAwayPlayoffs(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingYearByYear(Split):
    """
    A class to represent a fielding yearByYear statistic

    Attributes
    ----------
    """
    _stat = ['yearByYear']
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingYearByYearAdvanced(Split):
    """
    A class to represent a fielding yearByYearAdvanced statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearAdvanced']
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingYearByYearPlayoffs(Split):
    """
    A class to represent a fielding yearByYearPlayoffs statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearPlayoffs']
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)

@dataclass(kw_only=True, repr=False)
class FieldingWinLoss(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingWinLossPlayoffs(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingByDayOfWeek(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingByDateRangeAdvanced(Split):
    """
    A class to represent a fielding byDateRangeAdvanced stat

    Attributes
    ----------
    """
    _stat = ['byDateRangeAdvanced']
    position: Union[Position, dict] = field(default_factory=dict)

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingByMonth(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingByMonthPlayoffs(Split):
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
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingLastXGames(Split):
    """
    A class to represent a fielding lastXGames stat

    Attributes
    ----------
    """
    _stat = ['lastXGames']
    stat: Union[SimpleFieldingSplit, dict]

    def __post_init__(self):
        self.stat = SimpleFieldingSplit(**self.stat)
        super().__post_init__()


@dataclass(kw_only=True, repr=False)
class FieldingGameLog(Split):
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
        super().__post_init__()

