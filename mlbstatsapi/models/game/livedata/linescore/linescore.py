from typing import List, Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import (
    LinescoreInning,
    LinescoreTeams,
    LinescoreDefense,
    LinescoreOffense,
)


class Linescore(MLBBaseModel):
    """
    A class to represent a game's linescore.

    Attributes
    ----------
    current_inning : int
        The game's current inning.
    current_inning_ordinal : str
        This inning's ordinal.
    inning_state : str
        What state this inning is in.
    inning_half : str
        Which half of the inning we are in.
    is_top_inning : bool
        Is this the top of the inning.
    scheduled_innings : int
        How many innings are scheduled for this game.
    innings : List[LinescoreInning]
        Data on each inning.
    teams : LinescoreTeams
        Line score data on our teams.
    defense : LinescoreDefense
        Current defense.
    offense : LinescoreOffense
        Current offense.
    balls : int
        Current count balls.
    strikes : int
        Current count strikes.
    outs : int
        Current count outs.
    note : str
        Any note for the linescore.
    """
    scheduled_innings: int = Field(alias="scheduledInnings")
    innings: List[LinescoreInning] = []
    teams: LinescoreTeams
    defense: LinescoreDefense
    offense: LinescoreOffense
    balls: Optional[int] = None
    strikes: Optional[int] = None
    outs: Optional[int] = None
    note: Optional[str] = None
    current_inning: Optional[int] = Field(default=None, alias="currentInning")
    current_inning_ordinal: Optional[str] = Field(default=None, alias="currentInningOrdinal")
    inning_state: Optional[str] = Field(default=None, alias="inningState")
    inning_half: Optional[str] = Field(default=None, alias="inningHalf")
    is_top_inning: Optional[bool] = Field(default=None, alias="isTopInning")
