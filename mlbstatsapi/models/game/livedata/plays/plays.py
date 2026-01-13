from typing import List, Optional, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.game.livedata.plays.play import Play
from mlbstatsapi.models.game.livedata.plays.playbyinning import PlayByInning


class Plays(MLBBaseModel):
    """
    A class to represent the plays in this game.

    Attributes
    ----------
    all_plays : List[Play]
        All the plays in this game.
    current_play : Play
        The current play in this game.
    scoring_plays : List[int]
        Which plays are scoring plays, indexed with all_plays.
    plays_by_inning : List[PlayByInning]
        Plays by inning.
    """
    all_plays: List[Play] = Field(default=[], alias="allplays")
    scoring_plays: List[int] = Field(alias="scoringplays")
    plays_by_inning: List[PlayByInning] = Field(default=[], alias="playsbyinning")
    current_play: Optional[Play] = Field(default=None, alias="currentplay")

    @field_validator('current_play', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v
