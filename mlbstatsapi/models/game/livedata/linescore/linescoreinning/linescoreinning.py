from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass
class LinescoreInningTeamScoreInfo:
    """
    A class to represent a games Linescore

    Attributes
    ----------
    hits : int
        Team hits for this inning
    errors : int
        Team errors for this inning
    leftOnBase : int
        Player left on base for this inning
    runs : int = None
        Team runs for this inning
    """
    hits:       int
    errors:     int
    leftOnBase: int
    runs:       int = None

@dataclass
class LinescoreInning:
    """
    A class to represent a inning for a ames Linescore

    Attributes
    ----------
    num : int
        Inning number
    ordinalNum : str
        Inning ordinal
    home : LinescoreInningTeamScoreInfo
        Home team inning info
    away : LinescoreInningTeamScoreInfo
        Away team inning info
    """
    num:        int
    ordinalNum: str
    home:       Union[LinescoreInningTeamScoreInfo, Dict[str, Any]]
    away:       Union[LinescoreInningTeamScoreInfo, Dict[str, Any]]

    def __post_init__(self):
        self.home = LinescoreInningTeamScoreInfo(**self.home)
        self.away = LinescoreInningTeamScoreInfo(**self.away)
