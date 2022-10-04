from typing import Union, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.person import Person

@dataclass
class GameProbablePitchers:
    away: Union[Person, Dict[str, Any]]
    home: Union[Person, Dict[str, Any]]

    def __post_init__(self):
        self.away = Person(**away)
        self.home = Person(**home)
