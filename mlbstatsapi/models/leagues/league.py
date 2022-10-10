from dataclasses import dataclass
from typing import Dict, Union, Any
from mlbstatsapi.models.sports import Sport
from .attributes import LeagueSeasonDateInfo

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
    ties: int = None

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
    name:               str = None
    abbreviation:       str = None
    nameShort:          str = None
    seasonState:        str = None
    hasWildCard:        bool = None
    hasSplitSeason:     bool = None
    numGames:           int = None
    hasPlayoffPoints:   bool = None
    numTeams:           int = None
    numWildcardTeams:   int = None
    seasonDateInfo:     Union[LeagueSeasonDateInfo, Dict[str, Any]] = None
    season:             str = None
    orgCode:            str = None
    conferencesInUse:   bool = None
    divisionsInUse:     bool = None
    sport:              Union[Sport, Dict[str, Any]] = None
    sortOrder:          int = None
    active:             bool = None

    def __post_init__(self):
        self.seasonDateInfo = LeagueSeasonDateInfo(**self.seasonDateInfo) if self.seasonDateInfo else self.seasonDateInfo
        self.sport = Sport(**self.sport) if self.sport else self.sport
