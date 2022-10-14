from typing import Optional, Union
from dataclasses import dataclass
from .attributes import Location, TimeZone, FieldInfo

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
    name:       Optional[str] = None
    location:   Optional[Union[Location, dict]] = None
    timeZone:   Optional[Union[TimeZone, dict]] = None
    fieldInfo:  Optional[Union[FieldInfo, dict]] = None
    active:     Optional[bool] = None

    def __post_init__(self):
        self.location = Location(**self.location) if self.location else self.location
        self.timeZone = TimeZone(**self.timeZone) if self.timeZone else self.timeZone
        self.fieldInfo = FieldInfo(**self.fieldInfo) if self.fieldInfo else self.fieldInfo
