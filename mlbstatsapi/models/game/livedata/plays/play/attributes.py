from typing import Optional, Any, Dict, List, Union
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
    at_bat_index: int = Field(alias="atBatIndex")
    half_inning: str = Field(alias="halfInning")
    is_top_inning: bool = Field(alias="isTopInning")
    inning: int
    is_complete: bool = Field(alias="isComplete")
    is_scoring_play: bool = Field(alias="isScoringPlay")
    has_out: bool = Field(alias="hasOut")
    captivating_index: int = Field(alias="captivatingIndex")
    end_time: Optional[str] = Field(default=None, alias="endTime")
    start_time: Optional[str] = Field(default=None, alias="startTime")
    has_review: Optional[bool] = Field(default=None, alias="hasReview")


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
    away_score: int = Field(alias="awayScore")
    home_score: int = Field(alias="homeScore")
    rbi: Optional[int] = None
    event: Optional[str] = None
    event_type: Optional[str] = Field(default=None, alias="eventType")
    description: Optional[str] = None
    is_out: Optional[bool] = Field(default=None, alias="isOut")


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
    is_overturned: bool = Field(alias="isOverturned")
    in_progress: bool = Field(alias="inProgress")
    review_type: str = Field(alias="reviewType")
    challenge_team_id: Optional[int] = Field(default=None, alias="challengeTeamId")
    # MLB API returns this as either null, a string, or a list of review objects.
    additional_reviews: Optional[Union[str, List[Dict[str, Any]]]] = Field(default=None, alias="additionalReviews")
