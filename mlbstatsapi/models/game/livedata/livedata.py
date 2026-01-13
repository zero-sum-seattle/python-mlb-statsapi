from typing import Optional, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.game.livedata.plays import Plays
from mlbstatsapi.models.game.livedata.linescore import Linescore
from mlbstatsapi.models.game.livedata.boxscore import BoxScore
from .attributes import GameLeaders, GameDecisions


class LiveData(MLBBaseModel):
    """
    A class to represent this game's live data.

    Attributes
    ----------
    plays : Plays
        Has the plays for this game.
    linescore : Linescore
        This game's linescore.
    boxscore : BoxScore
        This game's boxscore.
    leaders : GameLeaders
        The data leaders for this game.
    decisions : GameDecisions
        Decisions for this game (i.e., winner or loser).
    """
    plays: Plays
    boxscore: BoxScore
    leaders: GameLeaders
    decisions: Optional[GameDecisions] = None
    linescore: Optional[Linescore] = None

    @field_validator('decisions', 'linescore', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v
