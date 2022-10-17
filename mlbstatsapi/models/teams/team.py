from typing import List, Dict, Union, Optional
from dataclasses import dataclass, field

from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport

from .attributes import TeamRecord

@dataclass
class Team:
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
    link: str
    mlb_class = "teams"
    name: Optional[str] = field(default_factory=dict)
    springleague: Union[League,dict] = field(default_factory=dict)
    allstarstatus: Optional[str]  = None
    season: Optional[str]  = None
    venue:  Union[Venue,dict] = field(default_factory=dict)
    springvenue:  Union[Venue,dict] = field(default_factory=dict)
    teamcode: Optional[str] = None
    filecode: Optional[str] = None
    abbreviation: Optional[str]  = None
    teamname: Optional[str]  = None
    locationname: Optional[str]  = None
    firstyearofplay: Optional[str]  = None
    league: Union[League,dict] = field(default_factory=dict)
    division: Union[Division,dict] = field(default_factory=dict)
    sport: Union[Sport,dict] = field(default_factory=dict)
    shortname: Optional[str]  = None
    record: Union[TeamRecord, dict] = None
    franchisename: Optional[str]  = None
    clubname: Optional[str]  = None
    active: Optional[str]  = None
    parentorgname: str = None
    parentorgid: str = None

    def __post_init__(self):
        self.springleague = League(**self.springleague) if self.springleague else self.springleague
        self.venue = Venue(**self.venue) if self.venue else self.venue        
        self.springvenue = Venue(**self.springvenue) if self.springvenue else self.springvenue        
        self.league = League(**self.league) if self.league else self.league
        self.division = Division(**self.division) if self.division else self.division
        self.record = TeamRecord(**self.record) if self.record else self.record
        self.sport = Sport(**self.sport) if self.sport else self.sport
