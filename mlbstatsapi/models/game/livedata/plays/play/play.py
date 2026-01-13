from typing import Optional, List
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.game.livedata.plays.play.matchup import PlayMatchup
from mlbstatsapi.models.game.livedata.plays.play.playrunner import PlayRunner
from mlbstatsapi.models.game.livedata.plays.play.playevent import PlayEvent
from mlbstatsapi.models.data import Count
from .attributes import PlayAbout, PlayResult, PlayReviewDetails


class Play(MLBBaseModel):
    """
    A class to represent a single play in this game.

    Attributes
    ----------
    result : PlayResult
        Play result.
    about : PlayAbout
        Information about this play.
    count : Count
        This play's count.
    matchup : PlayMatchup
        This play's matchup.
    pitch_index : List[int]
        Pitch index for this play, indexing play events.
    action_index : List[int]
        Action index for this play, indexing play events.
    runner_index : List[int]
        Runner index for this play, indexing runners.
    runners : List[PlayRunner]
        Runners.
    play_events : List[PlayEvent]
        Play events.
    play_end_time : str
        Time this play ends.
    at_bat_index : int
        The play index number.
    review_details : PlayReviewDetails
        Information on reviews if present.
    """
    result: PlayResult
    about: PlayAbout
    count: Count
    matchup: PlayMatchup
    pitch_index: List[int] = Field(alias="pitchindex")
    action_index: List[int] = Field(alias="actionindex")
    runner_index: List[int] = Field(alias="runnerindex")
    runners: List[PlayRunner] = []
    play_events: List[PlayEvent] = Field(default=[], alias="playevents")
    at_bat_index: int = Field(alias="atbatindex")
    play_end_time: Optional[str] = Field(default=None, alias="playendtime")
    review_details: Optional[PlayReviewDetails] = Field(default=None, alias="reviewdetails")
