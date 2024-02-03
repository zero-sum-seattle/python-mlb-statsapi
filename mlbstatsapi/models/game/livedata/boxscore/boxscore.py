from typing import Union, List, Any, Optional
from dataclasses import dataclass, field

from .attributes import BoxScoreTeams, BoxScoreOffical, BoxScoreVL, PlayersDictPerson



@dataclass
class TopPerformer:
    """
    A class to represent this games topperformer

    Attributes
    ----------
    player : Player
        Player 
    type : str
        The officials for this game
    gamescore : int
        gamescore
    hittinggamescore : int
        hitting game score
    """
    player: Union[PlayersDictPerson, dict]
    type: str
    gamescore: int
    hittinggamescore: Optional[int] = None
    pitchinggamescore: Optional[int] = None
    
    def __post_init__(self):
        self.player = PlayersDictPerson(**self.player)

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
    topperformers: Optional[List[Union[TopPerformer, dict]]] = field(default_factory=list)

    def __post_init__(self):
        self.teams = BoxScoreTeams(**self.teams)
        self.officials = [BoxScoreOffical(**official) for official in self.officials]
        self.info = [BoxScoreVL(**infos) for infos in self.info]
        self.topperformers = [TopPerformer(**topperformer) for topperformer in self.topperformers]


