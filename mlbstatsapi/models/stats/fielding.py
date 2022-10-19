from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.game import Game

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
    type_ = [ 'season', 'seasonAdvanced', 'statsSingleSeason', 
    'statsSingleSeasonAdvanced', 'careerRegularSeason', 'careerPlayoffs' ]
    season: str
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None
    team: Optional[Union[Team, dict]] = None
    player: Optional[Union[Person, dict]] = None
    league: Optional[Union[League, dict]] = None
    sport: Optional[Union[Sport, dict]] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingHAA(Stats, SimpleFielding):
    type_ = [ 'homeAndAway', 'homeAndAwayPlayoffs' ]
    season: str
    ishome: bool

@dataclass(kw_only=True)
class FieldingYBY(Stats, SimpleFielding):
    type_ = [ 'yearByYear', 'yearByYearAdvanced', 'yearByYearPlayoffs' ]
    season: str
    team: Union[Team, dict]

@dataclass(kw_only=True)
class FieldingWL(Stats, SimpleFielding):
    type_ = ['winLoss', 'winLossPlayoffs' ]
    season: str
    iswin: bool

@dataclass(kw_only=True)
class FieldingByDayOfWeek(Stats, SimpleFielding):
    type_ = [ 'byDayOfWeek' ]
    dayofweek: str
    numteams: str
    team: Union[Team, dict]
    sport: Union[Sport, dict]

@dataclass(kw_only=True)
class FieldingByDateRangeAdvanced(Stats, SimpleFielding):
    type_ = [ 'byDateRangeAdvanced' ]
    dayofweek: str
    numteams: str
    team: Union[Team, dict]
    sport: Union[Sport, dict]
    position: Union[Position, dict]

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingByMonth(Stats, SimpleFielding):
    type_ = [ 'byMonth', 'byMonthPlayoffs' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class FieldingLastXGames(Stats, SimpleFielding):
    type_ = [ 'lastXGames' ]
    numteams: int
    team: Union[Team, dict]
    sport: Union[Sport, dict]

@dataclass(kw_only=True)
class FieldingGameLog(Stats, SimpleFielding):
    type_ = [ 'gameLog' ]
    season: str
    team: Union[Team, dict]
    sport: Union[Sport, dict]
    league: Union[League, dict]
    opponent: Union[Team, dict]
    date: str
    gametype: str
    ishome: bool
    iswin: bool
    position: Union[Position, dict]
    game: Union[Game, dict]


