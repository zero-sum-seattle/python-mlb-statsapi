from typing import Union, Dict, Any
from dataclasses import dataclass, field

@dataclass
class LinescoreTeamsScoreInfo:
    runs:       int
    hits:       int
    errors:     int
    leftOnBase: int

@dataclass
class LinescoreTeams:
    home: Union[LinescoreTeamsScoreInfo, Dict[str, Any]]
    away: Union[LinescoreTeamsScoreInfo, Dict[str, Any]]

    def __post_init__(self):
        self.home = LinescoreTeamsScoreInfo(**self.home)
        self.away = LinescoreTeamsScoreInfo(**self.away)
