from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class PitchCoordinates:
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
    breakAngle:     float
    breakLength:    float
    breakY:         int
    spinRate:       int
    spinDirection:  int

@dataclass
class PitchData:
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
