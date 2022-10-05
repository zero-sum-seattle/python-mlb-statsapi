from typing import Dict, Union, Any
from dataclasses import dataclass, field
from .attributes import VenueLocation, VenueTimeZone, VenueFieldInfo

@dataclass
class Venue:
    """
    A class to represent a venue.

    Attributes
    ----------
    id : int
        id for this venue
    name : str = None
        Name for this venue
    link : str
        Link to venues endpoint
    location : VenueLocation = None
        Location for this venue
    timeZone : VenueTimeZone = None
        Timezone for this venue
    fieldInfo :  VenueFieldInfo = None
        Info on this venue's field
    active : bool = None
        Is this field currently active
    """
    id:         int
    link:       str
    name:       str = None
    location:   Union[VenueLocation, Dict[str, Any]] = None
    timeZone:   Union[VenueTimeZone, Dict[str, Any]] = None
    fieldInfo:  Union[VenueFieldInfo, Dict[str, Any]] = None
    active:     bool = None

    def __post_init__(self):
        self.location = VenueLocation(**self.location) if self.location else self.location
        self.timeZone = VenueTimeZone(**self.timeZone) if self.timeZone else self.timeZone
        self.fieldInfo = VenueFieldInfo(**self.fieldInfo) if self.fieldInfo else self.fieldInfo
