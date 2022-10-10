from typing import Union, Dict, List, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.people import Person

from mlbstatsapi.models.game.livedata.boxscore.boxscoreteams import BoxScoreTeams
from mlbstatsapi.models.game.livedata.boxscore.boxscoreteams.boxscoreteaminfo import BoxScoreVL

@dataclass
class BoxScoreOffical:
    """
    A class to represent an official for this game

    Attributes
    ----------
    official : Person
        The official person
    officialType : str
        What type of official this person is
    """
    official:       Union[Person, Dict[str, Any]]
    officialType:   str

    def __post_init__(self):
        self.official = Person(**self.official)

@dataclass
class BoxScore:
    """
    A class to represent this games boxscore

    Attributes
    ----------
    teams : BoxScoreTeams
        Box score data for each team
    officials : List[BoxScoreOffical]
        The officials for this game
    info : List[BoxScoreVL]
        Box score information
    pitchingNotes : List[str]
        Pitching notes for this game
    """
    teams:          Union[BoxScoreTeams, Dict[str, Any]]
    officials:      Union[List[BoxScoreOffical], List[Dict[str, Any]]]
    info:           Union[List[BoxScoreVL], List[Dict[str, Any]]]
    pitchingNotes:  List[str]

    def __post_init__(self):
        self.teams = BoxScoreTeams(**self.teams)
        self.officials = [BoxScoreOffical(**official) for official in self.officials]
        self.info = [BoxScoreVL(**infos) for infos in self.info]
