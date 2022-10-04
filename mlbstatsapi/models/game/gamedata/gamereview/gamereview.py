from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class ReviewInfo:
    """
    A class to represent reviewInfo for each team in this game.

    Attributes
    ----------
    used : int
        How many challenges used
    remaining : int
        How many challenges are remaining
    """
    used:       int
    remaining:  int

@dataclass
class GameReview:
    """
    A class to represent the Game Reviews for this game.

    Attributes
    ----------
    hasChallenges : bool
        If their are challenges
    away : ReviewInfo
        Away team review info
    home : ReviewInfo
        Home team review info
    """
    hasChallenges:  bool
    away:           Union[ReviewInfo, Dict[str, Any]]
    home:           Union[ReviewInfo, Dict[str, Any]]

    def __post_init__(self):
        self.away = ReviewInfo(**self.away)
        self.home = ReviewInfo(**self.home)
