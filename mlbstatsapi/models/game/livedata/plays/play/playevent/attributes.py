from typing import Union
from dataclasses import dataclass

@dataclass
class HitCoordinate:
    """
    A class to represent a play events hit location coordinates.

    Attributes
    ----------
    coordx : int
        X coordinate for hit
    coordy : int
        Y coordinate for hit
    """
    coordx: int
    coordy: int

    @property
    def x(self):
        return self.coordx

    @property
    def y(self):
        return self.coordy

@dataclass
class HitData:
    """
    A class to represent a play events hit data.

    Attributes
    ----------
    launchspeed : float
        Hit launch speed
    launchangle : int
        Hit launch angle
    totaldistance : int
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
    launchspeed: float
    launchangle: int
    totaldistance: int
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
    hasreview : bool
        Play event has review
    call : PlayEventDetailsCallType
        Play event call
    event : str = None
        Play event
    eventtype : str = None
        Play event type
    code : str = None
        Play event Code
    ballcolor : str = None
        ballColor
    trailcolor : str = None
        trailColor
    awayscore : int = None
        awayScore
    homescore : int = None
        homeScore
    isinplay : bool = None
        If it is in play
    isstrike : bool = None
        If it is a strike
    isball : bool = None
        If it is a ball
    isscoringplay : bool = None
        If it is a scoring play
    type : PlayEventDetailsCallType
        Play type
    fromcatcher : bool = None
        If from the catcher
    runnergoing : bool = None
        If a runner is going
    """
    description: str
    hasreview: bool
    call: Union[PlayEventCallType, dict] = None
    event: str = None
    eventtype: str = None
    code: str = None
    ballcolor: str = None
    trailcolor: str = None
    awayscore: int = None
    homescore: int = None
    isinplay: bool = None
    isstrike: bool = None
    isball: bool = None
    isscoringplay: bool = None
    type: Union[PlayEventCallType, dict] = None
    fromcatcher: bool = None
    runnergoing: bool = None

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
