from typing import Union
from dataclasses import dataclass

from .attributes import PitchCoordinates, PitchBreaks

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
    startSpeed: float
    endSpeed: float
    strikeZoneTop: float
    strikeZoneBottom: float
    coordinates: Union[PitchCoordinates, dict]
    breaks: Union[PitchBreaks, dict]
    zone: int
    typeConfidence: float
    plateTime: float
    extension: float

    def __post_init__(self):
        self.coordinates = PitchCoordinates(**self.coordinates)
        self.breaks = PitchBreaks(**self.breaks)