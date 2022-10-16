from dataclasses import dataclass
from typing import Optional, Union

from mlbstatsapi.models.sports import Sport

from .attributes import SeasonDateInfo

@dataclass
class LeagueRecord:
    """
    A class to represent a leaguerecord.

    Attributes
    ----------
    wins : int
        number of wins in leaguerecord
    losses: int
        number of losses in leaguerecord
    ties: int
        number of ties in leaguerecord
    pct: str
        winning pct of leaguerecord
    """
    wins: int
    losses: int
    pct: str
    ties: Optional[int] = None

@dataclass
class League:
    """
    A class to represent a league.

    Attributes
    ----------
    id : int
        id number of the league
    name: str
        name of the league
    link : str
        link of the league
    abbreviation : str = None
        abbreviation the league
    nameShort : str = None
        Short name for the league
    seasonState : str = None
        State of the leagues season
    hasWildCard : bool = None
        Status of the leagues wildcard
    hasSplitSeason : bool = None
        Status of the leagues split season
    numGames : int = None
        Total number of league games
    hasPlayoffPoints : bool = None
        Status of the leagues playoff points
    numTeams : int = None
        Total number of team in league
    numWildcardTeams : int = None
        Total number of wildcard teams in league
    seasonDateInfo : LeagueSeasonDateInfo = None
        LeagueSeasonDateInfo attribue
    season : str = None
        League season
    orgCode : str = None
        Leagues orginization code
    conferencesInUse : bool = None
        Status of the in use conferences of the league
    divisionsInUse : bool = None
        Status of leagues divisions in use
    sport : Sport = None
        What 'sport' this league is a part of
    sortOrder : int = None
        League sort order
    active : bool = None
        Status on the activity of the league
    """
    id:                 int
    link:               str
    name:               Optional[str] = None
    abbreviation:       Optional[str] = None
    nameshort:          Optional[str] = None
    seasonstate:        Optional[str] = None
    haswildcard:        Optional[bool] = None
    hassplitseason:     Optional[bool] = None
    numgames:           Optional[int] = None
    hasplayoffpoints:   Optional[bool] = None
    numteams:           Optional[int] = None
    numwildcardteams:   Optional[int] = None
    seasondateinfo:     Optional[Union[SeasonDateInfo, dict]] = None
    season:             Optional[str] = None
    orgcode:            Optional[str] = None
    conferencesinuse:   Optional[bool] = None
    divisionsinuse:     Optional[bool] = None
    sport:              Optional[Union[Sport, dict]] = None
    sortorder:          Optional[int] = None
    active:             Optional[bool] = None

    def __post_init__(self):
        self.seasondateinfo = SeasonDateInfo(**self.seasondateinfo) if self.seasondateinfo else self.seasondateinfo
        self.sport = Sport(**self.sport) if self.sport else self.sport
