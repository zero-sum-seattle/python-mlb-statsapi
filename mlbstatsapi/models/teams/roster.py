from typing import List, Union, Optional
from dataclasses import dataclass, field
from mlbstatsapi.models.people import Player

@dataclass
class Roster:
    """
    A class to represent a Team.

    Attributes
    ----------
    roster : list
        roster is a list of roster objects
    link: str
        link to the roster endpoint
    teamId: int 
        The team id of the roster
    rosterType: str
        the roster type
    season: str
        the season of the roster
    date: str
        the date of the roster
    """
    link: str
    teamId: int
    rosterType: str
    roster: List[Union[Player, dict]] = field(default_factory=dict)
    season: Optional[str] = None
    date: Optional[str] = None

    def __post_init__(self):
        self.roster = [ Player (**player) for player in self.roster ]