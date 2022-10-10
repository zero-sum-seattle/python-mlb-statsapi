from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays.playbyinning.playbyinninghits.hitsbyteam import HitsByTeam

@dataclass
class PlayByInningHits():
    """
    A class to represent a play by inning in this game.

    Attributes
    ----------
    home : List[HitsByTeam]
        Home team hits
    away : List[HitsByTeam]
        Away team hits
    """
    home: Union[List[HitsByTeam], List[Dict[str, Any]]]
    away: Union[List[HitsByTeam], List[Dict[str, Any]]]

    def __post_init__(self):
        self.home = [HitsByTeam(**home_hit) for home_hit in self.home]
        self.away = [HitsByTeam(**away_hit) for away_hit in self.away]
