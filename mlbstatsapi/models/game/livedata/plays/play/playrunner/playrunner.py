from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.people import Person

from mlbstatsapi.models.game.livedata.plays.play.playrunner.runnercredits import RunnerCredits

@dataclass
class RunnerMovement:
    isOut:      bool
    outNumber:  int
    originBase: str = None
    start:      str = None
    end:        str = None
    outBase:    str = None

@dataclass
class RunnerDetails:
    event:              str
    eventType:          str
    runner:             Union[Person, Dict[str, Any]]
    isScoringEvent:     bool
    rbi:                bool
    earned:             bool
    teamUnearned:       bool
    playIndex:          int
    movementReason:     str = None
    responsiblePitcher: Union[Person, Dict[str, Any]] = None

    def __post_init__(self):
        self.runner = Person(**self.runner)
        self.responsiblePitcher = Person(**self.responsiblePitcher) if self.responsiblePitcher else self.responsiblePitcher

@dataclass
class PlayRunner:
    movement:   Union[RunnerMovement, Dict[str, Any]]
    details:    Union[RunnerDetails, Dict[str, Any]]
    credits:    Union[List[RunnerCredits], List[Dict[str, Any]]]

    def __post_init__(self):
        self.movement = RunnerMovement(**self.movement)
        self.details = RunnerDetails(**self.details)
        self.credits = [RunnerCredits(**credit) for credit in self.credits]
