from typing import Union, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.person import Person

from playEvents_models.playEventsDetails import PlayEventsDetails
from playEvents_models.playCount import PlayCount

@dataclass
class PlaysPlayPlayEvents:
    details:    Union[PlayEventsDetails, Dict[str, Any]]
    count:      Union[PlayCount, Dict[str, Any]] = None
    index:      int
    startTime:  str
    endTime:    str
    isPitch:    bool
    type:       str
    player:     Union[Person, Dict[str, Any]] = None

    def __post_init__(self):
        self.details = PlayPlayEventsDetails(**details)
        self.count = PlayCount(**count) if count else count
        self.index = index
        self.startTime = startTime
        self.endTime = endTime
        self.isPitch = isPitch
        self.type = type
        self.player = Person(**player) if player else player
