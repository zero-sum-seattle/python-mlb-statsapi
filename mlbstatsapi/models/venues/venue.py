from typing import Optional, Union
from dataclasses import dataclass
from .attributes import Location, TimeZone, FieldInfo

@dataclass(repr=False)
class Venue:
    """
    A class to represent a venue.

    Attributes
    ----------
    id : int
        id for this venue
    name : str
        Name for this venue
    link : str
        Link to venues endpoint
    location : Location
        Location for this venue
    timezone : TimeZone
        Timezone for this venue
    fieldinfo :  FieldInfo
        Info on this venue's field
    active : bool
        Is this field currently active
    season : str
        This field holds the season
    """
    id:         int
    link:       str
    name:       Optional[str] = None
    location:   Optional[Union[Location, dict]] = None
    timezone:   Optional[Union[TimeZone, dict]] = None
    fieldinfo:  Optional[Union[FieldInfo, dict]] = None
    active:     Optional[bool] = None
    season:     Optional[str] = None

    def __post_init__(self):
        self.location = Location(**self.location) if self.location else self.location
        self.timezone = TimeZone(**self.timezone) if self.timezone else self.timezone
        self.fieldinfo = FieldInfo(**self.fieldinfo) if self.fieldinfo else self.fieldinfo

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))