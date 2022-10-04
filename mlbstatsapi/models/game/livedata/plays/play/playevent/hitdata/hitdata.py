from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class HitCoordinate:
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
    launchSpeed:    float
    launchAngle:    int
    totalDistance:  int
    trajectory:     str
    hardness:       str
    location:       str
    coordinates:    HitCoordinate

    def __post_init__(self):
        self.coordinates = HitCoordinate(**self.coordinates)
