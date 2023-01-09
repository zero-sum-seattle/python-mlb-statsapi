from typing import Optional, Union
from dataclasses import dataclass, field

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

@dataclass(repr=False)
class Location:
    """
    A class to represent a Location used by venue.

    Attributes
    ----------
    address1 : str
        Venues first address line
    address2 : str
        Venues second address line
    city : str
        City the venue is in
    state : str
        The State the venue is in
    stateAbbrev : str
        The staes abbreviation
    postalCode : str
        Postal code for this venue
    defaultCoordinates : VenueDefaultCoordinates
        Long and lat for this venues location
    country : str
        What country this venue is in
    phone : str
        Phone number for this venue
    """
    city: str
    country: str
    stateabbrev: Optional[str] = None
    address1: Optional[str] = None
    state: Optional[str] = None
    postalcode: Optional[str] = None
    phone: Optional[str] = None
    address2: Optional[str] = None
    defaultcoordinates: Optional[Union[VenueDefaultCoordinates, dict]] = field(default_factory=dict)

    def __post_init__(self):
        self.defaultcoordinates = VenueDefaultCoordinates(**self.defaultcoordinates) if self.defaultcoordinates else self.defaultcoordinates

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

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

@dataclass(repr=False)
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
    right : int
        Distance to right
    rightLine : int
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

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))