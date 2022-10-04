from typing import Union, Dict, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team

# @dataclass
# class LinescoreOffenseOnBase:
#     first:  Union[Person, Dict[str, Any]] = None
#     second: Union[Person, Dict[str, Any]] = None
#     third:  Union[Person, Dict[str, Any]] = None
#
#     def __post_init__(self):
#         self.first = Person(**self.first) if first else first
#         self.second = Person(**self.second) if second else second
#         self.third = Person(**self.third) if third else third

@dataclass
class LinescoreOffense:
    """
    A class to represent a games current offense

    Attributes
    ----------
    batter : Person
        Current batter
    onDeck : Person
        Current on deck batter
    inHole : Person
        Current in the hole batter
    pitcher : Person
        Who is this teams pitcher
    battingOrder : int
        Number in the batting order
    team : Team
        The team currently on offense
    """
    batter:         Union[Person, Dict[str, Any]]
    onDeck:         Union[Person, Dict[str, Any]]
    inHole:         Union[Person, Dict[str, Any]]
    pitcher:        Union[Person, Dict[str, Any]]
    battingOrder:   int
    team:           Union[Team, Dict[str, Any]]
    # onBase:         Union[LinescoreOffenseOnBase, Dict[str, Any]] = None

    def __post_init__(self):
        self.batter = Person(**self.batter)
        self.onDeck = Person(**self.onDeck)
        self.inHole = Person(**self.inHole)
        self.pitcher = Person(**self.pitcher)
        self.team = Team(**self.team)
        # self.onBase = LinescoreOffenseOnBase(**self.onBase) if onBase else onBase
