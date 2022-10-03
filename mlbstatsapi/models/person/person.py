from typing import List, Dict, Union
from .person_data_class import PrimaryPosition, PitchHand, BatSide
from mlbstatsapi import MlbObject
from mlbstatsapi.stats import Stats

class Person(MlbObject):
    """
    A class to represent a Person.

    Attributes
    ----------
    id : int
        id number of the person
    full_name: str
        full_name of the person
    """

    id: int
    full_name: str
    link: str
    stats: List[Stats]
    primary_position: Union[PrimaryPosition,dict]
    pitch_hand: Union[PitchHand,dict]
    bad_side: Union[BatSide,dict]
    strikeZoneTop: float
    strikeZoneBottom: float
    mlb_class = "people"
    
    def __init__(self, 
                id: int, 
                link: str, 
                primaryPosition: Union[PrimaryPosition,dict] = None, 
                pitchHand: Union[PitchHand,dict] = None, 
                batSide: Union[BatSide,dict] = None,
                strikeZoneTop: float = None,
                strikeZoneBottom: float = None,
                fullName: str = None, 
                stats: List[Stats] = None, 
                reload: bool = False, 
                **kwargs) -> None:

        self.id = id 
        self.full_name = fullName 
        self.link = link
        self.strikezonetop = strikeZoneTop
        self.strikezonebottom = strikeZoneBottom
        self.stats = [ Stats(**stat) for stat in stats ] if isinstance(stats, dict) else []
        self.primary_position = PrimaryPosition(**primaryPosition) if isinstance(primaryPosition, dict) else primaryPosition
        self.bat_side = BatSide(**batSide) if isinstance(batSide, dict) else batSide
        self.pitch_hand = PitchHand(**pitchHand) if isinstance(pitchHand, type) else pitchHand

        self.__dict__.update(kwargs) 