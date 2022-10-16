from dataclasses import dataclass

@dataclass
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
    starttime: str
    endtime: str
    iscomplete: bool
    isscoringplay: bool
    hasreview: bool
    hasout: bool
    captivatingindex: int

@dataclass
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
    """
    type: str
    event: str
    eventtype: str
    description: str
    rbi: int
    awayscore: int
    homescore: int

@dataclass
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
    challengeteamid: int