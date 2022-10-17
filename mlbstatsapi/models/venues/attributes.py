from typing import Optional, Union
from dataclasses import dataclass

@dataclass
class VenueDefaultCoordinates:
    """
    A class to represent a venue.

    Attributes
    ----------
    latitude : float
        The latatude coordinate for this venue
    longitude : float
        The longitude coordinate for this venue
    """
    latitude: float
    longitude: float

@dataclass
class Location:
    """
    A class to represent a Location used by venue.

    Attributes
    ----------
    address1 : str
        Venues first address line
    address2 : str = None
        Venues second address line
    city : str
        City the venue is in
    state : str
        The State the venue is in
    stateAbbrev : str
        The staes abbreviation
    postalCode : str
        Postal code for this venue
    defaultCoordinates : Union[VenueDefaultCoordinates, Dict[str, Any]]
        Long and lat for this venues location
    country : str
        What country this venue is in
    phone : str
        Phone number for this venue
    """
    address1: str
    city: str
    state: str
    stateabbrev: str
    postalcode: str
    defaultcoordinates: Union[VenueDefaultCoordinates, dict]
    country: str
    phone: str
    address2: Optional[str] = None

    def __post_init__(self):
        self.defaultcoordinates = VenueDefaultCoordinates(**self.defaultcoordinates)

@dataclass
class TimeZone:
    """
    A class to represent a TimeZone Used by venue.

    Attributes
    ----------
    id : str
        id string for a venues timezone
    offset : int
        The offset for this timezone from
    tz : str
        Timezone string
    """
    id: str
    offset: int
    tz: str

@dataclass
class FieldInfo:
    """
    A class to represent a venue Field info.

    Attributes
    ----------
    capacity : int
        Capacity for this venue
    turfType : str
        The type of turf in this venue
    roofType : str
        What kind of roof for this venue
    leftLine : int = None
        Distance down the left line
    left : int = None
        Distance to left
    leftCenter : int = None
        Distance to left center
    center : int = None
        Distance to center
    rightCenter : int = None
        Distance to right center
    right : int = None
        Distance to right
    rightLine : int = None
        Distance to right line
    """
    capacity: Optional[int] = None
    turftype: Optional[str] = None
    rooftype: Optional[str] = None
    leftline: Optional[int] = None
    left: Optional[int] = None
    leftcenter: Optional[int] = None
    center: Optional[int] = None
    rightcenter: Optional[int] = None
    right: Optional[int] = None
    rightline: Optional[int] = None
