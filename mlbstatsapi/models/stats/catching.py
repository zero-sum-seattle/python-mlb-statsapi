from dataclasses import dataclass
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
    _stat = ['season']


@dataclass(kw_only=True)
class CatchingSingleSeason(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['statsSingleSeason']


@dataclass(kw_only=True)
class CatchingYearByYearPlayoffs(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['yearByYearPlayoffs']


@dataclass(kw_only=True)
class CatchingYearByYear(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['yearByYear']


@dataclass(kw_only=True)
class CatchingProjected(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['projectedRos']


@dataclass(kw_only=True)
class CatchingCareer(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['career']


@dataclass(kw_only=True)
class CatchingCareerRegularSeason(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['careerRegularSeason']


@dataclass(kw_only=True)
class CatchingGameLog(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

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
class CatchingLastXGames(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['lastXGames']


@dataclass(kw_only=True)
class CatchingByDateRange(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['byDateRange']


@dataclass(kw_only=True)
class CatchingByDayOfWeek(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['byDayOfWeek']
    dayofweek: int


@dataclass(kw_only=True)
class CatchingHomeAndAway(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['homeAndAway']
    ishome: bool


@dataclass(kw_only=True)
class CatchingWinLoss(Splits, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    _stat = ['winLoss']
    iswin: bool

