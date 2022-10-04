from typing import Union, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.League import League
from mlbstatsapi.models.venue import Venue
from mlbstatsapi.models.division import Division
from mlbstatsapi.models.sport import Sport

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
        self.springLeague = League(**springLeague)
        self.venue = Venue(**venue)
        self.springVenue = Venue(**springVenue)
        self.league = League(**league)
        self.division = Division(**division)
        self.sport = Sport(**sport)
        self.record = GameTeamRecord(**record)
