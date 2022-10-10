from typing import Union, Dict, List, Any
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
    code:           str
    name:           str
    type:           str
    abbreviation:   str

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
    player:     Union[Person, Dict[str, Any]]
    position:   Union[RunnerCreditsPosition, Dict[str, Any]]
    credit:     str

    def __post_init__(self):
        self.player = Person(**self.player)
        self.position = RunnerCreditsPosition(**self.position)
