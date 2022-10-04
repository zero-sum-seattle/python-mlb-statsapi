from typing import Union, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.people import Person, PrimaryPosition

from mlbstatsapi.models.game.livedata.plays.play.playevent.playeventdetails import PlayEventDetails
from mlbstatsapi.models.game.livedata.plays.play.playevent.pitchdata import PitchData
from mlbstatsapi.models.game.livedata.plays.play.playevent.hitdata import HitData

@dataclass
class PlayCount:
    """
    A class to represent a play count.

    Attributes
    ----------
    balls : int
        Balls
    strikes : int
        strikes
    outs : int
        Outs
    """
    balls:      int
    strikes:    int
    outs:       int

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
    details:            Union[PlayEventDetails, Dict[str, Any]]
    index:              int
    startTime:          str
    endTime:            str
    isPitch:            bool
    type:               str
    playId:             str = None
    pitchNumber:        int = None
    actionPlayId:       str = None
    isBaseRunningPlay:  bool = None
    isSubstitution:     bool = None
    battingOrder:       str = None
    count:              Union[PlayCount, Dict[str, Any]] = None
    pitchData:          Union[PitchData, Dict[str, Any]] = None
    hitData:            Union[HitData, Dict[str, Any]] = None
    player:             Union[Person, Dict[str, Any]] = None
    position:           Union[PrimaryPosition, Dict[str, Any]] = None
    replacedPlayer:     Union[Person, Dict[str, Any]] = None

    def __post_init__(self):
        self.details = PlayEventDetails(**self.details)
        self.count = PlayCount(**self.count) if self.count else self.count
        self.pitchData = PitchData(**self.pitchData) if self.pitchData else self.pitchData
        self.hitData = HitData(**self.hitData) if self.hitData else self.hitData
        self.player = Person(**self.player) if self.player else self.player
        self.replacedPlayer = Person(**self.replacedPlayer) if self.replacedPlayer else self.replacedPlayer
