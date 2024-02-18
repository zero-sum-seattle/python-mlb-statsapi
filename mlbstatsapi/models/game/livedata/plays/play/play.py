from typing import Union, Optional, List
from pydantic import BaseModel

from mlbstatsapi.models.game.livedata.plays.play.matchup import PlayMatchup
from mlbstatsapi.models.game.livedata.plays.play.playrunner import PlayRunner
from mlbstatsapi.models.game.livedata.plays.play.playevent import PlayEvent
from mlbstatsapi.models.data import Count
from .attributes import PlayAbout, PlayResult, PlayReviewDetails


class Play(BaseModel):
    """Represents a single play in a game.

    Attributes:
        result (PlayResult): The result of the play.
        about (PlayAbout): Information about the play.
        count (Count): The play's count.
        matchup (PlayMatchup): The play's matchup.
        pitchIndex (List[int]): Indexes of pitches in this play, indexing `playEvents`.
        actionIndex (List[int]): Indexes of actions in this play, indexing `playEvents`.
        runnerIndex (List[int]): Indexes of runners in this play, indexing `runners`.
        runners (List[PlayRunner]): Information about runners during the play.
        playEvents (List[PlayEvent]): Events that occurred during the play.
        playEndTime (Optional[str]): The time this play ends. Defaults to None.
        atBatIndex (int): The play's index number.
        reviewDetails (Optional[PlayReviewDetails]): Information on reviews if present. Defaults to None.
    """
    result: PlayResult
    about: PlayAbout
    count: Count
    matchup: PlayMatchup
    pitchIndex: List[int]
    actionIndex: List[int]
    runnerIndex: List[int]
    runners: List[PlayRunner]
    playEvents: List[PlayEvent]
    atBatIndex: int
    playEndTime: Optional[str] = None
    reviewDetails: Optional[PlayReviewDetails] = None
