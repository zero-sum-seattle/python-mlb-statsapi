from typing import Union, Dict, List, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.person import Person

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
