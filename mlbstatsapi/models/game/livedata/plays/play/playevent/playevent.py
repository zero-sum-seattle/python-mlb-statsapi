from typing import Union, Optional
from dataclasses import dataclass
from mlbstatsapi.models.people import Person, Position

from mlbstatsapi.models.game.livedata.plays.play.playevent.pitchdata import PitchData

from .attributes import PlayEventDetails, PlayCount, HitData

@dataclass
class PlayEvent:
    """
    A class to represent a information about a play.

    Attributes
    ----------
    details : PlayEventDetails
        Event details
    index : int
        Event index
    starttime : str
        Event start time
    endtime : str
        Event end time
    ispitch : bool
        Is this event a pitch
    type : str
        Type
    playid : str = None
        Unique play id ?
    pitchnumber : int = None
        Pitch number
    actionplayid : str = None
        Unique action play id ?
    isbaserunningplay : bool = None
        Is there base running this play
    issubstitution : bool = None
        Is this a substitution
    battingorder : str = None
        A weird batting order string that only has appeared once
    count : PlayCount  = None
        Count
    pitchdata : PitchData  = None
        Pitch data
    hitdata : HitData  = None
        Hit data
    player : Person  = None
        Player
    position : PrimaryPosition  = None
        Position
    replacedplayer : Person  = None
        Replaced player
    """
    details: Union[PlayEventDetails, dict]
    index: int
    starttime: str
    endtime: str
    ispitch: bool
    type: str
    playid: Optional[str] = None
    pitchnumber: Optional[int] = None
    actionplayid: Optional[str] = None
    isbaserunningplay: Optional[bool] = None
    issubstitution: Optional[bool] = None
    battingorder: Optional[str] = None
    count: Optional[Union[PlayCount, dict]] = None
    pitchdata: Optional[Union[PitchData, dict]] = None
    hitdata: Optional[Union[HitData, dict]] = None
    player: Optional[Union[Person, dict]] = None
    position: Optional[Union[Position, dict]] = None
    replacedplayer: Optional[Union[Person, dict]] = None

    def __post_init__(self):
        self.details = PlayEventDetails(**self.details)
        self.count = PlayCount(**self.count) if self.count else self.count
        self.pitchdata = PitchData(**self.pitchdata) if self.pitchdata else self.pitchdata
        self.hitdata = HitData(**self.hitdata) if self.hitdata else self.hitdata
        self.player = Person(**self.player) if self.player else self.player
        self.position = Position(**self.position) if self.position else self.position
        self.replacedplayer = Person(**self.replacedplayer) if self.replacedplayer else self.replacedplayer
