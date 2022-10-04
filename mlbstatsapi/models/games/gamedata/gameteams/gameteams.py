from typing import Union, Dict, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.gamedata.gameteams.gameteam import GameTeam

@dataclass
class gameTeams:
    away: Union[GameTeam, Dict[str, Any]]
    home: Union[GameTeam, Dict[str, Any]]

    def __post_init__(self):
        self.away = GameTeam(**away)
        self.home = GameTeam(**home)
