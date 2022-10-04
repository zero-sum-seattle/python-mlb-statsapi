from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays.playbyinning.playbyinninghits import PlayByInningHits

@dataclass
class PlayByInning():
    startIndex: int
    endIndex:   int
    top:        List[int]
    bottom:     List[int]
    hits:       Union[PlayByInningHits, Dict[str, Any]]

    def __post_init__(self):
        self.hits = PlayByInningHits(**self.hits)
