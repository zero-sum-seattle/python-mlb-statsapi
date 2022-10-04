from typing import List, Dict, Union
from dataclasses import dataclass, field
from mlbstatsapi.models.stats import Stats
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport
from mlbstatsapi import MlbObject

@dataclass
class Team(MlbObject):
    """
    A class to represent a Team.

    Attributes
    ----------
    id : int
        id number of the team
    name: str
        name of the person
    """
    id: int
    name: str
    link: str
    springLeague: Union[League,dict]
    allStarStatus: str
    season: int
    venue:  Union[Venue,dict]
    springVenue:  Union[Venue,dict]
    teamCode: str
    fileCode: str
    abbreviation: str
    teamName: str
    locationName: str
    firstYearOfPlay: str
    league: Union[League,dict]
    division: Union[Division,dict]
    sport: Union[Sport,dict]
    shortName: str
#    record: Union[LeagueRecord, dict]
    franchiseName: str
    clubName: str
    active: bool
    mlb_class = "teams"
    stats: Union[Stats, dict] = field(default_factory=dict)


    def __post_init__(self):
        self.league = League(**self.league)
        self.sport = Sport(**self.sport)
        self.venue = Venue(**self.venue)
        self.springVenue = Venue(**self.springVenue)
        self.spring_league = League(**self.springLeague)
        self.division = Division(**self.division)
        self.stats = [ Stats(**stat) for stat in self.stats ] 
