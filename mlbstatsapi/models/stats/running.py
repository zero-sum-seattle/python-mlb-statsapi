from dataclasses import dataclass, field
from typing import Optional, Union, List

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.game import Game

from .stats import Splits, CodeDesc, Count

@dataclass(kw_only=True)
class RunningOpponentsFaced(Splits):
    """
    A class to represent a running opponentsFaced statistic

    Attributes
    ----------
    """
    _stat = [ 'opponentsFaced' ]
    batter: Union[Person, dict]
    group: str 
    pitcher: Union[Person, dict]