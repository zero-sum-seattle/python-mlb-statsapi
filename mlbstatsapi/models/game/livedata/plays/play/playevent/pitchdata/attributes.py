from typing import Optional
from dataclasses import dataclass

@dataclass
class PitchCoordinates:
    """
    A class to represent a play events pitch data.

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

@dataclass
class PitchBreaks:
    """
    A class to represent a play events pitch data.

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
    breaky: int
    spinrate: int
    spindirection: int