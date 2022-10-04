from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays.play.playevent import PlayCount
from mlbstatsapi.models.game.livedata.plays.play.playmatchup import PlayMatchup
from mlbstatsapi.models.game.livedata.plays.play.playrunner import PlayRunner
from mlbstatsapi.models.game.livedata.plays.play.playevent import PlayEvent

@dataclass
class PlayAbout:
    atBatIndex:         int
    halfInning:         str
    isTopInning:        bool
    inning:             int
    startTime:          str
    endTime:            str
    isComplete:         bool
    isScoringPlay:      bool
    hasReview:          bool
    hasOut:             bool
    captivatingIndex:   int

@dataclass
class PlayResult:
    type:           str
    event:          str
    eventType:      str
    description:    str
    rbi:            int
    awayScore:      int
    homeScore:      int

@dataclass
class Play:
    result:         Union[PlayResult, Dict[str, Any]]
    about:          Union[PlayAbout, Dict[str, Any]]
    count:          Union[PlayCount, Dict[str, Any]]
    matchup:        Union[PlayMatchup, Dict[str, Any]]
    pitchIndex:     List[int]
    actionIndex:    List[int]
    runnerIndex:    List[int]
    runners:        Union[List[PlayRunners], List[Dict[str, Any]]]
    playEvents:     Union[List[PlayEvent], List[Dict[str, Any]]]
    playEndTime:    str
    atBatIndex:     int

    def __post_init__(self):
        self.result = PlayResult(**result)
        self.about = PlayAbout(**about)
        self.count = PlayCount(**count)
        self.matchup = PlayMatchup(**matchup)
        self.runners = [PlayRunner(**runner) for runner in runners]
        self.playEvents = [PlayEvent(**playEvent) for playEvent in playEvents]
