from typing import Optional, List
from pydantic import BaseModel

from .attributes import GamePaceData

class GamePace(BaseModel):
    """Represents game pace data, aggregating information across teams, leagues, and sports.

    Attributes:
        teams (List[GamePaceData], optional): A list of game pace data for various teams. Optional.
        leagues (List[GamePaceData], optional): A list of game pace data for various leagues. Optional.
        sports (List[GamePaceData], optional): A list of game pace data for various sports. Optional.
    """
    
    teams: Optional[List[GamePaceData]] = None
    leagues: Optional[List[GamePaceData]] = None
    sports: Optional[List[GamePaceData]] = None 