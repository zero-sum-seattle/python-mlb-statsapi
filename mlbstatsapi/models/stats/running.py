from dataclasses import dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.people import Batter, Pitcher

from .stats import Splits

@dataclass(kw_only=True)
class RunningOpponentsFaced(Splits):
    """
    A class to represent a running opponentsFaced statistic

    Attributes
    ----------
    """
    _stat = [ 'opponentsFaced' ]
    batter: Union[Batter, dict]
    group: str 
    pitcher: Union[Pitcher, dict]

    def __post_init__(self):
        self.batter = Batter(**self.batter) if self.batter else self.batter
        self.pitcher = Pitcher(**self.pitcher) if self.batter else self.batter