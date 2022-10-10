from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class PlayEventDetailsCallType:
    """
    A class to represent a play event details call type.

    Attributes
    ----------
    code : str
        Call type code
    description : str
        Call type description
    """
    code:           str
    description:    str

@dataclass
class PlayEventDetails:
    """
    A class to represent a plays events details.

    Attributes
    ----------
    description : str
        Play event descripton
    hasReview : bool
        Play event has review
    call : PlayEventDetailsCallType
        Play event call
    event : str = None
        Play event
    eventType : str = None
        Play event type
    code : str = None
        Play event Code
    ballColor : str = None
        ballColor
    trailColor : str = None
        trailColor
    awayScore : int = None
        awayScore
    homeScore : int = None
        homeScore
    isInPlay : bool = None
        If it is in play
    isStrike : bool = None
        If it is a strike
    isBall : bool = None
        If it is a ball
    isScoringPlay : bool = None
        If it is a scoring play
    type : PlayEventDetailsCallType
        Play type
    fromCatcher : bool = None
        If from the catcher
    runnerGoing : bool = None
        If a runner is going
    """
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
