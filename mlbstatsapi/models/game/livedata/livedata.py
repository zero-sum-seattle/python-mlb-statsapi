from typing import Union, Optional
from dataclasses import dataclass, field

from mlbstatsapi.models.game.livedata.plays import Plays
from mlbstatsapi.models.game.livedata.linescore import Linescore
from mlbstatsapi.models.game.livedata.boxscore import BoxScore

from .attributes import GameLeaders, GameDecisions


@dataclass(repr=False)
class LiveData:
    """
    A class to represent this games live data.

    Attributes
    ----------
    plays : Plays
        Has the plays for this game
    linescore : Linescore
        This games linescore
    boxscore : BoxScore
        This games boxscore
    leaders : GameLeaders
        The data leaders for this game
    decisions : GameDecisions = None
        Decisions for this game, Ie a winner or a loser
    """
    plays: Union[Plays, dict]
    boxscore: Union[BoxScore, dict]
    leaders: Union[GameLeaders, dict]
    decisions: Optional[Union[GameDecisions, dict]] = field(default_factory=dict)
    linescore: Union[Linescore, dict] = field(default_factory=dict)


    def __post_init__(self):
        self.plays = Plays(**self.plays)
        self.linescore = Linescore(**self.linescore) if self.linescore else self.linescore
        self.boxscore = BoxScore(**self.boxscore)
        self.decisions = GameDecisions(**self.decisions) if self.decisions else self.decisions
        self.leaders = GameLeaders(**self.leaders)

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))