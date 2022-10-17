from dataclasses import dataclass
from typing import Optional, Union

from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport


@dataclass
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
    season : str = None
        Current season for the division
    nameShort : str = None
        Short name for the division
    abbreviation : str = None
        Abbreviation of the divison name
    league : League = None
        League this division is in
    sport : Sport = None
        Sport this divison is in
    hasWildcard : bool = None
        If this league has a wildcard
    sortOrder : int = None
        Sort order
    numPlayoffTeams : int = None
        Number of playoff teams in division
    active : bool = None
        Current status of this division
    """
    id: int
    name: str
    link: str
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