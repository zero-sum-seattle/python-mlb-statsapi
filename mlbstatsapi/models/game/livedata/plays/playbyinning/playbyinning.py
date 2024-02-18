from typing import Union, List
from pydantic import BaseModel
from .attributes import PlayByInningHits

class PlayByInning(BaseModel):
    """Represents a play by inning in a game.

    Attributes:
        startIndex (int): Starting play index number, indexed with `Plays.allPlays`.
        endIndex (int): End play index number, indexed with `Plays.allPlays`.
        top (List[int]): Play indexes for the top of the inning.
        bottom (List[int]): Play indexes for the bottom of the inning.
        hits (PlayByInningHits): Hits for the inning by home and away.
    """
    startIndex: int
    endIndex: int
    top: List[int]
    bottom: List[int]
    hits: PlayByInningHits


