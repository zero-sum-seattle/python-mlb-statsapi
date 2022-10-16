from typing import Union
from dataclasses import dataclass

from .attributes import PitchCoordinates, PitchBreaks

@dataclass
class PitchData:
    """
    A class to represent a play events pitch data.

    Attributes
    ----------
    startspeed : float
        Pitch start speed
    endspeed : float
        Pitch end speed
    strikezonetop : float
        Batters strike zone top
    strikezonebottom : float
        Batters strike zone bottom
    coordinates : Dict
        Pitch coordinates
    breaks : Dict
        Pitch breaks
    zone : int
        Pitch zone
    typeconfidence : float
        Type confidence
    platetime : float
        Pitch platetime
    extension : float
        Pitch extension
    """
    startspeed: float
    endspeed: float
    strikezonetop: float
    strikezonebottom: float
    coordinates: Union[PitchCoordinates, dict]
    breaks: Union[PitchBreaks, dict]
    zone: int
    typeconfidence: float
    platetime: float
    extension: float

    def __post_init__(self):
        self.coordinates = PitchCoordinates(**self.coordinates)
        self.breaks = PitchBreaks(**self.breaks)