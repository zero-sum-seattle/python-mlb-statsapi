from typing import Union, Optional
from dataclasses import dataclass

from mlbstatsapi.models.people import Person

@dataclass
class RunnerCreditsPosition:
    """
    A class to represent a runners credit position.

    Attributes
    ----------
    code : str
        code
    name : str
        name
    type : str
        type
    abbreviation : str
        abbreviation
    """
    code: str
    name: str
    type: str
    abbreviation: str

@dataclass
class RunnerCredits:
    """
    A class to represent a runners credit.

    Attributes
    ----------
    player : Person
        The player
    position : RunnerCreditsPosition
        The position
    credit : str
        The credit
    """
    player: Union[Person, dict]
    position: Union[RunnerCreditsPosition, dict]
    credit: str

    def __post_init__(self):
        self.player = Person(**self.player)
        self.position = RunnerCreditsPosition(**self.position)

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
    isOut: bool
    outNumber: int
    originBase: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    outBase: Optional[str] = None

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
    event: str
    eventType: str
    runner: Union[Person, dict]
    isScoringEvent: bool
    rbi: bool
    earned: bool
    teamUnearned: bool
    playIndex: int
    movementReason: Optional[str] = None
    responsiblePitcher: Optional[Union[Person, dict]] = None

    def __post_init__(self):
        self.runner = Person(**self.runner)
        self.responsiblePitcher = Person(**self.responsiblePitcher) if self.responsiblePitcher else self.responsiblePitcher