from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel


class PlayAbout(MLBBaseModel):
    """
    A class to represent information about a play.

    Attributes
    ----------
    at_bat_index : int
        Current at bat index.
    half_inning : str
        What side of the inning.
    is_top_inning : bool
        Is this inning the top of the inning.
    inning : int
        What number of inning we are in.
    start_time : str
        The start time for this play.
    end_time : str
        The end time for this play.
    is_complete : bool
        Is this play complete.
    is_scoring_play : bool
        Is this play a scoring play.
    has_review : bool
        Does this play have a review.
    has_out : bool
        Does this play have an out.
    captivating_index : int
        What is the captivating index for this play.
    """
    at_bat_index: int = Field(alias="atbatindex")
    half_inning: str = Field(alias="halfinning")
    is_top_inning: bool = Field(alias="istopinning")
    inning: int
    is_complete: bool = Field(alias="iscomplete")
    is_scoring_play: bool = Field(alias="isscoringplay")
    has_out: bool = Field(alias="hasout")
    captivating_index: int = Field(alias="captivatingindex")
    end_time: Optional[str] = Field(default=None, alias="endtime")
    start_time: Optional[str] = Field(default=None, alias="starttime")
    has_review: Optional[bool] = Field(default=None, alias="hasreview")


class PlayResult(MLBBaseModel):
    """
    A class to represent a play result.

    Attributes
    ----------
    type : str
        Play result type.
    event : str
        Play event.
    event_type : str
        Event type.
    description : str
        Event description.
    rbi : int
        Number of RBIs.
    away_score : int
        Score for away team.
    home_score : int
        Score for home team.
    is_out : bool
        If the play was an out.
    """
    type: str
    away_score: int = Field(alias="awayscore")
    home_score: int = Field(alias="homescore")
    rbi: Optional[int] = None
    event: Optional[str] = None
    event_type: Optional[str] = Field(default=None, alias="eventtype")
    description: Optional[str] = None
    is_out: Optional[bool] = Field(default=None, alias="isout")


class PlayReviewDetails(MLBBaseModel):
    """
    A class to represent play review details.

    Attributes
    ----------
    is_overturned : bool
        Was it overturned.
    in_progress : bool
        Is it in progress.
    review_type : str
        What type of review.
    challenge_team_id : int
        The team issuing the challenge review.
    additional_reviews : str
        Additional reviews.
    """
    is_overturned: bool = Field(alias="isoverturned")
    in_progress: bool = Field(alias="inprogress")
    review_type: str = Field(alias="reviewtype")
    challenge_team_id: Optional[int] = Field(default=None, alias="challengeteamid")
    additional_reviews: Optional[str] = Field(default=None, alias="additionalreviews")
