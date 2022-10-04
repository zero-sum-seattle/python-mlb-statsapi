from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class PlayEventDetailsCallType:
    code:           str
    description:    str

@dataclass
class PlayEventDetails:
    call:           Union[PlayEventDetailsCallType, Dict[str, Any]] = None
    description:    str
    event:          str = None
    eventType:      str = None
    code:           str = None
    ballColor:      str = None
    trailColor:     str = None
    awayScore:      int = None
    homeScore:      int = None
    isInPlay:       bool = None
    isStrike:       bool = None
    isBall:         bool = None
    isScoringPlay:  bool = None
    type:           Union[PlayEventDetailsCallType, Dict[str, Any]] = None
    hasReview:      bool
    fromCatcher:    bool = None
    runnerGoing:    bool = None

    def __post_init__(self):
        self.call = PlayEventDetailsCallType(**call) if call else call
        self.type = PlayEventDetailsCallType(**type) if type else type
