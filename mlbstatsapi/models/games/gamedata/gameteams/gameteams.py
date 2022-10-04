from typing import Union, Dict, Any
from dataclasses import dataclass

from gameTeams_modules.gameTeamsTeam import GameTeamsTeam

@dataclass
class gameTeams:
    away: Union[GameTeamsTeam, Dict[str, Any]]
    home: Union[GameTeamsTeam, Dict[str, Any]]

    def __post_init__(self):
        self.away = GameTeamsTeam(**away)
        self.home = GameTeamsTeam(**home)
