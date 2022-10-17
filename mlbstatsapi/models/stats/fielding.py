from dataclasses import dataclass, field
from typing import Optional, Union

from .stats import Stats

@dataclass
class SimpleFielding(Stats):
    """
    A class to represent a simple fielding statistics

    Used for the following stat types:
    season, seasonAdvanced, statsSingleSeason, homeAndAway, byDayOfWeek, byDateRange, lastXGames, gameLog
    """
    type_ = [ 'season', 'seasonAdvanced', 'statsSingleSeason', 'homeAndAway', 'byDayOfWeek', 'byDateRange',
    'lastXGames', 'gameLog' ]
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