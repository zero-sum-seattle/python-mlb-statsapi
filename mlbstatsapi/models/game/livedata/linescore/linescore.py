from typing import Union, List, Optional
from pydantic import BaseModel

from .attributes import LinescoreInning
from .attributes import LinescoreTeams
from .attributes import LinescoreDefense
from .attributes import LinescoreOffense


class Linescore(BaseModel):
    """Represents a game's Line score.

    Attributes:
        currentinning (int): The game's current inning.
        currentinningordinal (str): The ordinal of the current inning.
        inningstate (str): The state of the current inning.
        inninghalf (str): Indicates which half of the inning is in play.
        istopinning (bool): Specifies if it's the top of the inning.
        scheduledinnings (int): The number of innings scheduled for the game.
        innings (List[LinescoreInning]): Data on each inning.
        teams (LinescoreTeams): Line score data for the teams.
        defense (LinescoreDefense): Information on the current defense.
        offense (LinescoreOffense): Information on the current offense.
        balls (int): The current count of balls.
        strikes (int): The current count of strikes.
        outs (int): The current count of outs.
    """

    scheduledInnings: int
    innings: List[LinescoreInning]
    teams: LinescoreTeams
    defense: LinescoreDefense
    offense: LinescoreOffense
    balls: Optional[int] = None
    strikes: Optional[int] = None
    outs: Optional[int] = None
    note: Optional[str] = None
    currentInning: Optional[int] = None
    currentInningOrdinal: Optional[str] = None
    inningState: Optional[str] = None
    inningHalf: Optional[str] = None
    isTopInning: Optional[bool] = None
