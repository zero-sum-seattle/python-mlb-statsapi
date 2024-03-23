from typing import Union, Optional, List
from pydantic import BaseModel
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport

from .attributes import TeamRecord


class Standings(BaseModel):
    """
    Represents standings within a league.

    Attributes:
        standingsType (str): Indicates the type of standings.
        league (League): Information about the league.
        division (Division): Information about the division.
        sport (Sport, optional): Information about the sport. Defaults to None.
        lastUpdated (str): The last time the standings were updated.
        teamRecords (List[TeamRecord]): Data for the team standings.
    """
    standingsType: Optional[str] = None
    league: League
    division: Sport
    lastUpdated: str
    teamRecords: List[TeamRecord]
    sport: Optional[Sport] = None

