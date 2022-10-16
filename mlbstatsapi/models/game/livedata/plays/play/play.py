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
    pitchindex : List[int]
        Pitch index for this play, indexing playEvents
    actionindex : List[int]
        Action index for this play, indexing playEvents
    runnerindex : List[int]
        Runner index for this play, indexing runners
    runners : List[PlayRunner]
        Runners
    playevents : List[PlayEvent]
        Play events
    playendtime : str
        Time this play ends
    atbatindex : int
        The play index number
    reviewdetails : PlayReviewDetails
        Information on reviews if present
    """
    result: Union[PlayResult, dict]
    about: Union[PlayAbout, dict]
    count: Union[PlayCount, dict]
    matchup: Union[PlayMatchup, dict]
    pitchindex: List[int]
    actionindex: List[int]
    runnerindex: List[int]
    runners: Union[List[PlayRunner], List[dict]]
    playevents: Union[List[PlayEvent], List[dict]]
    playendtime: str
    atbatindex: int
    reviewdetails: Optional[Union[PlayReviewDetails, dict]] = None

    def __post_init__(self):
        self.result = PlayResult(**self.result)
        self.about = PlayAbout(**self.about)
        self.count = PlayCount(**self.count)
        self.matchup = PlayMatchup(**self.matchup)
        self.runners = [PlayRunner(**runner) for runner in self.runners]
        self.playevents = [PlayEvent(**playevent) for playevent in self.playevents]
        self.reviewdetails = PlayReviewDetails(**self.reviewdetails) if self.reviewdetails else self.reviewdetails
