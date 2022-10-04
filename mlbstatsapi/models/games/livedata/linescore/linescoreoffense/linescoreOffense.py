from typing import Union, Dict, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.person import Person
from mlbstatsapi.models.team import Team

@dataclass
class LinescoreOffenseOnBase:
    first:  Union[Person, Dict[str, Any]] = None
    second: Union[Person, Dict[str, Any]] = None
    third:  Union[Person, Dict[str, Any]] = None

    def __post_init__(self):
        self.first = Person(**first) if first else first
        self.second = Person(**second) if second else second
        self.third = Person(**third) if third else third

@dataclass
class LinescoreOffense:
    batter:         Union[Person, Dict[str, Any]]
    onDeck:         Union[Person, Dict[str, Any]]
    inHole:         Union[Person, Dict[str, Any]]
    pitcher:        Union[Person, Dict[str, Any]]
    battingOrder:   int
    team:           Union[Team, Dict[str, Any]]
    onBase:         Union[LinescoreOffenseOnBase, Dict[str, Any]] = None

    def __post_init__(self):
        self.batter = Person(**batter)
        self.onDeck = Person(**onDeck)
        self.inHole = Person(**inHole)
        self.pitcher = Person(**pitcher)
        self.team = Team(**team)
        self.onBase = LinescoreOffenseOnBase(**onBase) if onBase else onBase
