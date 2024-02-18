from typing import Union, Optional
from pydantic import BaseModel

from mlbstatsapi.models.game.livedata.plays import Plays
from mlbstatsapi.models.game.livedata.linescore import Linescore
from mlbstatsapi.models.game.livedata.boxscore import BoxScore

from .attributes import GameLeaders, GameDecisions


class LiveData(BaseModel):
    """Represents live data for a game.

    Attributes:
        plays (Plays): Contains the plays for this game.
        linescore (Optional[Linescore]): The game's linescore. Defaults to None.
        boxscore (BoxScore): The game's boxscore.
        leaders (GameLeaders): The data leaders for this game.
        decisions (Optional[GameDecisions]): Decisions for this game, such as a winner or a loser. Defaults to None.
    """
    plays: Plays
    boxscore: BoxScore
    leaders: GameLeaders
    decisions: Optional[GameDecisions] = None
    linescore: Optional[Linescore] = None
