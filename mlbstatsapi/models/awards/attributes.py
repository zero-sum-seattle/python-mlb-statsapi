from typing import Union, Optional
from dataclasses import dataclass

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person

@dataclass(kw_only=True, repr=False)
class Award:
    """
    This class represents an award object

    Attributes
    ----------
    id : str
        Award id
    name : str
        Name of the award
    date : str
        Date of when award was given
    season : str
        Season award is for/from
    team : Team
        Team award was to/ Player is from
    player : Person
        Person award is for
    votes : int None
        Any votes associated with award
    notes : str  None
        Any notes associated with award
    """

    id: str
    name: str
    date: str
    season: str
    team: Union[Team, dict]
    player: Union[Person, dict]
    votes: Optional[int] = None
    notes: Optional[str] = None

    def __post_init__(self):
        self.team = Team(**self.team)
        self.player = Person(**self.player)

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))