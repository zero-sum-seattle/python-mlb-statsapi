from dataclasses import dataclass
from typing import Optional, Union

from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport


@dataclass(repr=False)
class Division:
    """
    A class to represent a division.

    Attributes
    ----------
    id : int
        id number of the divison
    name : str
        name of the division
    link : str
        link of the division
    season : str
        Current season for the division
    nameshort : str
        Short name for the division
    abbreviation : str
        Abbreviation of the divison name
    league : League
        League this division is in
    sport : Sport
        Sport this divison is in
    haswildcard : bool
        If this league has a wildcard
    sortorder : int
        Sort order
    numplayoffteams : int
        Number of playoff teams in division
    active : bool
        Current status of this division
    """
    id: int
    link: str
    name: Optional[str] = None
    season: Optional[str] = None
    nameshort: Optional[str] = None
    abbreviation: Optional[str] = None
    league: Optional[Union[League, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
    haswildcard: Optional[bool] = None
    sortorder: Optional[int] = None
    numplayoffteams: Optional[int] = None
    active: Optional[bool] = None

    def __post_init__(self):
        self.league = League(**self.league) if self.league else self.league
        self.sport = Sport(**self.sport) if self.sport else self.sport

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))