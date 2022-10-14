from typing import Optional
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
    aY: Optional[float] = None
    aZ: Optional[float] = None
    pfxX: Optional[float] = None
    pfxZ: Optional[float] = None
    pX: Optional[float] = None
    pZ: Optional[float] = None
    vX0: Optional[float] = None
    vY0: Optional[float] = None
    vZ0: Optional[float] = None
    x0: Optional[float] = None
    y0: Optional[float] = None
    z0: Optional[float] = None
    aX: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None

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
    breakAngle: float
    breakLength: float
    breakY: int
    spinRate: int
    spinDirection: int