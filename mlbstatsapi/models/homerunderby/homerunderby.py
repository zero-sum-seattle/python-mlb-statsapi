from typing import Union, List
from dataclasses import dataclass

from mlbstatsapi.models.people import Person

from .attributes import info, status, rounds


@dataclass
class Game:
    """
    A class to represent a Game.

    Attributes
    ----------
    gamepk : int
        id number of this game
    
    """
    info: Union[Info, dict]
    status: Union[Status, dict]
    rounds: List
    players: List[Union[Person, dict]]

    def __post_init__(self):
        self.info = Info(**self.info)
        self.status = Status(**self.status)
        self.rounds = [Round(**round) for round in self.rounds]
        self.players = [Person(**player) for player in self.players]