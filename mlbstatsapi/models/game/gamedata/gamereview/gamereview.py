from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class ReviewInfo:
    used:       int
    remaining:  int

@dataclass
class GameReview:
    hasChallenges:  bool
    away:           Union[ReviewInfo, Dict[str, Any]]
    home:           Union[ReviewInfo, Dict[str, Any]]

    def __post_init__(self):
        self.away = ReviewInfo(**self.away)
        self.home = ReviewInfo(**self.home)
