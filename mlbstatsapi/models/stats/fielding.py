from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport

from .stats import Stats

@dataclass
class SimpleFielding:
    """
    A class to represent a simple fielding statistics

    """
    gamesplayed: Optional[int] = None
    gamesstarted: Optional[int] = None
    caughtstealing: Optional[int] = None
    stolenbases: Optional[int] = None
    stolenbasepercentage: Optional[str] = None
    assists: Optional[int] = None
    putouts: Optional[int] = None
    errors: Optional[int] = None
    chances: Optional[int] = None
    fielding: Optional[str] = None
    rangefactorpergame: Optional[str] = None
    rangefactorper9inn: Optional[str] = None
    innings: Optional[str] = None
    games: Optional[int] = None
    passedball: Optional[int] = None
    doubleplays: Optional[int] = None
    tripleplays: Optional[int] = None
    catcherera: Optional[str] = None
    catchersinterference: Optional[int] = None
    wildpitches: Optional[int] = None
    throwingerrors: Optional[int] = None
    pickoffs: Optional[int] = None

@dataclass(kw_only=True)
class SeasonFielding(Stats, SimpleFielding):
    type_ = [ 'season', 'seasonAdvanced', 'statsSingleSeason', 'homeAndAway', 'byDayOfWeek', 'byDateRange',
    'lastXGames', 'gameLog' ]
    season: str
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None
    team: Optional[Union[Team, dict]] = None
    player: Optional[Union[Person, dict]] = None
    league: Optional[Union[League, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
