from typing import Union, List
from dataclasses import dataclass

from mlbstatsapi.models.people import Person

from .attributes import Info, Status, Round


@dataclass
class Homerunderby:
    """
    A class representing a homerun derby

    Attributes
    ----------
    info : Info
        An object containing information about the game.
    status : Status
        An object containing the status of the game.
    rounds : Round
        A list of Round objects representing the rounds in the game.
    players : List[Person]
        A list of objects containing the data for the players in the game.
    """
    info: Union[Info, dict]
    status: Union[Status, dict]
    rounds: List[Round]
    players: List[Union[Person, dict]]

    def __post_init__(self):
        self.info = Info(**self.info)
        self.status = Status(**self.status)
        self.rounds = [Round(**round) for round in self.rounds]
        
        player_list = []

        for player in self.players:
            if 'stats' in player:
                player.pop('stats')
            player_list.append(Person(**player))

        self.players = player_list