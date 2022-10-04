from typing import Union, Dict, List, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team

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
        self.pitcher = Person(**self.pitcher)
        self.catcher = Person(**self.catcher)
        self.first = Person(**self.first)
        self.second = Person(**self.second)
        self.third = Person(**self.third)
        self.shortstop = Person(**self.shortstop)
        self.left = Person(**self.left)
        self.center = Person(**self.center)
        self.right = Person(**self.right)
        self.batter = Person(**self.batter)
        self.onDeck = Person(**self.onDeck)
        self.inHole = Person(**self.inHole)
        self.team = Team(**self.team)

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
        self.innings = [LinescoreInning(**inning) for inning in self.innings]
        self.teams = LinescoreTeams(**self.teams)
        self.defense = LinescoreDefense(**self.defense)
        self.offense = LinescoreOffense(**self.offense)
