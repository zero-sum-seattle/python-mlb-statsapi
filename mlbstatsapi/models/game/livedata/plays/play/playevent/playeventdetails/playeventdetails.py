from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class PlayEventDetailsCallType:
    code:           str
    description:    str

@dataclass
class PlayEventDetails:
    description:    str
    hasReview:      bool
    call:           Union[PlayEventDetailsCallType, Dict[str, Any]] = None
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
    fromCatcher:    bool = None
    runnerGoing:    bool = None

    def __post_init__(self):
        self.call = PlayEventDetailsCallType(**self.call) if self.call else self.call
        self.type = PlayEventDetailsCallType(**self.type) if self.type else self.type
