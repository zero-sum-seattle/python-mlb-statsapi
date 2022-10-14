from typing import Union, List
from dataclasses import dataclass

from .attributes import PlayByInningHits

@dataclass
class PlayByInning():
    """
    A class to represent a play by inning in this game.

    Attributes
    ----------
    startIndex : int
        Starting play index number, indexed with Plays.allPlays
    endIndex : int
        End play index number, indexed with Plays.allPlays
    top : List[int]
        Play indexes for top of the inning
    bottom : List[int]
        play indexes for bottom of the inning
    hits : PlayByInningHits
        Hits for the inning by home and away
    """
    startIndex: int
    endIndex: int
    top: List[int]
    bottom: List[int]
    hits: Union[PlayByInningHits, dict]

    def __post_init__(self):
        self.hits = PlayByInningHits(**self.hits)
