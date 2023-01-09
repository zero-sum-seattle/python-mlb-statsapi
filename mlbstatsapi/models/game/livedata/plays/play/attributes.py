from typing import Optional
from dataclasses import dataclass

@dataclass(repr=False)
class PlayAbout:
    """
    A class to represent a information about a play.

    Attributes
    ----------
    atbatindex : int
        Current at bat index
    halfinning : str
        What side of the inning
    istopinning : bool
        Is this inning the top of the inning
    inning : int
        What number of inning we are in
    starttime : str
        The start time for this play
    endtime : str
        The end time for this play
    iscomplete : bool
        Is this play complete
    isscoringplay : bool
        is this play a scoring play
    hasreview : bool
        Dose this play have a review
    hasout : bool
        Does this play have a out
    captivatingindex : int
        What is the captivating index for this play
    """
    atbatindex: int
    halfinning: str
    istopinning: bool
    inning: int
    iscomplete: bool
    isscoringplay: bool
    hasout: bool
    captivatingindex: int
    endtime: Optional[str] = None
    starttime: Optional[str] = None
    hasreview: Optional[bool] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class PlayResult:
    """
    A class to represent a play result.

    Attributes
    ----------
    type : str
        Play result type
    event : str
        Play event
    eventtype : str
        Event type
    description : str
        Event description
    rbi : int
        Number of RBI's
    awayscore : int
        Score for away team
    homescore : int
        Score for home team
    isout : bool
        If the play was an out
    """
    type: str
    rbi: int
    awayscore: int
    homescore: int
    event: Optional[str] = None
    eventtype: Optional[str] = None
    description: Optional[str] = None
    isout: Optional[bool] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

@dataclass(repr=False)
class PlayReviewDetails:
    """
    A class to represent play review details.

    Attributes
    ----------
    isoverturned : bool
        Was it overturned
    inprogress : bool
        Is it in progress
    reviewtype : str
        What type of review
    challengeteamid : int
        The team issuing the challenge review
    """
    isoverturned: bool
    inprogress: bool
    reviewtype: str
    challengeteamid: Optional[int] = None
    additionalreviews: Optional[str] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None]
        return "{}({})".format(type(self).__name__, ", ".join(kws))