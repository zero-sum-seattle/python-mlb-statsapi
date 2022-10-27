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
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding advanced season 
    numteams : str
        the number of teams for the fielding season
    """
    type_ = ['seasonAdvanced', 'statsSingleSeasonAdvanced' ]
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class SeasonFielding(Stats, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding yearByYear 
    numteams : str
        the number of teams for the fielding season
    """
    type_ = [ 'season', 'statsSingleSeason' ]
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingCareer(Stats, SimpleFielding):
    """
    A class to represent a fielding career statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding yearByYear 
    numteams : str
        the number of teams for the fielding season
    """
    type_ = [ 'careerRegularSeason' ]
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position    

@dataclass(kw_only=True)
class FieldingCareerPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding career playoff statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding yearByYear 
    numteams : str
        the number of teams for the fielding season
    """
    type_ = [ 'careerPlayoffs' ]
    gametype: Optional[str] = None
    position: Optional[Union[Position, dict]] = None
    numteams: Optional[str] = None

    def __post_init__(self):
        self.position = Position(**self.position) if self.position else self.position

@dataclass(kw_only=True)
class FieldingHAA(Stats, SimpleFielding):
    """
    A class to represent a fielding homeAndAway statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding yearByYear 
    numteams : str
        the number of teams for the fielding season
    """
    type_ = [ 'homeAndAway' ]
    ishome: bool

@dataclass(kw_only=True)
class FieldingHAAPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding homeAndAwayPlayoffs statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching season
    """
    type_ = [ 'homeAndAwayPlayoffs' ]
    ishome: bool

@dataclass(kw_only=True)
class FieldingYBY(Stats, SimpleFielding):
    """
    A class to represent a fielding yearByYear statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the pitching yearByYear 
    numteams : str
        the number of teams for the pitching season
    """
    type_ = [ 'yearByYear' ]
    team: Union[Team, dict]

@dataclass(kw_only=True)
class FieldingYBYAdvanced(Stats, SimpleFielding):
    """
    A class to represent a fielding yearByYearAdvanced statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding yearByYear 
    numteams : str
        the number of teams for the fielding season
    """
    type_ = [ 'yearByYearAdvanced']
    team: Union[Team, dict]

@dataclass(kw_only=True)
class FieldingYBYPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding season statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding yearByYearPlayoffs 
    numteams : str
        the number of teams for the fielding season
    """
    type_ = [ 'yearByYearPlayoffs' ]
    team: Union[Team, dict]

@dataclass(kw_only=True)
class FieldingWL(Stats, SimpleFielding):
    """
    A class to represent a fielding winLoss statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding winLoss 
    numteams : str
        the number of teams for the fielding season
    """
    type_ = ['winLoss' ]
    iswin: bool

@dataclass(kw_only=True)
class FieldingWLPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding winLossPlayoffs statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding winLossPlayoffs 
    numteams : str
        the number of teams for the fielding winLossPlayoffs
    """
    type_ = [ 'winLossPlayoffs' ]
    iswin: bool

@dataclass(kw_only=True)
class FieldingByDayOfWeek(Stats, SimpleFielding):
    """
    A class to represent a fielding byDayOfWeek statistic

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding byDayOfWeek 
    numteams : str
        the number of teams for the fielding byDayOfWeek
    """
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
    """
    A class to represent a fielding byMonth stat

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding byMonth 
    numteams : str
        the number of teams for the fielding byMonth
    """
    type_ = [ 'byMonth' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class FieldingByMonthPlayoffs(Stats, SimpleFielding):
    """
    A class to represent a fielding byMonthPlayoffs stat

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding byMonthPlayoffs 
    numteams : str
        the number of teams for the fielding byMonthPlayoffs
    """
    type_ = [ 'byMonthPlayoffs' ]
    month: int
    numteams: int

@dataclass(kw_only=True)
class FieldingLastXGames(Stats, SimpleFielding):
    """
    A class to represent a fielding lastXGames stat

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding lastXGames 
    numteams : str
        the number of teams for the fielding lastXGames
    """
    type_ = [ 'lastXGames' ]
    numteams: int

@dataclass(kw_only=True)
class FieldingGameLog(Stats, SimpleFielding):
    """
    A class to represent a fielding gameLog stats

    Attributes
    ----------
    gametype : Team
        the gametype code of the fielding gameLog 
    numteams : str
        the number of teams for the fielding gameLog
    """
    type_ = [ 'gameLog' ]
    opponent: Union[Team, dict]
    date: str
    gametype: str
    ishome: bool
    iswin: bool
    position: Union[Position, dict]
    game: Union[Game, dict]


