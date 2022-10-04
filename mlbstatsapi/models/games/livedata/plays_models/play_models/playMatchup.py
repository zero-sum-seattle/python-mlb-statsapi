from typing import Union, Dict, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.person import Person

@dataclass
class PlaysPlayMatchupSide:
    code: str
    description: str

@dataclass
class PlayMatchupSplits:
    batter: str
    pitcher: str
    menOnBase: str

@dataclass
class PlaysPlayMatchup:
    batter:                 Union[Person, Dict[str, Any]]
    batSide:                Union[PlayMatchupSide, Dict[str, Any]]
    pitcher:                Union[Person, Dict[str, Any]]
    pitchHand:              Union[PlayMatchupSide, Dict[str, Any]]
    batterHotColdZones:     List
    pitcherHotColdZones:    List
    splits:                 Union[PlayMatchupSplits, Dict[str, Any]]

    def __post_init__(self):
        self.batter = Person(**batter)
        self.batSide = PlayMatchupSide(**batSide)
        self.pitcher = Person(**pitcher)
        self.pitchHand = PlayMatchupSide(**pitchHand)
        self.batterHotColdZones = batterHotColdZones
        self.pitcherHotColdZones = pitcherHotColdZones
        self.splits = PlayMatchupSplits(**splits)
