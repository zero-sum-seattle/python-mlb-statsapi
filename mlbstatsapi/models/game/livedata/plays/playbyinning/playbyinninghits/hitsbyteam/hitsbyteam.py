from typing import Union, Dict, Any
from dataclasses import dataclass

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person

@dataclass
class HitsByTeamHitCoordinates:
    x: float
    y: float

@dataclass
class HitsByTeam:
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
