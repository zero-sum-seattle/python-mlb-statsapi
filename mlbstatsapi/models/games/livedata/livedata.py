from typing import Union, Dict, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays import Plays
from mlbstatsapi.models.game.livedata.linescore import Linescore
from mlbstatsapi.models.game.livedata.boxscore import BoxScore

@dataclass
class LiveDataDecisions:
    winner: Union[Person, Dict[str, Any]]
    loser:  Union[Person, Dict[str, Any]]

    def __post_init__(self):
        self.winner = Person(**winner)
        self.loser = Person(**loser)

@dataclass
class LiveDataLeaders:
    # Dont know what this populated looks like. Every game ive seen its three empty dicts?
    hitDistance: Dict
    hitSpeed: Dict
    pitchSpeed: Dict

class LiveData:
    plays:      Union[Plays, Dict[str, Any]]
    linescore:  Union[Linescore, Dict[str, Any]]
    boxscore:   Union[BoxScore, Dict[str, Any]]
    decisions:  Union[LiveDataDecisions, Dict[str, Any]] = None
    leaders:    Union[LiveDataLeaders, Dict[str, Any]]

    def __post_init__(self):
        self.plays = Plays(**plays)
        self.linescore = Linescore(**linescore)
        self.boxscore = BoxScore(**boxscore)
        self.decisions = LiveDataDecisions(**decisions) if decisions else decisions
        self.leaders = LiveDataLeaders(**leaders)
