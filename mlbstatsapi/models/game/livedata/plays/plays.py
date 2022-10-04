from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays.play import Play
from mlbstatsapi.models.game.livedata.plays.playbyinning import PlayByInning

@dataclass
class Plays:
    allPlays:       Union[List[Play], List[Dict[str, Any]]]
    currentPlay:    Union[Play, Dict[str, Any]]
    scoringPlays:   List[int]
    playsByInning:  Union[List[PlayByInning], List[Dict[str, Any]]]

    def __post_init__(self):
        self.allPlays = [Play(**play) for play in self.allPlays if play]
        self.currentPlay = Play(**self.currentPlay)
        self.playsByInning = [PlayByInning(**inning) for inning in self.playsByInning if inning]
