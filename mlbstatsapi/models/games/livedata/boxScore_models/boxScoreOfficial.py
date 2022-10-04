from typing import Union, Dict, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.person import Person

@dataclass
class BoxScoreOffical:
    official:       Union[Person, Dict[str, Any]]
    officialType:   str

    def __post_init__(self):
        self.official = Person(**official)
