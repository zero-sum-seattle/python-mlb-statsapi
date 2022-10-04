from typing import Union, Dict, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.gamedata.gamevenue.gamevenuelocation import GameVenueLocation

@dataclass
class GameVenueTimeZone:
    """
    A class to represent a venues field information.

    Attributes
    ----------
    id : str
        id string for a venues timezone
    offset : int
        The offset for this timezone from
    tz : str
        Timezone string
    """
    id:     str
    offset: int
    tz:     str

@dataclass
class GameVenueFieldInfo:
    """
    A class to represent a venues field information.

    Attributes
    ----------
    capacity : int
        Capacity for this venue
    turfType : str
        The type of turf in this venue
    roofType : str
        What kind of roof for this venue
    leftLine : int
        Distance down the left line
    left : int
        Distance to left
    leftCenter : int
        Distance to left center
    center : int
        Distance to center
    rightCenter : int
        Distance to right center
    rightLine : int
        Distance to right line
    """
    capacity:       int
    turfType:       str
    roofType:       str
    leftLine:       int = None
    left:           int = None
    leftCenter:     int = None
    center:         int = None
    rightCenter:    int = None
    right:          int = None
    rightLine:      int = None

@dataclass
class GameVenue:
    """
    A class to represent a Games venue.

    Attributes
    ----------
    id : int
        id for this venue
    name : str
        Name for this venue
    link : str
        Link to venues endpoint
    location : GameVenueLocation
        Location for this venue
    timeZone : GameVenueTimeZone
        TImezone for this venue
    fieldInfo : GameVenueFieldInfo
        Info on this venue's field
    active : bool
        Is this field currently active
    """
    id:         int
    name:       str
    link:       str
    location:   Union[GameVenueLocation, Dict[str, Any]]
    timeZone:   Union[GameVenueTimeZone, Dict[str, Any]]
    fieldInfo:  Union[GameVenueFieldInfo, Dict[str, Any]]
    active:     bool

    def __post_init__(self):
        self.location = GameVenueLocation(**self.location)
        self.timeZone = GameVenueTimeZone(**self.timeZone)
        self.fieldInfo = GameVenueFieldInfo(**self.fieldInfo)
