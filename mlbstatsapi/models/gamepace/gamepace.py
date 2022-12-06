from dataclasses import dataclass
from typing import Optional, List

from .attributes import Gamepacedata

@dataclass
class Gamepace:
    """
    A dataclass representing a gamepace.

    Attributes:
    ----------
    teams : List[Gamepaceteams]
        A list of teams in the gamepace.
    leagues : List[Gamepaceleagues]
        A list of leagues in the gamepace.
    sports : List[Gamepacesports]
        A list of sports in the gamepace.
    """
    teams: Optional[List[Gamepacedata]] = None
    leagues: Optional[List[Gamepacedata]] = None
    sports: Optional[List[Gamepacedata]] = None


    def __post_init__(self):
        self.teams = Gamepacedata(**self.teams) if self.teams else None        
        self.leagues = Gamepacedata(**self.leagues) if self.leagues else None    
        self.sports = Gamepacedata(**self.sports) if self.sports else None        