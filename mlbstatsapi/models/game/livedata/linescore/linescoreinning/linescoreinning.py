from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class LinescoreInningTeamScoreInfo:
    hits:       int
    errors:     int
    leftOnBase: int
    runs:       int = None

@dataclass
class LinescoreInning:
    num:        int
    ordinalNum: str
    home:       Union[LinescoreInningTeamScoreInfo, Dict[str, Any]]
    away:       Union[LinescoreInningTeamScoreInfo, Dict[str, Any]]

    def __post_init__(self):
        self.home = LinescoreInningTeamScoreInfo(**self.home)
        self.away = LinescoreInningTeamScoreInfo(**self.away)
