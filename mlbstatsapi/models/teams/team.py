from typing import List, Dict, Union
from dataclasses import dataclass
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
    stats: List[Stats]
    springleague: Union[League,dict]
    allstarstatus: str
    id: int
    name: str
    link: str
    season: int
    venue:  Union[Venue,dict]
    springvenue:  Union[Venue,dict]
    teamcode: str
    filecode: str
    abbreviation: str
    teamname: str
    locationname: str
    firstyearofplay: str
    league: Union[League,dict]
    division: Union[Division,dict]
    sport: Union[Sport,dict]
    shortname: str
#    record: Union[LeagueRecord, dict]
    franchisename: str
    clubname: str
    active: bool
    mlb_class = "teams"


    def __init__(self,
                id: int,
                name: str,
                link: str,
                season: int = None,
                teamCode: str = None,
                sport: Union[Sport,dict] = None,
                venue: Union[Venue,dict] = None,
                league: Union[League,dict] = None,
                division: Union[Division,dict] = None,
                springVenue: Union[Venue,dict] = None,
                springLeague: Union[League,dict] = None,
                stats: List[Stats] = None, 
                 **kwargs) -> None:

        self.id = id
        self.name = name
        self.link = link
        self.season = season
        self.teamcode = teamCode
        self.league = League(**league) if isinstance(league, dict) else league 
        self.sport = Sport(**sport) if isinstance(sport, dict) else sport
        self.venue = Venue(**venue) if isinstance(venue, dict) else venue
        self.springVenue = Venue(**springVenue) if isinstance(springVenue, dict) else springVenue
        self.spring_league = League(**springLeague) if isinstance(springLeague, dict) else springLeague
        self.division = Division(**division) if isinstance(division, dict) else division
        self.stats = [ Stats(**stat) for stat in stats ] if isinstance(stats, dict) else []
        self.__dict__.update(kwargs)