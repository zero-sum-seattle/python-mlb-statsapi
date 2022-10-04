from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class GameVenueLocationCoordinates:
    """
    A class to represent a venues exact.

    Attributes
    ----------
    latitude : float
        The latatude coordinate for this venue
    longitude : float
        The longitude coordinate for this venue
    """
    latitude:   float
    longitude:  float

@dataclass
class GameVenueLocation:
    """
    A class to represent a venues location.

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
    defaultCoordinates : GameVenueLocationCoordinates
        Long and lat for this venues location
    country : str
        What country this venue is in
    phone : str
        Phone number for this venue
    """
    address1:           str
    city:               str
    state:              str
    stateAbbrev:        str
    postalCode:         str
    defaultCoordinates: Union[GameVenueLocationCoordinates, Dict[str, Any]]
    country:            str
    phone:              str
    address2:           str = None

    def __post_init__(self):
        self.defaultCoordinates = GameVenueLocationCoordinates(**self.defaultCoordinates)
