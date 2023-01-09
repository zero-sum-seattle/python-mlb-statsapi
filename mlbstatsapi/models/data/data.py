from dataclasses import dataclass, field, InitVar
from typing import List, Union, Dict, Any, Optional




@dataclass(repr=False)
class PitchBreak:
    """
    A class to hold pitch pitch break data
    
    Attributes
    ----------
    breakangle : float
        Degrees clockwise (batter's view) that the plane of 
        the pitch deviates from the vertical
    breaklength : float
        Max distance that the pitch separates from the straight
        line between pitch start and pitch end
    breaky : int
        Distance from home plate where the break is greatest
    spinrate : int
        Pitch spinRate
    spindirection : int
        Pitch spinDirection
    """
    breakangle: float
    breaklength: float
    breaky: float
    spinrate: Optional[float] = None
    spindirection: Optional[float] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class PitchCoordinates:
    """
    A class to hold pitch coordinates for playLog

    Attributes
    ----------
    ay : float, default=None
        Ball acceleration on the y axis
    az : float, default=None
        Ball acceleration on the z axis
    pfxx : float, default=None
        horizontal movement of the ball in inches
    pfxz : float, default=None
        Vertical movement of the ball in inches
    px : float, default=None
        Horizontal position in feet of the ball as it 
        crosses the front axis of home plate
    pz : float, default=None
        Vertical position in feet of the ball as it 
        crosses the front axis of home plate
    vx0 : float, default=None
        Velocity of the ball from the x-axis
    vy0 : float, default=None
        Velocity of the ball from the y axis, this
        is negative becuase 0,0,0 is behind the batter
        and the ball travels from pitcher mound towards 0,0,0
    vz0 : float, default=None
        Velocity of the ball from the z axis
    x0 : float, default=None
        Coordinate location of the ball at the point it was
        reeased from pitchers hand on the x axis (time=0)
    y0 : float, default=None
        Coordinate location of the ball at the point it was
        reeased from pitchers hand on the y axis (time=0)
    z0 : float, default=None
        Coordinate location of the ball at the point it was
        reeased from pitchers hand on the z axis (time=0)
    ax : float, default=None
        Ball acceleration on the x axis
    x : float, default=None
        X coordinate where pitch crossed front of home plate
    y : float, default=None
        Y coordinate where pitch crossed front of home plate
    """
    ay: Optional[float] = None
    az: Optional[float] = None
    pfxx: Optional[float] = None
    pfxz: Optional[float] = None
    px: Optional[float] = None
    pz: Optional[float] = None
    vx0: Optional[float] = None
    vy0: Optional[float] = None
    vz0: Optional[float] = None
    x0: Optional[float] = None
    y0: Optional[float] = None
    z0: Optional[float] = None
    ax: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class PitchData:
    """
    A class to hold data on a pitch
    
    Attributes
    ----------
    startspeed : float
        The starting speed of the pitch.
    endspeed : float
        The ending speed of the pitch.
    strikezonetop : float
        The top of the strike zone.
    strikezonebottom : float
        The bottom of the strike zone.
    coordinates : PitchCoordinates
        The coordinates of the pitch.
    breaks : PitchBreak
        The break data of the pitch.
    zone : float
        The zone in which the pitch was thrown.
    typeconfidence : float
        The confidence in the type of pitch thrown.
    platetime : float
        The amount of time the pitch was in the air.
    extension : float
        The extension of the pitch.
    strikezonewidth : float
        The width of the strikezone
    strikezonedepth : float
        The depth of the strikezone
    """
    strikezonetop: float
    strikezonebottom: float
    breaks: Union[PitchBreak, dict] 
    coordinates: Optional[Union[PitchCoordinates, dict]] = field(default_factory=dict) 
    extension: Optional[float] = None
    startspeed: Optional[float] = None
    endspeed: Optional[float] = None
    zone: Optional[float] = None
    typeconfidence: Optional[float] = None
    platetime: Optional[float] = None
    strikezonewidth: Optional[float] = None
    strikezonedepth: Optional[float] = None


    def __post_init__(self):
        self.coordinates = PitchCoordinates(**self.coordinates) if self.coordinates else self.coordinates
        self.breaks = PitchBreak(**self.breaks) if self.breaks else self.breaks

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass
class HitCoordinates:
    """
    A class to represent a play events hit location coordinates.

    Attributes
    ----------
    coordx : int
        X coordinate for hit
    coordy : int
        Y coordinate for hit
    """
    coordx: Optional[float] = None
    coordy: Optional[float] = None

    @property
    def x(self):
        return self.coordx

    @property
    def y(self):
        return self.coordy

