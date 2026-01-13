from typing import List
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person


class HitCoordinates(MLBBaseModel):
    """
    A class to represent a hit's coordinates.

    Attributes
    ----------
    x : float
        X coordinate for hit.
    y : float
        Y coordinate for hit.
    """
    x: float
    y: float


class HitsByTeam(MLBBaseModel):
    """
    A class to represent a hit during an inning.

    Attributes
    ----------
    team : Team
        This team.
    inning : int
        This inning number.
    pitcher : Person
        The pitcher.
    batter : Person
        The batter.
    coordinates : HitCoordinates
        Hit coordinates.
    type : str
        Type.
    description : str
        Description.
    """
    team: Team
    inning: int
    pitcher: Person
    batter: Person
    coordinates: HitCoordinates
    type: str
    description: str


class PlayByInningHits(MLBBaseModel):
    """
    A class to represent a play by inning hits.

    Attributes
    ----------
    home : List[HitsByTeam]
        Home team hits.
    away : List[HitsByTeam]
        Away team hits.
    """
    home: List[HitsByTeam] = []
    away: List[HitsByTeam] = []
