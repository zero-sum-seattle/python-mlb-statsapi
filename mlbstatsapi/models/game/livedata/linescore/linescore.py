from typing import Union, List
from dataclasses import dataclass

# from mlbstatsapi.models.game.livedata.linescore.linescoreinning import LinescoreInning
# from mlbstatsapi.models.game.livedata.linescore.linescoreteams import LinescoreTeams
# from mlbstatsapi.models.game.livedata.linescore.linescoreoffense import LinescoreOffense

from .attributes import LinescoreInning
from .attributes import LinescoreTeams
from .attributes import LinescoreDefense
from .attributes import LinescoreOffense

@dataclass
class Linescore:
    """
    A class to represent a games Linescore

    Attributes
    ----------
    currentInning : int
        The games current inning
    currentInningOrdinal : str
        This innings ordinal
    inningState : str
        What state this inning is in
    inningHalf : str
        WHich half of the inning are we in
    isTopInning : bool
        Is this the top of the inning
    scheduledInnings : int
        How many innings are scheduled for this game
    innings : List[LinescoreInning]
        Data on each inning
    teams : LinescoreTeams
        Line score data on our teams
    defense : LinescoreDefense
        Current defense
    offense : LinescoreOffense
        Current offense
    balls : int
        current count balls
    strikes : int
        current count strikes
    outs : int
        current count outs
    """
    currentInning: int
    currentInningOrdinal: str
    inningState: str
    inningHalf: str
    isTopInning: bool
    scheduledInnings: int
    innings: Union[List[LinescoreInning], List[dict]]
    teams: Union[LinescoreTeams, dict]
    defense: Union[LinescoreDefense, dict]
    offense: Union[LinescoreOffense, dict]
    balls: int
    strikes: int
    outs: int

    def __post_init__(self):
        self.innings = [LinescoreInning(**inning) for inning in self.innings]
        self.teams = LinescoreTeams(**self.teams)
        self.defense = LinescoreDefense(**self.defense)
        self.offense = LinescoreOffense(**self.offense)
