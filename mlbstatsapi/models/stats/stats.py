from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.game import Game

@dataclass(kw_only=True)
class Stats:
    """
    Base class for stats

    Attributes
    ----------
    gametype : str
        type of game for stat
    numteams : str
        number of teams inolved in this stat
    season : str
        season of the stat
    dayofweek : str
        day of the week of the stat
    iswin : bool
        bool to hold if stat is a win
    ishome : bool
        bool to hold if stat is at home
    date : str
        date of game
    group : str 
        type of stat group
    stat_group : str
        type of the stat group
    stat_type : str
        type of the stat 
    """
    team: Optional[Union[Team, dict]] = field(default_factory=dict)
    player: Optional[Union[Person, dict]] = field(default_factory=dict)
    league: Optional[Union[League, dict]] = field(default_factory=dict)
    sport: Optional[Union[Sport, dict]] = field(default_factory=dict)
    position: Optional[Union[Position, dict]] = field(default_factory=dict)
    game: Optional[Union[Game, dict]] = field(default_factory=dict)
    opponent: Optional[Union[Team, dict]] = field(default_factory=dict)
    gametype: Optional[str] = None
    numteams: Optional[str] = None
    season: Optional[str] = None
    dayofweek: Optional[str] = None
    iswin: Optional[bool] = None
    ishome: Optional[bool] = None
    date: Optional[str] = None
    group: Optional[str] = None
    stat_group: str
    stat_type: str

    def __post_init__(self):
        self.team = Team(**self.team) if self.team else self.team
        self.player = Person(**self.player) if self.player else self.player
        self.league = League(**self.league) if self.league else self.league
        self.position = Position(**self.position) if self.position else self.position
        self.sport = Sport(**self.sport) if self.sport else self.sport
        self.opponent = Team(**self.opponent) if self.opponent else self.opponent

@dataclass
class ExpectedStatistics(Stats):
    """
    A class to represent a excepted statistics statType: expectedStatistics.

    Attributes
    ----------
    avg : str
    slg : str
    woba : str
    wobaCon : str
    rank : int
    """
    type_ = [ 'expectedStatistics' ]
    avg: str
    slg: str
    woba: str
    wobacon: str
    rank: int