from typing import Union, Optional, List
from dataclasses import dataclass

from mlbstatsapi.models.people import Person

from .attributes import PlayMatchupSide, PlayMatchupSplits

@dataclass
class PlayMatchup:
    """
    A class to represent a play Matchup.

    Attributes
    ----------
    batter : Person
        Matchup batter
    batSide : PlayMatchupSide
        batters batside
    pitcher : Person
        Matchup pitcher
    pitchHand : PlayMatchupSide
        Pitchers side
    batterHotColdZones : List

    pitcherHotColdZones : List

    splits : PlayMatchupSplits
        PlayMatchupSplits
    batterHotColdZoneStats : List = None

    postOnFirst : Person = None
        Runner on first
    postOnSecond : Person = None
        Runner on second
    postOnThird : Person = None
        Runner on third
    """
    batter: Union[Person, dict]
    batSide: Union[PlayMatchupSide, dict]
    pitcher: Union[Person, dict]
    pitchHand: Union[PlayMatchupSide, dict]
    batterHotColdZones: List
    pitcherHotColdZones: List
    splits: Union[PlayMatchupSplits, dict]
    batterHotColdZoneStats: Optional[List] = None
    postOnFirst: Optional[Union[Person, dict]] = None
    postOnSecond: Optional[Union[Person, dict]] = None
    postOnThird: Optional[Union[Person, dict]] = None

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