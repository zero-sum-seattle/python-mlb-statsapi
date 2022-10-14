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
    startTime : str
        Event start time
    endTime : str
        Event end time
    isPitch : bool
        Is this event a pitch
    type : str
        Type
    playId : str = None
        Unique play id ?
    pitchNumber : int = None
        Pitch number
    actionPlayId : str = None
        Unique action play id ?
    isBaseRunningPlay : bool = None
        Is there base running this play
    isSubstitution : bool = None
        Is this a substitution
    battingOrder : str = None
        A weird batting order string that only has appeared once
    count : PlayCount  = None
        Count
    pitchData : PitchData  = None
        Pitch data
    hitData : HitData  = None
        Hit data
    player : Person  = None
        Player
    position : PrimaryPosition  = None
        Position
    replacedPlayer : Person  = None
        Replaced player
    """
    details: Union[PlayEventDetails, dict]
    index: int
    startTime: str
    endTime: str
    isPitch: bool
    type: str
    playId: Optional[str] = None
    pitchNumber: Optional[int] = None
    actionPlayId: Optional[str] = None
    isBaseRunningPlay: Optional[bool] = None
    isSubstitution: Optional[bool] = None
    battingOrder: Optional[str] = None
    count: Optional[Union[PlayCount, dict]] = None
    pitchData: Optional[Union[PitchData, dict]] = None
    hitData: Optional[Union[HitData, dict]] = None
    player: Optional[Union[Person, dict]] = None
    position: Optional[Union[Position, dict]] = None
    replacedPlayer: Optional[Union[Person, dict]] = None

    def __post_init__(self):
        self.details = PlayEventDetails(**self.details)
        self.count = PlayCount(**self.count) if self.count else self.count
        self.pitchData = PitchData(**self.pitchData) if self.pitchData else self.pitchData
        self.hitData = HitData(**self.hitData) if self.hitData else self.hitData
        self.player = Person(**self.player) if self.player else self.player
        self.position = Position(**self.position) if self.position else self.position
        self.replacedPlayer = Person(**self.replacedPlayer) if self.replacedPlayer else self.replacedPlayer
