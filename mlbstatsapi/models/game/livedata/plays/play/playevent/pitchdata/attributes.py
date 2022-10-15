from typing import Optional
from dataclasses import dataclass

@dataclass
class PitchCoordinates:
    """
    A class to represent a play events pitch data.

    Attributes
    ----------
    ay : float = None
        Pitch coordinate aY
    az : float = None
        Pitch coordinate aZ
    pfxx : float = None
        Pitch coordinate pfxX
    pfxz : float = None
        Pitch coordinate pfxZ
    px : float = None
        Pitch coordinate pX
    pz : float = None
        Pitch coordinate pZ
    vx0 : float = None
        Pitch coordinate vX0
    vy0 : float = None
        Pitch coordinate vY0
    vz0 : float = None
        Pitch coordinate vZ0
    x0 : float = None
        Pitch coordinate x0
    y0 : float = None
        Pitch coordinate y0
    z0 : float = None
        Pitch coordinate z0
    ax : float = None
        Pitch coordinate aX
    x : float = None
        Pitch coordinate x
    y : float = None
        Pitch coordinate y
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

@dataclass
class PitchBreaks:
    """
    A class to represent a play events pitch data.

    Attributes
    ----------
    breakangle : float
        Pitch break angle
    breaklength : float
        Pitch break length
    breaky : int
        Pitch break Y
    spinrate : int
        Pitch spinRate
    spindirection : int
        Pitch spinDirection
    """
    breakangle: float
    breaklength: float
    breaky: int
    spinrate: int
    spindirection: int