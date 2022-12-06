from typing import Union, List
from dataclasses import dataclass

from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.teams import Team

@dataclass
class Eventtype:
    code: str
    name: str

@dataclass
class Info:
    """
    A class to represent a Game's metaData.

    Attributes
    ----------
    wait : int
        No idea what this wait signifies
    
    """
    id: int
    name: str
    eventType: Union[Eventtype, dict]
    eventDate: str
    venue: Union[Venue, dict]
    isMultiDay: bool
    isPrimaryCalendar: bool
    fileCode: str
    eventNumber: int
    publicFacing: bool
    teams: List[Union[Team, dict]]

    def __post_init__(self):
        self.eventType = Eventtype(**self.eventType)
        self.venue = Venue(**self.venue)
        self.teams = [Team(**team) for team in self.teams]

@dataclass
class Status:
    state: str
    currentRound: int
    currentRoundTimeLeft: str
    inTieBreaker: bool
    tieBreakerNum: int
    clockStopped: bool
    bonusTime: bool