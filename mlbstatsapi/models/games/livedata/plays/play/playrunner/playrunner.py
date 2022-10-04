from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays.play.playrunner.runnercredits import RunnerCredits

@dataclass
class RunnerMovement:
    originBase: str = None
    start:      str = None
    end:        str = None
    outBase:    str = None
    isOut:      bool
    outNumber:  int

@dataclass
class RunnerDetails:
    event:              str
    eventType:          str
    movementReason:     str = None
    runner:             Union[Person, Dict[str, Any]]
    responsiblePitcher: Union[Person, Dict[str, Any]] = None
    isScoringEvent:     bool
    rbi:                bool
    earned:             bool
    teamUnearned:       bool
    playIndex:          int

    def __post_init__(self):
        self.runner = Person(**runner)
        self.responsiblePitcher = Person(**responsiblePitcher) if responsiblePitcher else responsiblePitcher

@dataclass
class PlayRunner:
    movement:   Union[RunnerMovement, Dict[str, Any]]
    details:    Union[RunnerDetails, Dict[str, Any]]
    credits:    Union[List[RunnerCredits], List[Dict[str, Any]]]

    def __post_init__(self):
        self.movement = RunnerMovement(**movement)
        self.details = RunnerDetails(**details)
        self.credits = [RunnerCredits(**credit) for credit in credits]
