from typing import List, Dict, Union, Optional
from dataclasses import dataclass, field


from .attributes import TeamRecord
# from mlbstatsapi.models.standings import Teamrecords


@dataclass(repr=False)
class Team:
    """
    A class to represent a Team.

    Attributes
    ----------
    id : int
        id number of the team
    name : str
        name of the team
    link : str
        The API link for the team
    springleague : League
        The spring league of the team
    allstarstatus : str
        The all status status of the team
    season : str
        The team's current season
    venue : Venue
        The team's home venue
    springvenue : Venue
        The team's spring venue
    teamcode : str
        team code 
    filecode : str
        filecode name of the team
    abbreviation : str
        The abbreviation of the team name
    teamname : str
        The team name 
    locationname : str
        The location of the team
    firstyearofplay : str
        The first year the team began play
    league : League
        The league of the team
    division : Division
        The division the team is in
    sport : Sport
        The sport of the team
    shortname : str
        The shortname of the team
    record : TeamRecord
        The record of the team
    franchisename : str
        The franchisename of the team
    clubname : str
        The clubname of the team
    active : str
        Active status of the team
    parentorgname : str
        The name of the parent team or org
    parentorgid : str
        The id of the partent team or org
    """
    id: int
    link: str
    teamName: str
    name: Optional[str] = field(default_factory=dict) 
    springLeague: dict = field(default_factory=dict) # Update with League object
    allStarStatus: Optional[str] = None
    season: Optional[str] = None
    venue: dict = field(default_factory=dict) # Update with Venue object
    springVenue: dict = field(default_factory=dict) # Update with Venue object
    fileCode: Optional[str] = None
    abbreviation: Optional[str] = None
    teamCode: Optional[str] = None
    locationName: Optional[str] = None
    firstYearOfPlay: Optional[str] = None
    league: dict = field(default_factory=dict) # Update with League object
    division: dict = field(default_factory=dict) # Update with Division object
    sport: dict = field(default_factory=dict) # Update with Sport object
    shortName: Optional[str] = None
    record: Union[TeamRecord, dict] = None
    franchiseName: Optional[str] = None
    clubName: Optional[str] = None
    active: Optional[str] = None
    parentOrgName: Optional[str] = None
    parentOrgId: Optional[str] = None

    def __post_init__(self):
        # self.springleague = League(**self.springleague) if self.springleague else self.springleague
        # self.venue = Venue(**self.venue) if self.venue else self.venue        
        # self.springvenue = Venue(**self.springvenue) if self.springvenue else self.springvenue        
        # self.league = League(**self.league) if self.league else self.league
        # self.division = Division(**self.division) if self.division else self.division
        self.record = TeamRecord(**self.record) if self.record else self.record
        # self.sport = Sport(**self.sport) if self.sport else self.sport

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))