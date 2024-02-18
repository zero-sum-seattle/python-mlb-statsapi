from typing import Union, List
from pydantic import BaseModel
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person

class HitCoordinates(BaseModel):
    """Represents the coordinates of a hit.

    Attributes:
        x (float): X coordinate for the hit.
        y (float): Y coordinate for the hit.
    """
    x: float
    y: float

class HitsByTeam(BaseModel):
    """Represents a hit during an inning.

    Attributes:
        team (Team): The team making the hit.
        inning (int): The inning number in which the hit occurred.
        pitcher (Person): The pitcher during the hit.
        batter (Person): The batter making the hit.
        coordinates (HitCoordinates): The coordinates where the hit landed.
        type (str): The type of hit.
        description (str): A description of the hit.
    """
    team: Team
    inning: int
    pitcher: Person
    batter: Person
    coordinates: HitCoordinates
    type: str
    description: str


class PlayByInningHits(BaseModel):
    """Represents the hits made by inning in a game.

    Attributes:
        home (List[HitsByTeam]): A list of hits by the home team.
        away (List[HitsByTeam]): A list of hits by the away team.
    """
    home: List[HitsByTeam]
    away: List[HitsByTeam]


