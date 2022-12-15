from dataclasses import dataclass
from typing import Optional, List

from .attributes import Gamepacedata

@dataclass
class Gamepace:
    """
    A dataclass representing a gamepace.

    Attributes:
    ----------
    teams : List[Gamepacedata]
        A list of teams in the gamepace.
    leagues : List[Gamepacedata]
        A list of leagues in the gamepace.
    sports : List[Gamepacedata]
        A list of sports in the gamepace.
    """
    teams: Optional[List[Gamepacedata]] = None
    leagues: Optional[List[Gamepacedata]] = None
    sports: Optional[List[Gamepacedata]] = None


    def __post_init__(self):
        self.teams = [Gamepacedata(**teams) for teams in self.teams]        
        self.leagues = [Gamepacedata(**leagues) for leagues in self.leagues]    
        self.sports = [Gamepacedata(**sports) for sports in self.sports]     