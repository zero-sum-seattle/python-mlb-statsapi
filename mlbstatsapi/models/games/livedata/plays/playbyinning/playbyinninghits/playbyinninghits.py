from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays.playbyinning.playbyinninghits.hitsbyteam import HitsByTeam

@dataclass
class PlayByInningHits():
    home: Union[List[HitsByTeam], List[Dict[str, Any]]]
    away: Union[List[HitsByTeam], List[Dict[str, Any]]]

    def __post_init__(self):
        self.home = [HitsByTeam(**home_hit) for home_hit in home]
        self.away = [HitsByTeam(**away_hit) for away_hit in away]
