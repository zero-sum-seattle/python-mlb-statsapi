from typing import Union, Dict, List, Any
from dataclasses import dataclass

from byInning_models.playByInningHits import PlayByInningHits

@dataclass
class PlayByInning():
    startIndex: int
    endIndex:   int
    top:        List[int]
    bottom:     List[int]
    hits:       Union[PlaysPlayByInningHits, Dict[str, Any]]

    def __post_init__(self):
        self.hits = PlayByInningHits(**hits)
