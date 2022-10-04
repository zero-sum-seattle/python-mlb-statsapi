from typing import Union, Dict, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.teams import Team

from mlbstatsapi.models.game.livedata.boxscore.boxscoreteams.boxscoreteaminfo import BoxScoreTeamInfo

@dataclass
class BoxScoreTeam:
    team:           Union[Team, Dict[str, Any]]
    teamStats:      Dict
    players:        Dict
    batters:        List[int]
    pitchers:       List[int]
    bench:          List[int]
    bullpen:        List[int]
    battingOrder:   List[int]
    info:           Union[List[BoxScoreTeamInfo], List[Dict[str, Any]]]
    note:           List[str]

    def __post_init__(self):
        self.team = Team(**self.team)
        self.info = [BoxScoreTeamInfo(**infos) for infos in self.info]

@dataclass
class BoxScoreTeams:
    home: Union[BoxScoreTeam, Dict[str, Any]]
    away: Union[BoxScoreTeam, Dict[str, Any]]

    def __post_init__(self):
        self.home = BoxScoreTeam(**self.home)
        self.away = BoxScoreTeam(**self.away)
