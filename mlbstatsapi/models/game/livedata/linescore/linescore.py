from typing import Union, List, Optional
from dataclasses import dataclass

from .attributes import LinescoreInning
from .attributes import LinescoreTeams
from .attributes import LinescoreDefense
from .attributes import LinescoreOffense

@dataclass(repr=False)
class Linescore:
    """
    A class to represent a games Linescore

    Attributes
    ----------
    currentinning : int
        The games current inning
    currentinningordinal : str
        This innings ordinal
    inningstate : str
        What state this inning is in
    inninghalf : str
        WHich half of the inning are we in
    istopinning : bool
        Is this the top of the inning
    scheduledinnings : int
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

    scheduledinnings: int
    innings: Union[List[LinescoreInning], List[dict]]
    teams: Union[LinescoreTeams, dict]
    defense: Union[LinescoreDefense, dict]
    offense: Union[LinescoreOffense, dict]
    balls: Optional[int] = None
    strikes: Optional[int] = None
    outs: Optional[int] = None
    note: Optional[str] = None
    currentinning: Optional[int] = None
    currentinningordinal: Optional[str] = None
    inningstate: Optional[str] = None
    inninghalf: Optional[str] = None
    istopinning: Optional[bool] = None

    def __post_init__(self):
        self.innings = [LinescoreInning(**inning) for inning in self.innings]
        self.teams = LinescoreTeams(**self.teams)
        self.defense = LinescoreDefense(**self.defense)
        self.offense = LinescoreOffense(**self.offense)

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))