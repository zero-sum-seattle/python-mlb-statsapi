from typing import Union, Optional
from dataclasses import dataclass
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.data import Count, HitData, PitchData, PlayDetails

@dataclass(repr=False)
class PlayEvent:
    """
    A class to represent a information about a play.

    Attributes
    ----------
    details : PlayDetails
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
    playid : str
        Unique play id ?
    pitchnumber : int
        Pitch number
    actionplayid : str
        Unique action play id ?
    isbaserunningplay : bool
        Is there base running this play
    issubstitution : bool
        Is this a substitution
    battingorder : str
        A weird batting order string that only has appeared once
    count : PlayCount
        Count
    pitchdata : PitchData
        Pitch data
    hitdata : HitData
        Hit data
    player : Person
        Player
    position : Position
        Position
    replacedplayer : Person
        Replaced player
    """
    details: Union[PlayDetails, dict]
    index: int
    ispitch: bool
    type: str
    pfxid: Optional[str] = None
    starttime: Optional[str] = None
    endtime: Optional[str] = None
    umpire: Optional[str] = None
    base: Optional[str] = None
    playid: Optional[str] = None
    pitchnumber: Optional[int] = None
    actionplayid: Optional[str] = None
    isbaserunningplay: Optional[bool] = None
    issubstitution: Optional[bool] = None
    battingorder: Optional[str] = None
    count: Optional[Union[Count, dict]] = None
    pitchdata: Optional[Union[PitchData, dict]] = None
    hitdata: Optional[Union[HitData, dict]] = None
    player: Optional[Union[Person, dict]] = None
    position: Optional[Union[Position, dict]] = None
    replacedplayer: Optional[Union[Person, dict]] = None
    reviewdetails: Optional[dict] = None
    injurytype: Optional[str] = None

    def __post_init__(self):
        self.details = PlayDetails(**self.details)
        self.count = Count(**self.count) if self.count else self.count
        self.pitchdata = PitchData(**self.pitchdata) if self.pitchdata else self.pitchdata
        self.hitdata = HitData(**self.hitdata) if self.hitdata else self.hitdata
        self.player = Person(**self.player) if self.player else self.player
        self.position = Position(**self.position) if self.position else self.position
        self.replacedplayer = Person(**self.replacedplayer) if self.replacedplayer else self.replacedplayer

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))