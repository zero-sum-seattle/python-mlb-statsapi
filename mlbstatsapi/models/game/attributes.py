from typing import List
from pydantic import BaseModel


class MetaData(BaseModel):
    """Represents a game's metaData.

    Attributes:
        wait (int): No idea what this wait signifies.
        timeStamp (str): The timeStamp of the metaData.
        gameEvents (List[str]): Current game events for this game.
        logicalEvents (List[str]): Current logical events for this game.
    """
    wait: int
    timeStamp: str
    gameEvents: List[str]
    logicalEvents: List[str]