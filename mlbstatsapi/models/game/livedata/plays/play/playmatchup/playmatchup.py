from typing import Union, Dict, List, Any
from dataclasses import dataclass
from mlbstatsapi.models.people import Person

@dataclass
class PlayMatchupSide:
    code:           str
    description:    str

@dataclass
class PlayMatchupSplits:
    batter:     str
    pitcher:    str
    menOnBase:  str

@dataclass
class PlayMatchup:
    batter:                 Union[Person, Dict[str, Any]]
    batSide:                Union[PlayMatchupSide, Dict[str, Any]]
    pitcher:                Union[Person, Dict[str, Any]]
    pitchHand:              Union[PlayMatchupSide, Dict[str, Any]]
    batterHotColdZones:     List
    pitcherHotColdZones:    List
    splits:                 Union[PlayMatchupSplits, Dict[str, Any]]
    batterHotColdZoneStats: List = None
    postOnFirst:            Union[Person, Dict[str, Any]] = None
    postOnSecond:           Union[Person, Dict[str, Any]] = None
    postOnThird:            Union[Person, Dict[str, Any]] = None


    def __post_init__(self):
        self.batter = Person(**self.batter)
        self.batSide = PlayMatchupSide(**self.batSide)
        self.pitcher = Person(**self.pitcher)
        self.pitchHand = PlayMatchupSide(**self.pitchHand)
        self.splits = PlayMatchupSplits(**self.splits)
        self.batterHotColdZoneStats = self.batterHotColdZoneStats['stats'] if self.batterHotColdZoneStats else self.batterHotColdZoneStats
        self.postOnFirst = Person(**self.postOnFirst) if self.postOnFirst else self.postOnFirst
        self.postOnSecond = Person(**self.postOnSecond) if self.postOnSecond else self.postOnSecond
        self.postOnThird = Person(**self.postOnThird) if self.postOnThird else self.postOnThird
