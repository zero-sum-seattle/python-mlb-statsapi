from typing import Union, Dict, List, Any
from dataclasses import dataclass

from play_models.playResult import PlayResult
from play_models.playAbout import PlayAbout
from play_models.playEvent_models.playCount import PlayCount
from play_models.playMatchup import PlayMatchup
from play_models.playRunners import PlayRunners
from play_models.playPlayEvents import PlayPlayEvents

@dataclass
class PlaysPlay:
    result:         Union[PlayResult, Dict[str, Any]]
    about:          Union[PlayAbout, Dict[str, Any]]
    count:          Union[PlayCount, Dict[str, Any]]
    matchup:        Union[PlayMatchup, Dict[str, Any]]
    pitchIndex:     List[int]
    actionIndex:    List[int]
    runnerIndex:    List[int]
    runners:        Union[List[PlayRunners], List[Dict[str, Any]]]
    playEvents:     Union[List[PlayPlayEvents], List[Dict[str, Any]]]
    playEndTime:    str
    atBatIndex:     int

    def __post_init__(self):
        self.result = PlayResult(**result)
        self.about = PlayAbout(**about)
        self.count = PlayCount(**count)
        self.matchup = PlayMatchup(**matchup)
        self.runners = [PlayRunners(**runner) for runner in runners]
        self.playEvents = [PlayPlayEvents(**playEvent) for playEvent in playEvents]