@dataclass(repr=False)
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
    coordinates: Union[HitCoordinates, dict]
    location: Optional[int] = None
    launchspeed: Optional[float] = None
    launchangle: Optional[str] = None # this is a negative number and I'm brain farting on those
    totaldistance: Optional[float] = None

    def __post_init__(self):
        self.coordinates = HitCoordinates(**self.coordinates) if self.coordinates else self.coordinates

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass
class CodeDesc:
    """
    a class to hold a code and a description

    Attributes
    ----------
    code : str
        the code to reference the attribute using this
    description : str
        the description of the attribute using this
    """
    code: str
    description: Optional[str] = None


@dataclass(repr=False)
class Count:
    """
    a class to hold a pitch count and base runners

    Attributes
    ----------
    code : str
        code
    balls : int
        number of balls
    inning : int
        inning number
    istopinning : bool
        bool to hold status of top inning
    outs : int
        number of outs
    runneron1b : bool
        bool to hold 1b runner status
    runneron2b : bool
        bool to hold 2b runner status
    runneron3b : bool
        bool to hold 3b runner status
    strikes : int
        strike count
    """
    balls: int
    outs: int
    strikes: int
    inning: Optional[int] = None
    runneron1b: Optional[bool] = None
    runneron2b: Optional[bool] = None
    runneron3b: Optional[bool] = None
    istopinning: Optional[bool] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class PlayDetails:
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    call : CodeDesc
        play call code and description
    description : str
        description of the play
    event : str
        type of event
    eventtype : str
        type of event
    isinplay : bool
        is the ball in play true or false
    isstrike : bool
        is the ball a strike true or false
    isball : bool
        is it a ball true or false
    isbasehit : bool
        is the event a base hit true or false
    isatbat : bool
        is the event at bat true or false
    isplateappearance : bool
        is the event a at play appears true or false
    type : CodeDesc
        type of pitch code and description
    batside : CodeDesc
        bat side code and description
    pitchhand : CodeDesc
        pitch hand code and description
    fromcatcher : bool
    """
    call: Optional[Union[CodeDesc, dict]] = None
    isinplay: Optional[bool] = None
    isstrike: Optional[bool] = None
    isscoringplay: Optional[bool] = None
    isout: Optional[bool] = None
    runnergoing: Optional[bool] = None
    isball: Optional[bool] = None
    isbasehit: Optional[bool] = None
    isatbat: Optional[bool] = None
    isplateappearance: Optional[bool] = None
    batside: Optional[Union[CodeDesc, dict]] = field(default_factory=dict)
    pitchhand: Optional[Union[CodeDesc, dict]] = field(default_factory=dict)
    eventtype: Optional[str] = None
    event: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Union[CodeDesc, dict]] = field(default_factory=dict)
    awayscore: Optional[int] = None
    homescore: Optional[int] = None
    hasreview: Optional[bool] = None
    code: Optional[str] = None
    ballcolor: Optional[str] = None
    trailcolor: Optional[str] = None
    fromcatcher: Optional[bool] = None

    def __post_init__(self):
        self.call = CodeDesc(**self.call) if self.call else self.call
        self.batside = CodeDesc(**self.batside) if self.batside else self.batside
        self.pitchhand = CodeDesc(**self.pitchhand) if self.pitchhand else self.pitchhand
        self.type = CodeDesc(**self.type) if self.type else self.type

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))