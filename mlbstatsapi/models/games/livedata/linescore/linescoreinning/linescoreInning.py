from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class LinescoreInningTeamScoreInfo:
    runs:       int
    hits:       int
    errors:     int
    leftOnBase: int

@dataclass
class LinescoreInning:
    num:        int
    ordinalNum: str
    home:       Union[LinescoreInningTeamScoreInfo, Dict[str, Any]]
    away:       Union[LinescoreInningTeamScoreInfo, Dict[str, Any]]

    def __post_init__(self):
        self.home = LinescoreInningTeamScoreInfo(**home)
        self.away = LinescoreInningTeamScoreInfo(**away)
