from typing import Union, Dict, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.person import Person

@dataclass
class PlaysPlayRunnersDetails:
    event:              str
    eventType:          str
    movementReason:     str = None
    runner:             Union[Person, Dict[str, Any]]
    responsiblePitcher: Union[Person, Dict[str, Any]] = None
    isScoringEvent:     bool
    rbi:                bool
    earned:             bool
    teamUnearned:       bool
    playIndex:          int

    def __post_init__(self):
        self.runner = Person(**runner)
        self.responsiblePitcher = Person(**responsiblePitcher) if responsiblePitcher else responsiblePitcher
