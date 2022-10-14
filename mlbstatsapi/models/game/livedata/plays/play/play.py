from typing import Union, Optional, List
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays.play.playevent import PlayCount
from mlbstatsapi.models.game.livedata.plays.play.matchup import PlayMatchup
from mlbstatsapi.models.game.livedata.plays.play.playrunner import PlayRunner
from mlbstatsapi.models.game.livedata.plays.play.playevent import PlayEvent

from .attributes import PlayAbout, PlayResult, PlayReviewDetails

@dataclass
class Play:
    """
    A class to represent a single play in this game.

    Attributes
    ----------
    result : PlayResult
        Play result
    about : PlayAbout
        Information about this play
    count : PlayCount
        This plays count
    matchup : PlayMatchup
        This plays matchup
    pitchIndex : List[int]
        Pitch index for this play, indexing playEvents
    actionIndex : List[int]
        Action index for this play, indexing playEvents
    runnerIndex : List[int]
        Runner index for this play, indexing runners
    runners : List[PlayRunner]
        Runners
    playEvents : List[PlayEvent]
        Play events
    playEndTime : str
        Time this play ends
    atBatIndex : int
        The play index number
    reviewDetails : PlayReviewDetails
        Information on reviews if present
    """
    result: Union[PlayResult, dict]
    about: Union[PlayAbout, dict]
    count: Union[PlayCount, dict]
    matchup: Union[PlayMatchup, dict]
    pitchIndex: List[int]
    actionIndex: List[int]
    runnerIndex: List[int]
    runners: Union[List[PlayRunner], List[dict]]
    playEvents: Union[List[PlayEvent], List[dict]]
    playEndTime: str
    atBatIndex: int
    reviewDetails: Optional[Union[PlayReviewDetails, dict]] = None

    def __post_init__(self):
        self.result = PlayResult(**self.result)
        self.about = PlayAbout(**self.about)
        self.count = PlayCount(**self.count)
        self.matchup = PlayMatchup(**self.matchup)
        self.runners = [PlayRunner(**runner) for runner in self.runners]
        self.playEvents = [PlayEvent(**playEvent) for playEvent in self.playEvents]
        self.reviewDetails = PlayReviewDetails(**self.reviewDetails) if self.reviewDetails else self.reviewDetails
