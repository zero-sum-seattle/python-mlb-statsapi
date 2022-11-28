from typing import Union, Optional
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
    
    trajectory: str
    hardness: str
    location: str
    coordinates: HitCoordinate
    launchspeed: Optional[float] = None
    launchangle: Optional[int] = None
    totaldistance: Optional[int] = None

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
    event : str
        Play event
    eventtype : str
        Play event type
    code : str
        Play event Code
    ballcolor : str
        ballColor
    trailcolor : str
        trailColor
    awayscore : int
        awayScore
    homescore : int
        homeScore
    isinplay : bool
        If it is in play
    isstrike : bool
        If it is a strike
    isball : bool
        If it is a ball
    isout : bool
        If its is an out
    isscoringplay : bool
        If it is a scoring play
    type : PlayEventDetailsCallType
        Play type
    fromcatcher : bool
        If from the catcher
    runnergoing : bool 
        If a runner is going
    """
    description: str
    hasreview: bool
    call: Optional[Union[PlayEventCallType, dict]] = None
    event: Optional[str] = None
    eventtype: Optional[str] = None
    code: Optional[str] = None
    ballcolor: Optional[str] = None
    trailcolor: Optional[str] = None
    awayscore: Optional[int] = None
    homescore: Optional[int] = None
    isinplay: Optional[bool] = None
    isstrike: Optional[bool] = None
    isball: Optional[bool] = None
    isout: Optional[bool] = None
    isscoringplay: Optional[bool] = None
    type: Optional[Union[PlayEventCallType, dict]] = None
    fromcatcher: Optional[bool] = None
    runnergoing: Optional[bool] = None

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
