from pydantic import BaseModel
from typing import Optional, Union, Any

from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.seasons import Season



class League(BaseModel):
    """
    Represents a league, detailing its identification, name, associated sport, and other relevant characteristics such as season state, wildcard status, and organizational details.

    Attributes:
        id (int): The unique identifier number of the league.
        link (str): The API link for the league details.
        name (Optional[str]): The name of the league.
        abbreviation (Optional[str]): The abbreviation of the league.
        nameShort (Optional[str]): The short name for the league.
        seasonState (Optional[str]): The state of the league's season.
        hasWildCard (Optional[bool]): Indicates if the league has a wildcard system.
        hasSplitSeason (Optional[bool]): Indicates if the league has a split season.
        numGames (Optional[int]): The total number of games in the league.
        hasPlayoffPoints (Optional[bool]): Indicates if the league uses playoff points.
        numTeams (Optional[int]): The total number of teams in the league.
        numWildcardTeams (Optional[int]): The total number of wildcard teams in the league.
        seasonDateInfo (Optional[Season]): The season date information.
        season (Optional[str]): The current season of the league.
        orgCode (Optional[str]): The organization code of the league.
        conferencesInUse (Optional[bool]): Indicates if conferences are in use within the league.
        divisionsInUse (Optional[bool]): Indicates if divisions are in use within the league.
        sport (Optional[Sport]): The sport this league is a part of.
        sortOrder (Optional[int]): The sort order of the league.
        active (Optional[bool]): The activity status of the league.
    """
    id: int
    link: str
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    nameShort: Optional[str] = None
    seasonState: Optional[str] = None
    hasWildCard: Optional[bool] = None
    hasSplitSeason: Optional[bool] = None
    numGames: Optional[int] = None
    hasPlayoffPoints: Optional[bool] = None
    numTeams: Optional[int] = None
    numWildcardTeams: Optional[int] = None
    seasonDateInfo: Optional[Season] = None
    season: Optional[str] = None
    orgCode: Optional[str] = None
    conferencesInUse: Optional[bool] = None
    divisionsInUse: Optional[bool] = None
    sport: Optional[Sport] = None
    sortOrder: Optional[int] = None
    active: Optional[bool] = None