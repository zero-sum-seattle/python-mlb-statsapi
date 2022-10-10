from typing import List, Dict, Union, Optional
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
    mlb_class = "teams"
    springLeague: Union[League,dict] = field(default_factory=dict)
    allStarStatus: Optional[str]  = None
    season: Optional[str]  = None
    venue:  Union[Venue,dict] = field(default_factory=dict)
    springVenue:  Union[Venue,dict] = field(default_factory=dict)
    teamCode: Optional[str] = None
    fileCode: Optional[str] = None
    abbreviation: Optional[str]  = None
    teamName: Optional[str]  = None
    locationName: Optional[str]  = None
    firstYearOfPlay: Optional[str]  = None
    league: Union[League,dict] = field(default_factory=dict)
    division: Union[Division,dict] = field(default_factory=dict)
    sport: Union[Sport,dict] = field(default_factory=dict)
    shortName: Optional[str]  = None
#    record: Union[LeagueRecord, dict]
    franchiseName: Optional[str]  = None
    clubName: Optional[str]  = None
    active: Optional[str]  = None
    stats: Union[Stats, dict] = field(default_factory=dict)
    parentOrgName: str = None
    parentOrgId: str = None

    def __post_init__(self):
        self.league = League(**self.league) if self.league else self.league
        self.sport = Sport(**self.sport) if self.sport else self.sport
        self.venue = Venue(**self.venue) if self.venue else self.venue
        self.springVenue = Venue(**self.springVenue) if self.springVenue else self.springVenue
        self.springLeague = League(**self.springLeague) if self.springLeague else self.springLeague
        self.division = Division(**self.division) if self.division else self.division
        self.stats = [ Stats(**stat) for stat in self.stats ] if self.stats else self.stats
