from typing import Union, List
from dataclasses import dataclass, field

from .attributes import BoxScoreTeams, BoxScoreOffical, BoxScoreVL

@dataclass
class BoxScore:
    """
    A class to represent this games boxscore

    Attributes
    ----------
    teams : BoxScoreTeams
        Box score data for each team
    officials : List[BoxScoreOffical]
        The officials for this game
    info : List[BoxScoreVL]
        Box score information
    pitchingnotes : List[str]
        Pitching notes for this game
    """
    teams: Union[BoxScoreTeams, dict]
    officials: Union[List[BoxScoreOffical], List[dict]]
    info: Union[List[BoxScoreVL], List[dict]]
    pitchingnotes: List[str]

    def __post_init__(self):
        self.teams = BoxScoreTeams(**self.teams)
        self.officials = [BoxScoreOffical(**official) for official in self.officials]
        self.info = [BoxScoreVL(**infos) for infos in self.info]
