from dataclasses import dataclass, field
from typing import Optional, Union

from .stats import Stats

class SimpleGame(Stats):
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
    type_ = [ 'season', 'career', 'careerRegularSeason', 'careerPlayoffs', 'statsSingleSeason' ]
    firstdateplayed: str
    gamesplayed: int
    gamesstarted: int
    lastdateplayed: str 