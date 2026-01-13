from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel


class VenueDefaultCoordinates(MLBBaseModel):
    """
    A class to represent venue coordinates.

    Attributes
    ----------
    latitude : float
        The latitude coordinate for this venue.
    longitude : float
        The longitude coordinate for this venue.
    """
    latitude: float
    longitude: float


class Location(MLBBaseModel):
    """
    A class to represent a location used by venue.

    Attributes
    ----------
    city : str
        City the venue is in.
    country : str
        Country this venue is in.
    state_abbrev : str
        The state's abbreviation.
    address1 : str
        Venue's first address line.
    address2 : str
        Venue's second address line.
    address3 : str
        Venue's third address line.
    state : str
        The state the venue is in.
    postal_code : str
        Postal code for this venue.
    phone : str
        Phone number for this venue.
    azimuth_angle : float
        Azimuth angle for this venue.
    elevation : int
        Elevation for this venue.
    default_coordinates : VenueDefaultCoordinates
        Latitude and longitude for this venue's location.
    """
    city: str
    country: str
    state_abbrev: Optional[str] = Field(default=None, alias="stateabbrev")
    address1: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = Field(default=None, alias="postalcode")
    phone: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    azimuth_angle: Optional[float] = Field(default=None, alias="azimuthangle")
    elevation: Optional[int] = None
    default_coordinates: Optional[VenueDefaultCoordinates] = Field(default=None, alias="defaultcoordinates")


class TimeZone(MLBBaseModel):
    """
    A class to represent a timezone used by venue.

    Attributes
    ----------
    id : str
        ID string for a venue's timezone.
    offset : int
        The offset for this timezone.
    tz : str
        Timezone string.
    offset_at_game_time : int
        Offset at game time.
    """
    id: str
    offset: int
    tz: str
    offset_at_game_time: Optional[int] = Field(default=None, alias="offsetatgametime")


class FieldInfo(MLBBaseModel):
    """
    A class to represent venue field info.

    Attributes
    ----------
    capacity : int
        Capacity for this venue.
    turf_type : str
        The type of turf in this venue.
    roof_type : str
        What kind of roof for this venue.
    left_line : int
        Distance down the left line.
    left : int
        Distance to left.
    left_center : int
        Distance to left center.
    center : int
        Distance to center.
    right_center : int
        Distance to right center.
    right : int
        Distance to right.
    right_line : int
        Distance to right line.
    """
    capacity: Optional[int] = None
    turf_type: Optional[str] = Field(default=None, alias="turftype")
    roof_type: Optional[str] = Field(default=None, alias="rooftype")
    left_line: Optional[int] = Field(default=None, alias="leftline")
    left: Optional[int] = None
    left_center: Optional[int] = Field(default=None, alias="leftcenter")
    center: Optional[int] = None
    right_center: Optional[int] = Field(default=None, alias="rightcenter")
    right: Optional[int] = None
    right_line: Optional[int] = Field(default=None, alias="rightline")
