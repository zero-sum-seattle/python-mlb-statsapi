from typing import Union, Dict, Any
from dataclasses import dataclass

from gameData_modules.plays import Plays
from gameData_modules.linescore import Linescore
from gameData_modules.boxScore import BoxScore
from gameData_modules.liveDataDecisions import LiveDataDecisions
from gameData_modules.liveDataLeaders import LiveDataLeaders

class LiveData:
    plays:      Union[Plays, Dict[str, Any]]
    linescore:  Union[Linescore, Dict[str, Any]]
    boxscore:   Union[BoxScore, Dict[str, Any]]
    decisions:  Union[LiveDataDecisions, Dict[str, Any]] = None
    leaders:    Union[LiveDataLeaders, Dict[str, Any]]

    def __post_init__(self):
        self.plays = Plays(**plays)
        self.linescore = Linescore(**linescore)
        self.boxscore = BoxScore(**boxscore)
        self.decisions = LiveDataDecisions(**decisions) if decisions else decisions
        self.leaders = LiveDataLeaders(**leaders)
