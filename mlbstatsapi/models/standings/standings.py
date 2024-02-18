from typing import Union, Optional, List
from dataclasses import dataclass

from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.sports import Sport

from .attributes import Teamrecords


@dataclass(repr=False)
class Standings:
    """
    A class representing a standings in a league.


    Attributes
    ----------
    standingstype : str
        A string indicating the type of standings.
    league : league
        An object containing information about the league.
    division : Division
        An object containing information about the division
    sport : Sport
        An object containing information about the sport.
    lastupdated : str
        A string indicating the last time the standing was updated.
    teamrecords : List[Teamrecords]
        A list of Teamrecord objects containing the data for the teams standings.
    """
    standingsType: str
    league: Union[League, dict]
    division: Union[Sport, dict]
    lastupdated: str
    teamrecords: List[Teamrecords]
    sport: Optional[Sport] = None

