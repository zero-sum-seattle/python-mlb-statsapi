from dataclasses import dataclass, field
from typing import Optional, Union, List

from .stats import Splits

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

@dataclass(kw_only=True)
class SeasonGame(Splits, SimpleGameStats):
    """
    A class to represent a game statistic

    Used for the following stat types:
    season, career, careerRegularSeason, careerPlayoffs, statsSingleSeason

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
    type_ = [ 'season', 'statsSingleSeason' ]


@dataclass(kw_only=True)
class CareerGame(Splits, SimpleGameStats):
    """
    A class to represent a game statistic


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
    type_ = [ 'career' ]

@dataclass(kw_only=True)
class CareerRegularSeasonGame(Splits, SimpleGameStats):
    """
    A class to represent a game statistic


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
    type_ = [ 'careerRegularSeason' ]

@dataclass(kw_only=True)
class CareerPlayoffsGame(Splits, SimpleGameStats):
    """
    A class to represent a game statistic

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
    type_ = [ 'careerPlayoffs' ]