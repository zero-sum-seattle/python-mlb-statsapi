from typing import Optional, Union
from pydantic import BaseModel
from .attributes import Location, TimeZone, FieldInfo

class Venue(BaseModel):
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
    id: int
    link: str
    name: Optional[str] = None
    location: Optional[Location] = None
    timezone: Optional[TimeZone] = None
    fieldinfo: Optional[FieldInfo] = None
    active: Optional[bool] = None
    season: Optional[str] = None
