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
class SeasonFieldingAdvanced(Stats, SimpleFielding):
    type_ = ['seasonAdvanced', 'statsSingleSeasonAdvanced' ]
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None
    league: Optional[Union[League, dict]] = None
    sport: Optional[Union[Sport, dict]] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class SeasonFielding(Stats, SimpleFielding):
    type_ = [ 'season', 'statsSingleSeason' ]
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None
    league: Optional[Union[League, dict]] = None
    sport: Optional[Union[Sport, dict]] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingCareer(Stats, SimpleFielding):
    type_ = [ 'careerRegularSeason', 'careerPlayoffs' ]
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None
    league: Optional[Union[League, dict]] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position    

@dataclass(kw_only=True)
class FieldingCareerPlayoffs(Stats, SimpleFielding):
    type_ = [ 'careerPlayoffs' ]
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None
    league: Optional[Union[League, dict]] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingHAA(Stats, SimpleFielding):
    type_ = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class FieldingHAAPlayoffs(Stats, SimpleFielding):
    type_ = [ 'homeAndAwayPlayoffs' ]
    ishome: bool

@dataclass(kw_only=True)
class FieldingYBY(Stats, SimpleFielding):
    type_ = [ 'yearByYear' ]
    team: Union[Team, dict]

@dataclass(kw_only=True)
class FieldingYBYAdvanced(Stats, SimpleFielding):
    type_ = [ 'yearByYearAdvanced']
    team: Union[Team, dict]

@dataclass(kw_only=True)
class FieldingYBYPlayoffs(Stats, SimpleFielding):
    type_ = [ 'yearByYearPlayoffs' ]
    team: Union[Team, dict]

@dataclass(kw_only=True)
class FieldingWL(Stats, SimpleFielding):
    type_ = ['winLoss' ]
    iswin: bool

@dataclass(kw_only=True)
class FieldingWLPlayoffs(Stats, SimpleFielding):
    type_ = [ 'winLossPlayoffs' ]
    iswin: bool

@dataclass(kw_only=True)
class FieldingByDayOfWeek(Stats, SimpleFielding):
    type_ = [ 'byDayOfWeek' ]
    dayofweek: str
    numteams: str

@dataclass(kw_only=True)
class FieldingByDateRangeAdvanced(Stats, SimpleFielding):
    type_ = [ 'byDateRangeAdvanced' ]
    dayofweek: str
    numteams: str
    position: Union[Position, dict]

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingByMonth(Stats, SimpleFielding):
    type_ = [ 'byMonth' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class FieldingByMonthPlayoffs(Stats, SimpleFielding):
    type_ = [ 'byMonthPlayoffs' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class FieldingByMonthPlayoffs(Stats, SimpleFielding):
    type_ = [ 'byMonthPlayoffs' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class FieldingLastXGames(Stats, SimpleFielding):
    type_ = [ 'lastXGames' ]
    numteams: int

@dataclass(kw_only=True)
class FieldingGameLog(Stats, SimpleFielding):
    type_ = [ 'gameLog' ]
    league: Union[League, dict]
    opponent: Union[Team, dict]
    date: str
    gametype: str
    ishome: bool
    iswin: bool
    position: Union[Position, dict]
    game: Union[Game, dict]


