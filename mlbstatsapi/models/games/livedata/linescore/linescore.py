from typing import Union, Dict, List, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.person import Person

from mlbstatsapi.models.game.livedata.linescore.linescoreinning import LinescoreInning
from mlbstatsapi.models.game.livedata.linescore.linescoreteams import LinescoreTeams
from mlbstatsapi.models.game.livedata.linescore.linescoreoffense import LinescoreOffense

@dataclass
class LinescoreDefense:
    pitcher:        Union[Person, Dict[str, Any]]
    catcher:        Union[Person, Dict[str, Any]]
    first:          Union[Person, Dict[str, Any]]
    second:         Union[Person, Dict[str, Any]]
    third:          Union[Person, Dict[str, Any]]
    shortstop:      Union[Person, Dict[str, Any]]
    left:           Union[Person, Dict[str, Any]]
    center:         Union[Person, Dict[str, Any]]
    right:          Union[Person, Dict[str, Any]]
    batter:         Union[Person, Dict[str, Any]]
    onDeck:         Union[Person, Dict[str, Any]]
    inHole:         Union[Person, Dict[str, Any]]
    battingOrder:   int
    team:           Union[Team, Dict[str, Any]]

    def __post_init__(self):
        self.pitcher = Person(**pitcher)
        self.catcher = Person(**catcher)
        self.first = Person(**first)
        self.second = Person(**second)
        self.third = Person(**third)
        self.shortstop = Person(**shortstop)
        self.left = Person(**left)
        self.center = Person(**center)
        self.right = Person(**right)
        self.batter = Person(**batter)
        self.onDeck = Person(**onDeck)
        self.inHole = Person(**inHole)
        self.team = Team(**team)

@dataclass
class Linescore:
    currentInning:          int
    currentInningOrdinal:   str
    inningState:            str
    inningHalf:             str
    isTopInning:            bool
    scheduledInnings:       int
    innings:                Union[List[LinescoreInning], List[Dict[str, Any]]]
    teams:                  Union[LinescoreTeams, Dict[str, Any]]
    defense:                Union[LinescoreDefense, Dict[str, Any]]
    offense:                Union[LinescoreOffense, Dict[str, Any]]
    balls:                  int
    strikes:                int
    outs:                   int

    def __post_init__(self):
        self.innings = [LinescoreInning(**inning) for inning in innings]
        self.teams = LinescoreTeams(**teams)
        self.defense = LinescoreDefense(**defense)
        self.offense = LinescoreOffense(**offense)
