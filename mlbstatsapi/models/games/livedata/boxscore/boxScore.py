from typing import Union, Dict, List, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.person import Person

from mlbstatsapi.models.game.livedata.boxscore.boxscoreteams import BoxScoreTeams
from mlbstatsapi.models.game.livedata.boxscore.boxscoreteams.boxscoreteaminfo import BoxScoreVL

@dataclass
class BoxScoreOffical:
    official:       Union[Person, Dict[str, Any]]
    officialType:   str

    def __post_init__(self):
        self.official = Person(**official)

@dataclass
class BoxScore:
    teams:          Union[BoxScoreTeams, Dict[str, Any]]
    officials:      Union[List[BoxScoreOffical], List[Dict[str, Any]]]
    info:           Union[List[BoxScoreVL], List[Dict[str, Any]]]
    pitchingNotes:  List[str]

    def __post_init__(self):
        self.teams = BoxScoreTeams(**teams)
        self.officials = [BoxScoreOffical(**official) for official in officials]
        self.info = [BoxScoreVL(**infos) for infos in info]
        self.pitchingNotes = pitchingNotes
