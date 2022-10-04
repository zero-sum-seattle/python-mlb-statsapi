from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.team import Team
from mlbstatsapi.models.person import Person

@dataclass
class PlaysPlayByInningHitsByTeamHitCoordinates:
    x: float
    y: float

@dataclass
class PlaysPlayByInningHitsByTeam:
    team:           Union[Team, Dict[str, Any]]
    inning:         int
    pitcher:        Union[Person, Dict[str, Any]]
    batter:         Union[Person, Dict[str, Any]]
    coordinates:    Union[PlaysPlayByInningHitsByTeamHitCoordinates, Dict[str, Any]]
    type:           str
    description:    str

    def __post_init__(self):
        self.team = Team(**team)
        self.pitcher = Person(**pitcher)
        self.batter = Person(**batter)
        self.coordinates = PlaysPlayByInningHitsByTeamHitCoordinates(**coordinates)
