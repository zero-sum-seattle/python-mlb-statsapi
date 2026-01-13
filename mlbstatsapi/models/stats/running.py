from typing import List, ClassVar
from mlbstatsapi.models.people import Batter, Pitcher
from .stats import Stat


class RunningOpponentsFaced(Stat):
    """
    A class to represent a running opponentsFaced statistic.

    Attributes
    ----------
    batter : Batter
        The batter of the stat.
    group : str
        The stat group of the stat.
    pitcher : Pitcher
        The pitcher of the stat.
    """
    _stat: ClassVar[List[str]] = ['opponentsFaced']
    batter: Batter
    group: str
    pitcher: Pitcher
