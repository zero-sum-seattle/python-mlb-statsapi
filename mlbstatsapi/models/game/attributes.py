from typing import List
from dataclasses import dataclass

@dataclass
class MetaData:
    """
    A class to represent a Game's metaData.

    Attributes
    ----------
    wait : int
        No idea what this wait signifies
    timeStamp : str
        The timeStamp
    gameEvents : List[str]
        Current game events for this game
    logicalEvents : List[str]
        Current logical events for this game
    """
    wait: int
    timestamp: str
    gameevents: List[str]
    logicalevents: List[str]