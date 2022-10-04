from typing import Union, Dict, Any
from dataclasses import dataclass, field

from linescoreTeams_models.linescoreTeamScore import LinescoreTeamScoreInfo

@dataclass
class LinescoreTeams:
    home: Union[LinescoreTeamScoreInfo, Dict[str, Any]]
    away: Union[LinescoreTeamScoreInfo, Dict[str, Any]]

    def __post_init__(self):
        self.home = LinescoreTeamScoreInfo(**home)
        self.away = LinescoreTeamScoreInfo(**away)
