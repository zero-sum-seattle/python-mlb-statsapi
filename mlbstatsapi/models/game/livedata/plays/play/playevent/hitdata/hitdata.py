from typing import Union, Dict, Any
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
    launchSpeed:    float
    launchAngle:    int
    totalDistance:  int
    trajectory:     str
    hardness:       str
    location:       str
    coordinates:    HitCoordinate

    def __post_init__(self):
        self.coordinates = HitCoordinate(**self.coordinates)
