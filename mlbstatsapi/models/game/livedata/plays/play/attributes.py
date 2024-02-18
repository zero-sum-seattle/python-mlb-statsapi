from typing import Optional
from pydantic import BaseModel


class PlayAbout(BaseModel):
    """Represents information about a play.

    Attributes:
        atBatIndex (int): The current at-bat index.
        halfInning (str): Specifies which half of the inning the play is in ('top' or 'bottom').
        isTopInning (bool): Indicates if this is the top half of the inning.
        inning (int): The current inning number.
        startTime (Optional[str]): The start time for this play, if applicable. Defaults to None.
        endTime (Optional[str]): The end time for this play, if applicable. Defaults to None.
        isComplete (bool): Indicates if this play is complete.
        isScoringPlay (bool): Specifies if this play is a scoring play.
        hasReview (Optional[bool]): Indicates if this play has a review, if applicable. Defaults to None.
        hasOut (bool): Specifies if this play results in an out.
        captivatingIndex (int): The captivating index for this play.
    """
    atBatIndex: int
    halfInning: str
    isTopInning: bool
    inning: int
    isComplete: bool
    isScoringPlay: bool
    hasOut: bool
    captivatingIndex: int
    endTime: Optional[str] = None
    startTime: Optional[str] = None
    hasReview: Optional[bool] = None



class PlayResult(BaseModel):
    """Represents the result of a play.

    Attributes:
        type (str): The type of play result.
        event (Optional[str]): The specific event of the play, if applicable. Defaults to None.
        eventType (Optional[str]): The type of event, if applicable. Defaults to None.
        description (Optional[str]): A description of the event, if applicable. Defaults to None.
        rbi (int): Number of runs batted in (RBIs) resulting from the play.
        awayScore (int): Score for the away team after the play.
        homeScore (int): Score for the home team after the play.
        isOut (Optional[bool]): Indicates if the play resulted in an out, if applicable. Defaults to None.
    """
    type: str
    rbi: int
    awayScore: int
    homeScore: int
    event: Optional[str] = None
    eventType: Optional[str] = None
    description: Optional[str] = None
    isOut: Optional[bool] = None


class PlayReviewDetails(BaseModel):
    """Represents the details of a play review.

    Attributes:
        isOverturned (bool): Indicates if the play was overturned.
        inProgress (bool): Indicates if the review is in progress.
        reviewType (str): Describes the type of review.
        challengeTeamId (Optional[int]): The ID of the team issuing the challenge, if applicable. Defaults to None.
        additionalReviews (Optional[str]): Any additional review details, if applicable. Defaults to None.
    """
    isOverturned: bool
    inProgress: bool
    reviewType: str
    challengeTeamId: Optional[int] = None
    additionalReviews: Optional[str] = None

