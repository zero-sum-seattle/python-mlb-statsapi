from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class PitchCoordinates:
    """
    A class to represent a play events pitch data.

    Attributes
    ----------
    aY : float = None
        Pitch coordinate aY
    aZ : float = None
        Pitch coordinate aZ
    pfxX : float = None
        Pitch coordinate pfxX
    pfxZ : float = None
        Pitch coordinate pfxZ
    pX : float = None
        Pitch coordinate pX
    pZ : float = None
        Pitch coordinate pZ
    vX0 : float = None
        Pitch coordinate vX0
    vY0 : float = None
        Pitch coordinate vY0
    vZ0 : float = None
        Pitch coordinate vZ0
    x0 : float = None
        Pitch coordinate x0
    y0 : float = None
        Pitch coordinate y0
    z0 : float = None
        Pitch coordinate z0
    aX : float = None
        Pitch coordinate aX
    x : float = None
        Pitch coordinate x
    y : float = None
        Pitch coordinate y
    """
    aY:     float = None
    aZ:     float = None
    pfxX:   float = None
    pfxZ:   float = None
    pX:     float = None
    pZ:     float = None
    vX0:    float = None
    vY0:    float = None
    vZ0:    float = None
    x0:     float = None
    y0:     float = None
    z0:     float = None
    aX:     float = None
    x:      float = None
    y:      float = None

@dataclass
class PitchBreaks:
    """
    A class to represent a play events pitch data.

    Attributes
    ----------
    breakAngle : float
        Pitch break angle
    breakLength : float
        Pitch break length
    breakY : int
        Pitch break Y
    spinRate : int
        Pitch spinRate
    spinDirection : int
        Pitch spinDirection
    """
    breakAngle:     float
    breakLength:    float
    breakY:         int
    spinRate:       int
    spinDirection:  int

@dataclass
class PitchData:
    """
    A class to represent a play events pitch data.

    Attributes
    ----------
    startSpeed : float
        Pitch start speed
    endSpeed : float
        Pitch end speed
    strikeZoneTop : float
        Batters strike zone top
    strikeZoneBottom : float
        Batters strike zone bottom
    coordinates : Dict
        Pitch coordinates
    breaks : Dict
        Pitch breaks
    zone : int
        Pitch zone
    typeConfidence : float
        Type confidence
    plateTime : float
        Pitch platetime
    extension : float
        Pitch extension
    """
    startSpeed:         float
    endSpeed:           float
    strikeZoneTop:      float
    strikeZoneBottom:   float
    coordinates:        Dict
    breaks:             Dict
    zone:               int
    typeConfidence:     float
    plateTime:          float
    extension:          float

    def __post_init__(self):
        self.coordinates = PitchCoordinates(**self.coordinates)
        self.breaks = PitchBreaks(**self.breaks)
