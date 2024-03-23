from typing import Union, Optional, List
from pydantic import BaseModel

from mlbstatsapi.models.people import Person
from mlbstatsapi.models.data import CodeDesc

from .attributes import PlayMatchupSplits

class PlayMatchup(BaseModel):
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
    batter: Person
    batSide: CodeDesc
    pitcher: Person
    pitchHand: CodeDesc
    splits: Union[PlayMatchupSplits, dict]
    batterHotColdZones: Optional[List] = []
    pitcherHotColdZones: Optional[List] = []
    postOnFirst: Optional[Person] = None
    postOnSecond: Optional[Person] = None
    postOnThird: Optional[Person] = None
