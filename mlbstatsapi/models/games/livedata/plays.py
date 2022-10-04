from typing import Union, Dict, List, Any
from dataclasses import dataclass

from plays_models.playByInning import PlayByInning
from plays_models.playsPlay import PlaysPlay

@dataclass
class Plays:
    allPlays:       Union[List[PlaysPlay], List[Dict[str, Any]]]
    currentPlay:    Union[PlaysPlay, Dict[str, Any]]
    scoringPlays:   List[int]
    playsByInning:  Union[List[PlayByInning], List[Dict[str, Any]]]

    def __post_init__(self):
        self.allPlays = [PlaysPlay(**play) for play in allPlays if play]
        self.currentPlay = PlaysPlay(**currentPlay)
        self.scoringPlays = scoringPlays
        self.playsByInning = [PlayByInning(**inning) for inning in playsByInning if inning]
