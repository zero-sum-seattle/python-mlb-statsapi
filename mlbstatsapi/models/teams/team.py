from typing import Optional
from pydantic import BaseModel

from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport

from .attributes import TeamRecord
# from mlbstatsapi.models.standings import Teamrecords


class Team(BaseModel):
    """Represents a Team.

    Attributes:
        id (int): ID number of the team.
        name (str, optional): Name of the team. Optional.
        link (str): The API link for the team.
        springLeague (League, optional): The spring league of the team. Optional.
        allStarStatus (str, optional): The all-star status of the team. Optional.
        season (int, optional): The team's current season. Optional.
        venue (Venue, optional): The team's home venue. Optional.
        springVenue (Venue, optional): The team's spring venue. Optional.
        teamCode (str, optional): Team code. Optional.
        fileCode (str, optional): File code name of the team. Optional.
        abbreviation (str, optional): The abbreviation of the team name. Optional.
        teamName (str, optional): The team name. Optional.
        locationName (str, optional): The location of the team. Optional.
        firstYearOfPlay (str, optional): The first year the team began play. Optional.
        league (League, optional): The league of the team. Optional.
        division (Division, optional): The division the team is in. Optional.
        sport (Sport, optional): The sport of the team. Optional.
        shortName (str, optional): The short name of the team. Optional.
        record (TeamRecord, optional): The record of the team. Optional.
        franchiseName (str, optional): The franchise name of the team. Optional.
        clubName (str, optional): The club name of the team. Optional.
        active (bool, optional): Active status of the team. Optional.
        parentorgname (str, optional): The name of the parent organization. Optional.
        parentorgid (str, optional): The ID of the parent organization. Optional.
    """

    id: int
    link: str
    name: Optional[str] = None
    springLeague: Optional[League] = None
    allStarStatus: Optional[str] = None
    season: Optional[int] = None
    venue: Optional[Venue] = None
    springVenue: Optional[Venue] = None
    teamCode: Optional[str] = None
    fileCode: Optional[str] = None
    abbreviation: Optional[str] = None
    teamName: Optional[str] = None
    locationName: Optional[str] = None
    firstYearOfPlay: Optional[str] = None
    league: Optional[League] = None
    division: Optional[Division] = None
    sport: Optional[Sport] = None
    shortName: Optional[str] = None
    record: Optional[TeamRecord] = None
    franchiseName: Optional[str] = None
    clubName: Optional[str] = None
    active: Optional[bool] = None
    parentorgname: Optional[str] = None
    parentorgid: Optional[str] = None
