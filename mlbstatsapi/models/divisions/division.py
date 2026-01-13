from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.sports import Sport

if TYPE_CHECKING:
    from mlbstatsapi.models.leagues import League


class Division(MLBBaseModel):
    """
    A class to represent a division.

    Attributes
    ----------
    id : int
        ID number of the division.
    link : str
        API link for the division.
    name : str
        Name of the division.
    season : str
        Current season for the division.
    name_short : str
        Short name for the division.
    abbreviation : str
        Abbreviation of the division name.
    league : League
        League this division is in.
    sport : Sport
        Sport this division is in.
    has_wildcard : bool
        Whether this league has a wildcard.
    sort_order : int
        Sort order.
    num_playoff_teams : int
        Number of playoff teams in division.
    active : bool
        Current status of this division.
    """
    id: int
    link: str
    name: Optional[str] = None
    season: Optional[str] = None
    name_short: Optional[str] = Field(default=None, alias="nameshort")
    abbreviation: Optional[str] = None
    league: Optional[League] = None
    sport: Optional[Sport] = None
    has_wildcard: Optional[bool] = Field(default=None, alias="haswildcard")
    sort_order: Optional[int] = Field(default=None, alias="sortorder")
    num_playoff_teams: Optional[int] = Field(default=None, alias="numplayoffteams")
    active: Optional[bool] = None

    model_config = {"arbitrary_types_allowed": True}
