from typing import List
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import GamePaceData


class GamePace(MLBBaseModel):
    """
    A class representing game pace data.

    Attributes
    ----------
    teams : List[GamePaceData]
        A list of game pace data by team.
    leagues : List[GamePaceData]
        A list of game pace data by league.
    sports : List[GamePaceData]
        A list of game pace data by sport.
    """
    teams: List[GamePaceData] = []
    leagues: List[GamePaceData] = []
    sports: List[GamePaceData] = []
