from typing import Union, Dict, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.teams import Team

from mlbstatsapi.models.game.livedata.boxscore.boxscoreteams.boxscoreteaminfo import BoxScoreTeamInfo

@dataclass
class BoxScoreTeam:
    """
    A class to represent the boxscore team

    Attributes
    ----------
    team : Team
        This team
    teamStats : Dict
        Team stats
    players : Dict
        Players on team
    batters : List[int]
        List of batters playerid for this team
    pitchers : List[int]
        List of pitcher playerid for this team
    bench : List[int]
        List of bench playerid for this team
    bullpen : List[int]
        Bullpen list of playerid
    battingOrder : List[int]
        Batting order for this team as a list of playerid
    info : List[BoxScoreTeamInfo]
        Batting and fielding info for team
    note : List[str]
        Team notes
    """
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
    """
    A class to represent the boxscore home and away teams

    Attributes
    ----------
    home: BoxScoreTeam
        Home team boxscore information
    away: BoxScoreTeam
        Away team boxscore information
    """
    home: Union[BoxScoreTeam, Dict[str, Any]]
    away: Union[BoxScoreTeam, Dict[str, Any]]

    def __post_init__(self):
        self.home = BoxScoreTeam(**self.home)
        self.away = BoxScoreTeam(**self.away)
