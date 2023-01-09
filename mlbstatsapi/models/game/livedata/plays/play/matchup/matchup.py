from typing import Union, Optional, List
from dataclasses import dataclass

from mlbstatsapi.models.people import Person
from mlbstatsapi.models.data import CodeDesc

from .attributes import PlayMatchupSplits

@dataclass(repr=False)
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
    pitcherhotcoldzones : List
        Pitcher hot cold zone stats
    splits : PlayMatchupSplits
        PlayMatchupSplits
    batterhotcoldzonestats : List
        Batter hot cold zone stats
    postonfirst : Person
        Runner on first
    postonsecond : Person
        Runner on second
    postonthird : Person
        Runner on third 
    """
    batter: Union[Person, dict]
    batside: Union[CodeDesc, dict]
    pitcher: Union[Person, dict]
    pitchhand: Union[CodeDesc, dict]
    batterhotcoldzones: List
    pitcherhotcoldzones: List
    splits: Union[PlayMatchupSplits, dict]
    batterhotcoldzonestats: Optional[List] = None
    pitcherhotcoldzonestats: Optional[List] = None
    postonfirst: Optional[Union[Person, dict]] = None
    postonsecond: Optional[Union[Person, dict]] = None
    postonthird: Optional[Union[Person, dict]] = None

    def __post_init__(self):
        self.batter = Person(**self.batter)
        self.batside = CodeDesc(**self.batside)
        self.pitcher = Person(**self.pitcher)
        self.pitchhand = CodeDesc(**self.pitchhand)
        self.splits = PlayMatchupSplits(**self.splits)
        self.batterhotcoldzonestats = self.batterhotcoldzonestats['stats'] if self.batterhotcoldzonestats else self.batterhotcoldzonestats
        self.pitcherhotcoldzonestats = self.pitcherhotcoldzonestats['stats'] if self.pitcherhotcoldzonestats else self.pitcherhotcoldzonestats
        self.postonfirst = Person(**self.postonfirst) if self.postonfirst else self.postonfirst
        self.postonsecond = Person(**self.postonsecond) if self.postonsecond else self.postonsecond
        self.postonthird = Person(**self.postonthird) if self.postonthird else self.postonthird
    
    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))