from typing import Union, Optional
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays import Plays
from mlbstatsapi.models.game.livedata.linescore import Linescore
from mlbstatsapi.models.game.livedata.boxscore import BoxScore

from .attributes import GameLeaders, GameDecisions

@dataclass
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
    leaders : LiveDataLeaders
        The data leaders for this game
    decisions : LiveDataDecisions = None
        Decisions for this game, Ie a winner or a loosers
    """
    plays: Union[Plays, dict]
    linescore: Union[Linescore, dict]
    boxscore: Union[BoxScore, dict]
    leaders: Union[GameLeaders, dict]
    decisions: Optional[Union[GameDecisions, dict]] = None

    def __post_init__(self):
        self.plays = Plays(**self.plays)
        self.linescore = Linescore(**self.linescore)
        self.boxscore = BoxScore(**self.boxscore)
        self.decisions = GameDecisions(**self.decisions) if self.decisions else self.decisions
        self.leaders = GameLeaders(**self.leaders)
