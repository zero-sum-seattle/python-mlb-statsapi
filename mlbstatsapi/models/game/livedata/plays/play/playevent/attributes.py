from typing import Union
from dataclasses import dataclass

@dataclass
class HitCoordinate:
    """
    A class to represent a play events hit location coordinates.

    Attributes
    ----------
    coordX : int
        X coordinate for hit
    coordY : int
        Y coordinate for hit
    """
    coordX: int
    coordY: int

    @property
    def x(self):
        return self.coordX

    @property
    def y(self):
        return self.coordY

@dataclass
class HitData:
    """
    A class to represent a play events hit data.

    Attributes
    ----------
    launchSpeed : float
        Hit launch speed
    launchAngle : int
        Hit launch angle
    totalDistance : int
        Hits total distance
    trajectory : str
        Hit trajectory
    hardness : str
        Hit hardness
    location : str
        Hit location
    coordinates : HitCoordinate
        Hit coordinates
    """
    launchSpeed: float
    launchAngle: int
    totalDistance: int
    trajectory: str
    hardness: str
    location: str
    coordinates: HitCoordinate

    def __post_init__(self):
        self.coordinates = HitCoordinate(**self.coordinates)

@dataclass
class PlayEventCallType:
    """
    A class to represent a play event details call type.

    Attributes
    ----------
    code : str
        Call type code
    description : str
        Call type description
    """
    code: str
    description: str

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
    description: str
    hasReview: bool
    call: Union[PlayEventCallType, dict] = None
    event: str = None
    eventType: str = None
    code: str = None
    ballColor: str = None
    trailColor: str = None
    awayScore: int = None
    homeScore: int = None
    isInPlay: bool = None
    isStrike: bool = None
    isBall: bool = None
    isScoringPlay: bool = None
    type: Union[PlayEventCallType, dict] = None
    fromCatcher: bool = None
    runnerGoing: bool = None

    def __post_init__(self):
        self.call = PlayEventCallType(**self.call) if self.call else self.call
        self.type = PlayEventCallType(**self.type) if self.type else self.type

@dataclass
class PlayCount:
    """
    A class to represent a play count.

    Attributes
    ----------
    balls : int
        Balls
    strikes : int
        strikes
    outs : int
        Outs
    """
    balls: int
    strikes: int
    outs: int
