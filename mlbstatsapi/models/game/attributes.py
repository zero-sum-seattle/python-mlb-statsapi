from typing import List
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel


class MetaData(MLBBaseModel):
    """
    A class to represent a Game's metadata.

    Attributes
    ----------
    wait : int
        Wait value.
    timestamp : str
        The timestamp.
    game_events : List[str]
        Current game events for this game.
    logical_events : List[str]
        Current logical events for this game.
    """
    wait: int
    timestamp: str
    game_events: List[str] = Field(alias="gameEvents")
    logical_events: List[str] = Field(alias="logicalEvents")
