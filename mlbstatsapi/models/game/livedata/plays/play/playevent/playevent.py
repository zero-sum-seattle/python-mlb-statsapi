from typing import Union, Dict, Any
from dataclasses import dataclass
from mlbstatsapi.models.people import Person, PrimaryPosition

from mlbstatsapi.models.game.livedata.plays.play.playevent.playeventdetails import PlayEventDetails
from mlbstatsapi.models.game.livedata.plays.play.playevent.pitchdata import PitchData
from mlbstatsapi.models.game.livedata.plays.play.playevent.hitdata import HitData

@dataclass
class PlayCount:
    balls:      int
    strikes:    int
    outs:       int

@dataclass
class PlayEvent:
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
