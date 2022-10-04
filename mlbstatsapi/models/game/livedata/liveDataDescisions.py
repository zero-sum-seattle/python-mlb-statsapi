from typing import Union, Dict, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.venue import Venue
from mlbstatsapi.models.person import Person

@dataclass
class LiveDataDecisions:
    winner: Union[Person, Dict[str, Any]]
    loser:  Union[Person, Dict[str, Any]]

    def __post_init__(self):
        self.winner = Person(**winner)
        self.loser = Person(**loser)
