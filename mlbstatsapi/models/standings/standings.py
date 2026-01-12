from typing import Optional, List
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport
from .attributes import TeamRecords


class Standings(MLBBaseModel):
    """
    A class representing standings in a league.

    Attributes
    ----------
    standings_type : str
        A string indicating the type of standings.
    league : League
        An object containing information about the league.
    division : Division
        An object containing information about the division.
    sport : Sport
        An object containing information about the sport.
    last_updated : str
        A string indicating the last time the standing was updated.
    team_records : List[TeamRecords]
        A list of TeamRecords objects containing the data for the teams standings.
    roundrobin : dict
        Roundrobin data (if applicable).
    """
    standings_type: str = Field(alias="standingstype")
    league: League
    division: Division
    last_updated: str = Field(alias="lastupdated")
    team_records: List[TeamRecords] = Field(alias="teamrecords")
    sport: Optional[Sport] = None
    roundrobin: Optional[dict] = None
