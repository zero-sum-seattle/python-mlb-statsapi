from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.person import Person

@dataclass
class RunnersCreditsPosition:
    code:           str
    name:           str
    type:           str
    abbreviation:   str

@dataclass
class RunnersCredits:
    player:     Union[Person, Dict[str, Any]]
    position:   Union[RunnersCreditsPosition, Dict[str, Any]]
    credit:     str

    def __post_init__(self):
        self.player = Person(**player)
        self.position = RunnersCreditsPosition(**position)
