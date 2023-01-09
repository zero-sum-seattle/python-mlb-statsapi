from typing import Union, Optional
from dataclasses import dataclass
from mlbstatsapi.models.people import Person


@dataclass(repr=False)
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
    save: Optional[Union[Person, dict]] = None

    def __post_init__(self):
        self.winner = Person(**self.winner)
        self.loser = Person(**self.loser)
        self.save = Person(**self.save) if self.save else self.save

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass
class GameLeaders:
    """
    A class to represent this games live data leaders.
    Not sure what this data looks like since every game ive seen
    has an empty dict for each of these.

    Attributes
    ----------
    hitdistance : dict
        hit distance
    hitspeed : dict
        hit speed
    pitchspeed : dict
        pitch speed
    """
    # Dont know what this populated looks like. Every game ive seen its three empty dicts?
    hitdistance: dict
    hitspeed: dict
    pitchspeed: dict