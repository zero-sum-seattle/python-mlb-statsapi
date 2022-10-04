from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.people import Person

from mlbstatsapi.models.game.livedata.plays.play.playrunner.runnercredits import RunnerCredits

@dataclass
class RunnerMovement:
    """
    A class to represent a play runner.

    Attributes
    ----------
    isOut : bool
        Was the running movement an out
    outNumber : int
        What is the outnumber
    originBase : str = None
        Original base
    start : str = None
        What base the runner started from
    end : str = None
        What base the runner ended at
    outBase : str = None
        Base runner was made out
    """
    isOut:      bool
    outNumber:  int
    originBase: str = None
    start:      str = None
    end:        str = None
    outBase:    str = None

@dataclass
class RunnerDetails:
    """
    A class to represent a play runner.

    Attributes
    ----------
    event : str
        Runner event
    eventType : str
        Runner event type
    runner : Person
        Who the runner is
    isScoringEvent :  bool
        Was this a scoring events
    rbi : bool
        Was this a rbi
    earned : bool
        Was it earned
    teamUnearned : bool
        Was it unearned
    playIndex : int
        Play index
    movementReason : str = None
        Reason for the movement
    responsiblePitcher : Person = None
        WHo was the responsible pitcher
    """
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
    """
    A class to represent a play runner.

    Attributes
    ----------
    movement : RunnerMovement
        Runner movements
    details : RunnerDetails
        Runner details
    credits : List[RunnerCredits]
        Runner credits
    """
    movement:   Union[RunnerMovement, Dict[str, Any]]
    details:    Union[RunnerDetails, Dict[str, Any]]
    credits:    Union[List[RunnerCredits], List[Dict[str, Any]]]

    def __post_init__(self):
        self.movement = RunnerMovement(**self.movement)
        self.details = RunnerDetails(**self.details)
        self.credits = [RunnerCredits(**credit) for credit in self.credits]
