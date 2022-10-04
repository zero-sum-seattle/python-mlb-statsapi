from typing import Union, Dict, Any
from dataclasses import dataclass, field

@dataclass
class LinescoreTeamsScoreInfo:
    """
    A class to represent current inning score info for a team

    Attributes
    ----------
    runs : int
        Current inning teams runs
    hits : int
        Current inning teams hits
    errors : int
        Current inning teams Errors
    leftOnBase : int
        Current inning players left on base
    """
    runs:       int
    hits:       int
    errors:     int
    leftOnBase: int

@dataclass
class LinescoreTeams:
    """
    A class to represent home and away teams in the linescore

    Attributes
    ----------
    home : LinescoreTeamsScoreInfo
        Home team current inning info
    away : LinescoreTeamsScoreInfo
        Away team current inning info
    """
    home: Union[LinescoreTeamsScoreInfo, Dict[str, Any]]
    away: Union[LinescoreTeamsScoreInfo, Dict[str, Any]]

    def __post_init__(self):
        self.home = LinescoreTeamsScoreInfo(**self.home)
        self.away = LinescoreTeamsScoreInfo(**self.away)
