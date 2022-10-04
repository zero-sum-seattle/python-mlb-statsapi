from typing import Union, Dict, List, Any
from dataclasses import dataclass

from inningHits_models.playByInningHitsByTeam import PlayByInningHitsByTeam

@dataclass
class PlaysPlayByInningHits():
    home: Union[List[PlayByInningHitsByTeam], List[Dict[str, Any]]]
    away: Union[List[PlayByInningHitsByTeam], List[Dict[str, Any]]]

    def __post_init__(self):
        self.home = [PlayByInningHitsByTeam(**home_hit) for home_hit in home]
        self.away = [PlayByInningHitsByTeam(**away_hit) for away_hit in away]
