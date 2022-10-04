from typing import Union, Dict, List, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.person import Person

from boxScore_models.boxScoreTeams import BoxScoreTeams, BoxScoreVL
from boxScore_models.boxScoreOffical import BoxScoreOffical
from boxScore_models.boxScoreVL import BoxScoreVL

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
