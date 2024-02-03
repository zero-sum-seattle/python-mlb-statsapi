from typing import List, Dict, Union, Optional, Any
from pydantic import BaseModel

from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport

from .attributes import TeamRecord
# from mlbstatsapi.models.standings import Teamrecords


class Team(BaseModel):
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
    name: Optional[str]
    springLeague: Union[League, Dict[str, Any]]
    allStarStatus: Optional[str]
    season: Optional[str]
    venue: Union[Venue, Dict[str, Any]]
    springVenue: Union[Venue, Dict[str, Any]]
    teamCode: Optional[str]
    fileCode: Optional[str]
    abbreviation: Optional[str]
    teamName: Optional[str]
    locationName: Optional[str]
    firstYearOfPlay: Optional[str]
    league: Union[League, Dict[str, Any]]
    division: Union[Division, Dict[str, Any]]
    sport: Union[Sport, Dict[str, Any]]
    shortName: Optional[str]
    record: Optional[Union[TeamRecord, Dict[str, Any]]]
    franchiseName: Optional[str]
    clubName: Optional[str]
    active: Optional[str]
    parentorgname: Optional[str]
    parentorgid: Optional[str]
