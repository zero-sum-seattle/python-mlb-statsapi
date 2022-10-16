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
    batside : PlayMatchupSide
        batters batside
    pitcher : Person
        Matchup pitcher
    pitchhand : PlayMatchupSide
        Pitchers side
    batterhotcoldzones : List

    pitcherhotcoldzones : List

    splits : PlayMatchupSplits
        PlayMatchupSplits
    batterhotcoldzonestats : List = None

    postonfirst : Person = None
        Runner on first
    postonsecond : Person = None
        Runner on second
    postonthird : Person = None
        Runner on third
    """
    batter: Union[Person, dict]
    batside: Union[PlayMatchupSide, dict]
    pitcher: Union[Person, dict]
    pitchhand: Union[PlayMatchupSide, dict]
    batterhotcoldzones: List
    pitcherhotcoldzones: List
    splits: Union[PlayMatchupSplits, dict]
    batterhotcoldzonestats: Optional[List] = None
    postonfirst: Optional[Union[Person, dict]] = None
    postonsecond: Optional[Union[Person, dict]] = None
    postonthird: Optional[Union[Person, dict]] = None

    def __post_init__(self):
        self.batter = Person(**self.batter)
        self.batside = PlayMatchupSide(**self.batside)
        self.pitcher = Person(**self.pitcher)
        self.pitchhand = PlayMatchupSide(**self.pitchhand)
        self.splits = PlayMatchupSplits(**self.splits)
        self.batterhotcoldzonestats = self.batterhotcoldzonestats['stats'] if self.batterhotcoldzonestats else self.batterhotcoldzonestats
        self.postonfirst = Person(**self.postonfirst) if self.postonfirst else self.postonfirst
        self.postonsecond = Person(**self.postonsecond) if self.postonsecond else self.postonsecond
        self.postonthird = Person(**self.postonthird) if self.postonthird else self.postonthird