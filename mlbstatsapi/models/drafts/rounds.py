from dataclasses import dataclass, field
from typing import List, Optional, Union

from .attributes import School, Home
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.data import CodeDesc

@dataclass(repr=False)
class DraftPick:
    """
    Represents a pick made in the MLB draft.

    Attributes
    ----------
    bisplayerid : int
        The unique identifier of the player associated with this draft pick.
    pickround : str
        The round of the draft in which this pick was made.
    picknumber : int
        The number of the pick in the round.
    roundpicknumber : int
        The number of the pick overall in the draft.
    rank : int
        The rank of the player among all players eligible for the draft.
    pickvalue : str
        The value of the pick, if known.
    signingbonus : str
        The signing bonus associated with this pick, if known.
    home : Home
        Information about the player's home location.
    scoutingreport : str
    A   scouting report on the player's abilities.
    school : School
        Information about the player's school or college.
    blurb : str
        A   brief summary of the player's background and accomplishments.
    headshotlink : str
        A   link to a headshot image of the player.
    team : Team or dict
        The team that made this draft pick.
    drafttype : CodeDesc
        Information about the type of draft in which this pick was made.
    isdrafted : bool
        Whether or not the player associated with this pick has been drafted.
    ispass : bool
        Whether or not the team passed on making a pick in this round.
    year : str
        The year in which the draft took place.
    """
    team: Union[Team, dict]
    drafttype: Union[CodeDesc, dict]
    isdrafted: bool
    ispass: bool
    year: str
    school: Union[School , dict] 
    home: Union[Home, dict]
    pickround:  str
    picknumber:  int
    roundpicknumber:  int
    headshotlink: Optional[str] = None
    person: Optional[Union[Person, dict]] = None
    bisplayerid: Optional[int] = None
    rank: Optional[int] = None
    pickvalue: Optional[str] = None
    signingbonus:  Optional[str] = None
    scoutingreport: Optional[str] = None
    blurb: Optional[str] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class Round:
    """
    Represents a round of the MLB draft.

    Attributes
    ----------
    round : str
        The round number of the draft, represented as a string.
    picks : List[DraftPick]
        A list of DraftPick objects representing the picks made in this round of the draft.
    """
    round: str
    picks: List[DraftPick]

    def __post_init__(self):
        self.picks = [DraftPick(**pick) for pick in self.picks]

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))