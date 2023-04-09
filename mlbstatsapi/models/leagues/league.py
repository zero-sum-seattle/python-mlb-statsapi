﻿from dataclasses import dataclass, field
from typing import Optional, Union

# from mlbstatsapi.models.sports import Sport
# from mlbstatsapi.models.seasons import Season


@dataclass
class LeagueRecord:
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
    ties: Optional[int] = None


@dataclass(repr=False)
class League:
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
    seasonDateInfo: dict = field(default_factory=dict) # Add Season
    season: Optional[str] = None
    orgCode: Optional[str] = None
    conferencesInUse: Optional[bool] = None
    divisionsInUse: Optional[bool] = None
    sport: dict = field(default_factory=dict) # Add Sport
    sortOrder: Optional[int] = None
    active: Optional[bool] = None

    # def __post_init__(self):
    #     self.seasondateinfo = Season(**self.seasondateinfo) if self.seasondateinfo else self.seasondateinfo
    #     self.sport = Sport(**self.sport) if self.sport else self.sport

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))