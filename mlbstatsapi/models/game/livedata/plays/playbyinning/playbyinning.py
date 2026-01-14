from typing import List
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import PlayByInningHits


class PlayByInning(MLBBaseModel):
    """
    A class to represent a play by inning in this game.

    Attributes
    ----------
    start_index : int
        Starting play index number, indexed with Plays.all_plays.
    end_index : int
        End play index number, indexed with Plays.all_plays.
    top : List[int]
        Play indexes for top of the inning.
    bottom : List[int]
        Play indexes for bottom of the inning.
    hits : PlayByInningHits
        Hits for the inning by home and away.
    """
    start_index: int = Field(alias="startIndex")
    end_index: int = Field(alias="endIndex")
    top: List[int]
    bottom: List[int]
    hits: PlayByInningHits
