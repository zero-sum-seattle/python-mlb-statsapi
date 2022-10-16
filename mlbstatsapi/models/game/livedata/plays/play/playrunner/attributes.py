from typing import Union, Optional
from dataclasses import dataclass

from mlbstatsapi.models.people import Person, Position

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
    position: Union[Position, dict]
    credit: str

    def __post_init__(self):
        self.player = Person(**self.player)
        self.position = Position(**self.position)

@dataclass
class RunnerMovement:
    """
    A class to represent a play runner.

    Attributes
    ----------
    isout : bool
        Was the running movement an out
    outnumber : int
        What is the outnumber
    originbase : str = None
        Original base
    start : str = None
        What base the runner started from
    end : str = None
        What base the runner ended at
    outbase : str = None
        Base runner was made out
    """
    isout: bool
    outnumber: int
    originbase: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    outbase: Optional[str] = None

@dataclass
class RunnerDetails:
    """
    A class to represent a play runner.

    Attributes
    ----------
    event : str
        Runner event
    eventtype : str
        Runner event type
    runner : Person
        Who the runner is
    isscoringevent :  bool
        Was this a scoring events
    rbi : bool
        Was this a rbi
    earned : bool
        Was it earned
    teamunearned : bool
        Was it unearned
    playindex : int
        Play index
    movementreason : str = None
        Reason for the movement
    responsiblepitcher : Person = None
        WHo was the responsible pitcher
    """
    event: str
    eventtype: str
    runner: Union[Person, dict]
    isscoringevent: bool
    rbi: bool
    earned: bool
    teamunearned: bool
    playindex: int
    movementreason: Optional[str] = None
    responsiblepitcher: Optional[Union[Person, dict]] = None

    def __post_init__(self):
        self.runner = Person(**self.runner)
        self.responsiblepitcher = Person(**self.responsiblepitcher) if self.responsiblepitcher else self.responsiblepitcher