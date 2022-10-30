from dataclasses import dataclass, field
from typing import Optional, Union

from .stats import Stats

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

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
class SeasonCatching(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'season', 'statsSingleSeason' ]

@dataclass(kw_only=True)
class CatchingYearByYearPlayoffs(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'yearByYearPlayoffs' ]

@dataclass(kw_only=True)
class CatchingYearByYear(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'yearByYear' ]

@dataclass(kw_only=True)
class CatchingProjected(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'projectedRos' ]

@dataclass(kw_only=True)
class CatchingCareer(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'career', 'careerRegularSeason' ]
    
@dataclass(kw_only=True)
class CatchingGameLog(Stats, SimpleCatching):
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
class CatchingLastXGames(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'lastXGames' ]

@dataclass(kw_only=True)
class CatchingByDateRange(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'byDateRange' ]

@dataclass(kw_only=True)
class CatchingByDayOfWeek(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'byDayOfWeek' ]
    dayofweek: int

@dataclass(kw_only=True)
class CatchingHomeAndAway(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class CatchingWinLoss(Stats, SimpleCatching):
    """
    A class to represent a catching winLoss statistic

    Attributes
    ----------
    """
    type_ = [ 'winLoss' ]
    iswin: bool