from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class GameVenueLocationCoordinates:
    latitude:   float
    longitude:  float

@dataclass
class GameVenueLocation:
    address1:           str
    city:               str
    state:              str
    stateAbbrev:        str
    postalCode:         str
    defaultCoordinates: Union[GameVenueLocationCoordinates, Dict[str, Any]]
    country:            str
    phone:              str

    def __post_init__(self):
        self.defaultCoordinates = GameVenueLocationCoordinates(**defaultCoordinates)
