from typing import Union, List
from dataclasses import dataclass

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person

@dataclass
class HitCoordinates:
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
    coordinates : HitCoordinates
        Hit coordinates
    type : str
        Type
    description : str
        description
    """
    team: Union[Team, dict]
    inning: int
    pitcher: Union[Person, dict]
    batter: Union[Person, dict]
    coordinates: Union[HitCoordinates, dict]
    type: str
    description: str

    def __post_init__(self):
        self.team = Team(**self.team)
        self.pitcher = Person(**self.pitcher)
        self.batter = Person(**self.batter)
        self.coordinates = HitCoordinates(**self.coordinates)

@dataclass
class PlayByInningHits:
    """
    A class to represent a play by inning in this game.

    Attributes
    ----------
    home : List[HitsByTeam]
        Home team hits
    away : List[HitsByTeam]
        Away team hits
    """
    home: Union[List[HitsByTeam], List[dict]]
    away: Union[List[HitsByTeam], List[dict]]

    def __post_init__(self):
        self.home = [HitsByTeam(**home_hit) for home_hit in self.home]
        self.away = [HitsByTeam(**away_hit) for away_hit in self.away]
