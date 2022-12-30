from dataclasses import dataclass, field
from typing import Optional, Union, List

from .stats import Split

@dataclass
class SimpleGameStats:
    """
    A class to represent a simple game statistics

    Attributes
    ----------
    firstdateplayed : str
        first date of game played
    gamesplayed : int
        number of the games player
    gamesstarted : int
        number of the games started
    lastdateplayed : str
        last date of the game played
    """
    firstdateplayed: str
    gamesplayed: int
    gamesstarted: int
    lastdateplayed: str

    def __post_init__(self):
        super().__post_init__()

@dataclass(kw_only=True)
class SeasonGame(Split):
    """
    A class to represent a game statistic

    Used for the following stat types:
    season, career, careerRegularSeason, careerPlayoffs, statsSingleSeason
    """
    type_ = ['season', 'statsSingleSeason']

    def __post_init__(self):
        super().__post_init__()

@dataclass(kw_only=True)
class CareerGame(Split):
    """
    A class to represent a game statistic
    """
    type_ = ['career']

    def __post_init__(self):
        super().__post_init__()

@dataclass(kw_only=True)
class CareerRegularSeasonGame(Split, SimpleGameStats):
    """
    A class to represent a game statistic
    """
    type_ = ['careerRegularSeason']

    def __post_init__(self):
        super().__post_init__()

@dataclass(kw_only=True)
class CareerPlayoffsGame(Split, SimpleGameStats):
    """
    A class to represent a game statistic

    """
    type_ = ['careerPlayoffs']

    def __post_init__(self):
        super().__post_init__()