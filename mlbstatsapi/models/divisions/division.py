from typing import Optional, Union
from pydantic import BaseModel

from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport


class Division(BaseModel):
    """
    A class to represent a division within a league, including its identification, name, associated league and sport, among other details.

    Attributes:
        id (int): The unique identifier number of the division.
        link (str): The API link for the division details.
        name (Optional[str]): The name of the division.
        season (Optional[str]): The current season for the division.
        nameShort (Optional[str]): The short name for the division.
        abbreviation (Optional[str]): The abbreviation of the division name.
        league (Optional[League]): The league this division is part of.
        sport (Optional[Sport]): The sport this division is associated with.
        hasWildcard (Optional[bool]): Indicates if this league has a wildcard system.
        sortOrder (Optional[int]): The sort order of the division.
        numPlayoffTeams (Optional[int]): The number of playoff teams in the division.
        active (Optional[bool]): The current status of this division (active/inactive).
    """
    id: int
    link: str
    name: Optional[str] = None
    season: Optional[str] = None
    nameShort: Optional[str] = None
    abbreviation: Optional[str] = None
    league: Optional[League] = None
    sport: Optional[Sport] = None
    hasWildcard: Optional[bool] = None
    sortOrder: Optional[int] = None
    numPlayoffTeams: Optional[int] = None
    active: Optional[bool] = None

