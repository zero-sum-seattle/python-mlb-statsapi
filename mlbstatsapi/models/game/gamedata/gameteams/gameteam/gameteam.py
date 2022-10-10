from typing import Union, List, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport

@dataclass
class GameTeamRecord:
    """
    A class to represent a teams current record.

    Attributes
    ----------
    gamesPlayed : int
        Number of game played by team
    wildCardGamesBack : str
        Number of game back from wildcard
    leagueGamesBack : str
        Number of league games back
    springLeagueGamesBack : str
        Number of game back in spring league
    sportGamesBack : str
        Number of games back in sport
    divisionGamesBack : str
        Number of games back in division
    conferenceGamesBack : str
        Number of games back in conference
    leagueRecord : Dict
        Record in league
    records : Dict
        Records
    divisionLeader : bool
        Is this team a divison leader
    wins : int
        Number of wins
    losses : int
        Number of losses
    winningPercentage : str
        Winning percentage
    """
    gamesPlayed:            int
    wildCardGamesBack:      str
    leagueGamesBack:        str
    springLeagueGamesBack:  str
    sportGamesBack:         str
    divisionGamesBack:      str
    conferenceGamesBack:    str
    leagueRecord:           Dict
    records:                Dict
    divisionLeader:         bool
    wins:                   int
    losses:                 int
    winningPercentage:      str

@dataclass
class GameTeam:
    """
    A class to represent a team info for this game.

    Attributes
    ----------
    springLeague : League
        Teams spring league
    allStarStatus : str
        Teams all star status
    id : int
        Team id
    name : str
        Team name
    link : str
        Link to teams endpoint
    season : int
        Team season
    venue : Venue
        Team's home venue
    springVenue : Venue
        Team's spring training venue
    teamCode : str
        Team code
    fileCode : str
        Team file code
    abbreviation : str
        Team name abbreviation
    teamName : str
        Team Name
    locationName : str
        Team's location
    firstYearOfPlay :str
        First year team started playing
    league : League
        Teams league
    division : Division
        Teams division
    sport : Sport
        Teams sport
    shortName : str
        Teams short name
    record : GameTeamRecord
        Teams record
    franchiseName : str
        Teams franchise name
    clubName : str
        Teams club name
    active : bool
        Is this team currently active
    """
    springLeague:       Union[League, Dict[str, Any]]
    allStarStatus:      str
    id:                 int
    name:               str
    link:               str
    season:             int
    venue:              Union[Venue, Dict[str, Any]]
    springVenue:        Union[Venue, Dict[str, Any]]
    teamCode:           str
    fileCode:           str
    abbreviation:       str
    teamName:           str
    locationName:       str
    firstYearOfPlay:    str
    league:             Union[League, Dict[str, Any]]
    division:           Union[Division, Dict[str, Any]]
    sport:              Union[Sport, Dict[str, Any]]
    shortName:          str
    record:             Union[GameTeamRecord, Dict[str, Any]]
    franchiseName:      str
    clubName:           str
    active:             bool

    def __post_init__(self):
        self.springLeague = League(**self.springLeague)
        self.venue = Venue(**self.venue)
        self.springVenue = Venue(**self.springVenue)
        self.league = League(**self.league)
        self.division = Division(**self.division)
        self.sport = Sport(**self.sport)
        self.record = GameTeamRecord(**self.record)
