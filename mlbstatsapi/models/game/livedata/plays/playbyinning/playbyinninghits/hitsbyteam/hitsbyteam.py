from typing import Union, Dict, Any
from dataclasses import dataclass

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person

@dataclass
class HitsByTeamHitCoordinates:
    """
    A class to represent a Hits coordinates.

    Attributes
    ----------
    x : float
        X coordinate for hit
    y : float
        Y coordinate for hit
    """
    x: float
    y: float

@dataclass
class HitsByTeam:
    """
    A class to represent a Hit during an inning.

    Attributes
    ----------
    team : Team
        This team
    inning : int
        This inning number
    pitcher : Person
        The pitcher
    batter : Person
        The batter
    coordinates : HitsByTeamHitCoordinates
        Hit coordinates
    type : str
        Type
    description : str
        description
    """
    team:           Union[Team, Dict[str, Any]]
    inning:         int
    pitcher:        Union[Person, Dict[str, Any]]
    batter:         Union[Person, Dict[str, Any]]
    coordinates:    Union[HitsByTeamHitCoordinates, Dict[str, Any]]
    type:           str
    description:    str

    def __post_init__(self):
        self.team = Team(**self.team)
        self.pitcher = Person(**self.pitcher)
        self.batter = Person(**self.batter)
        self.coordinates = HitsByTeamHitCoordinates(**self.coordinates)
