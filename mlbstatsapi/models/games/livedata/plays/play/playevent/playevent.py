from typing import Union, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.person import Person

from mlbstatsapi.models.game.livedata.plays.play.playevent.playeventdetails import PlayEventDetails

@dataclass
class PlayCount:
    balls:      int
    strikes:    int
    outs:       int

@dataclass
class PlayPlayEvents:
    details:    Union[PlayEventDetails, Dict[str, Any]]
    count:      Union[PlayCount, Dict[str, Any]] = None
    index:      int
    startTime:  str
    endTime:    str
    isPitch:    bool
    type:       str
    player:     Union[Person, Dict[str, Any]] = None

    def __post_init__(self):
        self.details = PlayEventDetails(**details)
        self.count = PlayCount(**count) if count else count
        self.index = index
        self.startTime = startTime
        self.endTime = endTime
        self.isPitch = isPitch
        self.type = type
        self.player = Person(**player) if player else player
