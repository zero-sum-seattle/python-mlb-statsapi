from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.person import Person

@dataclass
class RunnerCreditsPosition:
    code:           str
    name:           str
    type:           str
    abbreviation:   str

@dataclass
class RunnerCredits:
    player:     Union[Person, Dict[str, Any]]
    position:   Union[RunnerCreditsPosition, Dict[str, Any]]
    credit:     str

    def __post_init__(self):
        self.player = Person(**player)
        self.position = RunnerCreditsPosition(**position)
