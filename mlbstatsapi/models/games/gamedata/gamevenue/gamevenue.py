from typing import Union, Dict, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.gamedata.gamevenue.gamevenuelocation import GameVenueLocation

@dataclass
class GameVenueTimeZone:
    id:     str
    offset: int
    tz:     str

@dataclass
class GameVenueFieldInfo:
    capacity:       int
    turfType:       str
    roofType:       str
    leftLine:       int
    left:           int
    leftCenter:     int
    center:         int
    rightCenter:    int
    rightLine:      int

@dataclass
class GameVenue:
    id:         int
    name:       str
    link:       str
    location:   Union[GameVenueLocation, Dict[str, Any]]
    timeZone:   Union[GameVenueTimeZone, Dict[str, Any]]
    fieldInfo:  Union[GameVenueFieldInfo, Dict[str, Any]]
    active:     bool

    def __post_init__(self):
        self.location = GameVenueLocation(**location)
        self.timeZone = GameVenueTimeZone(**timeZone)
        self.fieldInfo = GameVenueFieldInfo(**fieldInfo)
