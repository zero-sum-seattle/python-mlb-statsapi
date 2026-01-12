from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport
from .attributes import TeamRecord


class Team(MLBBaseModel):
    """
    A class to represent a Team.

    Attributes
    ----------
    id : int
        ID number of the team.
    link : str
        The API link for the team.
    name : str
        Name of the team.
    spring_league : League
        The spring league of the team.
    all_star_status : str
        The all-star status of the team.
    season : int
        The team's current season.
    venue : Venue
        The team's home venue.
    spring_venue : Venue
        The team's spring venue.
    team_code : str
        Team code.
    file_code : str
        File code name of the team.
    abbreviation : str
        The abbreviation of the team name.
    team_name : str
        The team name.
    location_name : str
        The location of the team.
    first_year_of_play : str
        The first year the team began play.
    league : League
        The league of the team.
    division : Division
        The division the team is in.
    sport : Sport
        The sport of the team.
    short_name : str
        The short name of the team.
    record : TeamRecord
        The record of the team.
    franchise_name : str
        The franchise name of the team.
    club_name : str
        The club name of the team.
    active : bool
        Active status of the team.
    parent_org_name : str
        The name of the parent team or org.
    parent_org_id : int
        The ID of the parent team or org.
    """
    id: int
    link: str
    name: Optional[str] = None
    spring_league: Optional[League] = Field(default=None, alias="springleague")
    all_star_status: Optional[str] = Field(default=None, alias="allstarstatus")
    season: Optional[int] = None
    venue: Optional[Venue] = None
    spring_venue: Optional[Venue] = Field(default=None, alias="springvenue")
    team_code: Optional[str] = Field(default=None, alias="teamcode")
    file_code: Optional[str] = Field(default=None, alias="filecode")
    abbreviation: Optional[str] = None
    team_name: Optional[str] = Field(default=None, alias="teamname")
    location_name: Optional[str] = Field(default=None, alias="locationname")
    first_year_of_play: Optional[str] = Field(default=None, alias="firstyearofplay")
    league: Optional[League] = None
    division: Optional[Division] = None
    sport: Optional[Sport] = None
    short_name: Optional[str] = Field(default=None, alias="shortname")
    record: Optional[TeamRecord] = None
    franchise_name: Optional[str] = Field(default=None, alias="franchisename")
    club_name: Optional[str] = Field(default=None, alias="clubname")
    active: Optional[bool] = None
    parent_org_name: Optional[str] = Field(default=None, alias="parentorgname")
    parent_org_id: Optional[int] = Field(default=None, alias="parentorgid")
