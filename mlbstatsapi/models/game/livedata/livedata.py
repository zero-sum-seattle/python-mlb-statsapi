from typing import Union, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.people import Person

from mlbstatsapi.models.game.livedata.plays import Plays
from mlbstatsapi.models.game.livedata.linescore import Linescore
from mlbstatsapi.models.game.livedata.boxscore import BoxScore

@dataclass
class LiveDataDecisions:
    winner: Union[Person, Dict[str, Any]]
    loser:  Union[Person, Dict[str, Any]]

    def __post_init__(self):
        self.winner = Person(**self.winner)
        self.loser = Person(**self.loser)

@dataclass
class LiveDataLeaders:
    # Dont know what this populated looks like. Every game ive seen its three empty dicts?
    hitDistance: Dict
    hitSpeed: Dict
    pitchSpeed: Dict

@dataclass
class LiveData:
    plays:      Union[Plays, Dict[str, Any]]
    linescore:  Union[Linescore, Dict[str, Any]]
    boxscore:   Union[BoxScore, Dict[str, Any]]
    leaders:    Union[LiveDataLeaders, Dict[str, Any]]
    decisions:  Union[LiveDataDecisions, Dict[str, Any]] = None

    def __post_init__(self):
        self.plays = Plays(**self.plays)
        self.linescore = Linescore(**self.linescore)
        self.boxscore = BoxScore(**self.boxscore)
        self.decisions = LiveDataDecisions(**self.decisions) if self.decisions else self.decisions
        self.leaders = LiveDataLeaders(**self.leaders)
