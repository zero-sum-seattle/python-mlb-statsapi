from typing import Union
from dataclasses import dataclass
from mlbstatsapi.models.people import Person

@dataclass
class GameDecisions:
    """
    A class to represent the winning and loosing pitcher for this game.
    Only used when a game is over.

    Attributes
    ----------
    winner : Person
        The winning person
    loser : Person
        The loosing person
    """
    winner: Union[Person, dict]
    loser: Union[Person, dict]

    def __post_init__(self):
        self.winner = Person(**self.winner)
        self.loser = Person(**self.loser)

@dataclass
class GameLeaders:
    """
    A class to represent this games live data leaders.
    Not sure what this data looks like since every game ive seen
    has an empty dict for each of these.

    Attributes
    ----------
    hitdistance : Dict

    hitspeed : Dict

    pitchspeed : Dict

    """
    # Dont know what this populated looks like. Every game ive seen its three empty dicts?
    hitdistance: dict
    hitspeed: dict
    pitchspeed: dict