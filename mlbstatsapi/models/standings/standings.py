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
    standingstype: str
    league: Union[League, dict]
    division: Union[Sport, dict]
    lastupdated: str
    teamrecords: List[Union[Teamrecords, dict]]
    sport: Optional[Union[Sport, dict]] = None

    def __post_init__(self):
        self.league = League(**self.league)
        self.division = Division(**self.division)
        self.sport = Sport(**self.sport) if self.sport else None
        self.teamrecords = [Teamrecords(**teamrecord) for teamrecord in self.teamrecords]

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))