from pydantic import BaseModel
from typing import Optional, Union, Any

from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.seasons import Season


class LeagueRecord(BaseModel):
    """
    A class to represent a leaguerecord.

    Attributes
    ----------
    wins : int
        number of wins in leaguerecord
    losses : int
        number of losses in leaguerecord
    ties : int
        number of ties in leaguerecord
    pct : str
        winning pct of leaguerecord
    """
    wins: int
    losses: int
    pct: str
    ties: Optional[int]


class League(BaseModel):
    """
    A class to represent a league.

    Attributes
    ----------
    id : int
        id number of the league
    name : str
        name of the league
    link : str
        link of the league
    abbreviation : str
        abbreviation the league
    nameshort : str
        Short name for the league
    seasonstate : str
        State of the leagues season
    haswildcard : bool
        Status of the leagues wildcard
    hassplitseason : bool
        Status of the leagues split season
    numgames : int
        Total number of league games
    hasplayoffpoints : bool
        Status of the leagues playoff points
    numteams : int
        Total number of team in league
    numwildcardteams : int
        Total number of wildcard teams in league
    seasondateinfo : Season
        Season obj
    season : str
        League season
    orgcode : str
        Leagues orginization code
    conferencesinuse : bool
        Status of the in use conferences of the league
    divisionsinuse : bool
        Status of leagues divisions in use
    sport : Sport
        What 'sport' this league is a part of
    sortorder : int
        League sort order
    active : bool
        Status on the activity of the league
    """
    id: int
    link: str
    name: Optional[str]
    abbreviation: Optional[str]
    nameShort: Optional[str]
    seasonState: Optional[str]
    hasWildCard: Optional[bool]
    hasSplitSeason: Optional[bool]
    numGames: Optional[int]
    hasPlayoffPoints: Optional[bool]
    numTeams: Optional[int]
    numWildcardTeams: Optional[int]
    seasonDateInfo: Optional[Union[Season, dict[str, Any]]]
    season: Optional[str]
    orgCode: Optional[str]
    conferencesInUse: Optional[bool]
    divisionsInUse: Optional[bool]
    sport: Optional[Union[Sport, dict[str, Any]]]
    sortOrder: Optional[int]
    active: Optional[bool]