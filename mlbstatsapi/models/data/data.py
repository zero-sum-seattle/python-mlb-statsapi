from dataclasses import dataclass, field, InitVar
from typing import List, Union, Dict, Any, Optional




@dataclass
class PitchBreak:
    """
    A class to hold pitch pitch break data
    
    Attributes
    ----------
    breakangle : float
    breaklength : float
    breaky : float
    spinrate : float
    spindirection : float
    """
    breakangle: float
    breaklength: float
    breaky: float
    spinrate: float
    spindirection: float


@dataclass
class PitchCoordinates:
    """
    A class to hold pitch coordinates for playLog

    Attributes
    ----------
    ay : float
    az : float
    pfxx : float
    pfxz : float
    px : float
    pz : float
    vx0 : float
    vy0 : float
    vz0 : float
    x : float
    y : float
    x0 : float
    y0 : float
    z0 : float
    ax : float
    """
    ay: float
    az: float
    pfxx: float
    pfxz: float
    px: float
    pz: float
    vx0: float
    vy0: float
    vz0: float
    x: float
    y: float
    x0: float
    y0: float
    z0: float
    ax: float


@dataclass
class PitchData:
    """
    A class to hold pitch pitch break data
    
    Attributes
    ----------
    startspeed : float
    endspeed : float
    strikezonetop : float
    strikezonebottom : float
    coordinates : Union[PitchCoordinates, dict]
    breaks : Union[PitchBreak, dict] 
    zone : float
    typeconfidence : float
    platetime : float
    extension : float
    """
    startspeed: float
    endspeed: float
    strikezonetop: float
    strikezonebottom: float
    coordinates: Union[PitchCoordinates, dict]
    breaks: Union[PitchBreak, dict] 
    zone:float
    typeconfidence: float
    platetime: float
    extension: float


    def __post_init__(self):
        self.coordinates = PitchCoordinates(**self.coordinates) if self.coordinates else self.coordinates
        self.breaks = PitchBreak(**self.breaks) if self.breaks else self.breaks

@dataclass
class HitCoordinates:
    """
    A class to hold pitch pitch break data
    
    Attributes
    ----------
    coordx: float
    coordy: float
    """
    coordx: float
    coordy: float

@dataclass
class HitData:
    """
    A class to hold pitch pitch break data
    
    Attributes
    ----------
    launchSpeed : float
    launchAngle : str
    totalDistance : float
    trajectory : str
    hardness : str
    location : int
    coordinates : Union[HitCoordinates, dict]
    """
    launchSpeed: float
    launchAngle: str # this is a negative number and I'm brain farting on those
    totalDistance: float
    trajectory: str
    hardness: str
    location: int
    coordinates: Union[HitCoordinates, dict]

    def __post_init__(self):
        self.coordinates = HitCoordinates(**self.coordinates) if self.coordinates else self.coordinates

@dataclass
class CodeDesc:
    """
    a class to hold a code and a description

    Attributes
    ----------
    code : str
        the pitch code to reference the pitch
    description : str
        the description of the pitch
    """
    code: str
    description: Optional[str] = None


@dataclass
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
    inning: int
    outs: int
    strikes: int
    runneron1b: Optional[bool] = None
    runneron2b: Optional[bool] = None
    runneron3b: Optional[bool] = None
    istopinning: Optional[bool] = None

@dataclass
class PlayDetails:
    """
    A class to represent a gamelog stat for a hitter

    Attributes
    ----------
    call : dict
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
    type : dict
        type of pitch code and description
    batside : dict
        bat side code and description
    pitchhand : dict
        pitch hand code and description
    """
    call: Union[CodeDesc, dict]
    isinplay: bool
    isstrike: bool
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

    def __post_init__(self):
        self.call = CodeDesc(**self.call) if self.call else self.call
        self.batside = CodeDesc(**self.batside) if self.batside else self.batside
        self.pitchhand = CodeDesc(**self.pitchhand) if self.pitchhand else self.pitchhand
        self.type = CodeDesc(**self.type) if self.type else self.type