from typing import Union, List, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport

@dataclass
class GameTeamRecord:
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
