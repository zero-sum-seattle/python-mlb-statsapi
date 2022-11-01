from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

from .stats import Splits


@dataclass
class SimpleCatching:
    """
    A class to represent a simple catching statistics

    Used for the following stat types:
    season
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
class CatchingSeason(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'season' ]

@dataclass(kw_only=True)
class CatchingSingleSeason(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'statsSingleSeason' ]

@dataclass(kw_only=True)
class CatchingYearByYearPlayoffs(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'yearByYearPlayoffs' ]

@dataclass(kw_only=True)
class CatchingYearByYear(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'yearByYear' ]

@dataclass(kw_only=True)
class CatchingProjected(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'projectedRos' ]

@dataclass(kw_only=True)
class CatchingCareer(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'career' ]

@dataclass(kw_only=True)
class CatchingCareerRegularSeason(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'careerRegularSeason' ]

@dataclass(kw_only=True)
class CatchingGameLog(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'gameLog' ]
    ishome: bool
    iswin: bool
    date: str
    game: Union[Game, dict]
    opponent: Union[Team, dict]

@dataclass(kw_only=True)
class CatchingLastXGames(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'lastXGames' ]

@dataclass(kw_only=True)
class CatchingByDateRange(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'byDateRange' ]

@dataclass(kw_only=True)
class CatchingByDayOfWeek(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'byDayOfWeek' ]
    dayofweek: int

@dataclass(kw_only=True)
class CatchingHomeAndAway(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class CatchingWinLoss(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'winLoss' ]
    iswin: bool

