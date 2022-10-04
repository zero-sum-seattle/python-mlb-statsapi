from typing import Union, Dict, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.team import Team

from .boxScoreVL import BoxScoreVL

@dataclass
class BoxScoreTeamsTeamInfoGroup:
    title:      str
    fieldList:  Union[List[BoxScoreVL], List[Dict[str, Any]]]

    def __post_init__(self):
        self.fieldList = [BoxScoreVL(**fieldLists) for fieldLists in fieldList]

@dataclass
class BoxScoreTeamsTeam:
    team:           Union[Team, Dict[str, Any]]
    teamStats:      Dict
    players:        Dict
    batters:        List[int]
    pitchers:       List[int]
    bench:          List[int]
    bullpen:        List[int]
    battingOrder:   List[int]
    info:           Union[List[BoxScoreTeamsTeamInfoGroup], List[Dict[str, Any]]]
    note:           List[str]

    def __post_init__(self):
        self.team = Team(**team)
        self.info = [BoxScoreTeamsTeamInfoGroup(**infos) for infos in info]

@dataclass
class BoxScoreTeams:
    home: Union[BoxScoreTeam, Dict[str, Any]]
    away: Union[BoxScoreTeam, Dict[str, Any]]

    def __init__(self, home: Dict, away: Dict, **kwargs) -> None:
        self.home = BoxScoreTeam(**home)
        self.away = BoxScoreTeam(**away)
