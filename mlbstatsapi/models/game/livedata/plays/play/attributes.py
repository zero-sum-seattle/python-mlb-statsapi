from dataclasses import dataclass

@dataclass
class PlayAbout:
    """
    A class to represent a information about a play.

    Attributes
    ----------
    atBatIndex : int
        Current at bat index
    halfInning : str
        What side of the inning
    isTopInning : bool
        Is this inning the top of the inning
    inning : int
        What number of inning we are in
    startTime : str
        The start time for this play
    endTime : str
        The end time for this play
    isComplete : bool
        Is this play complete
    isScoringPlay : bool
        is this play a scoring play
    hasReview : bool
        Dose this play have a review
    hasOut : bool
        Does this play have a out
    captivatingIndex : int
        What is the captivating index for this play
    """
    atBatIndex: int
    halfInning: str
    isTopInning: bool
    inning: int
    startTime: str
    endTime: str
    isComplete: bool
    isScoringPlay: bool
    hasReview: bool
    hasOut: bool
    captivatingIndex: int

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
    eventType : str
        Event type
    description : str
        Event description
    rbi : int
        Number of RBI's
    awayScore : int
        Score for away team
    homeScore : int
        Score for home team
    """
    type: str
    event: str
    eventType: str
    description: str
    rbi: int
    awayScore: int
    homeScore: int

@dataclass
class PlayReviewDetails:
    """
    A class to represent play review details.

    Attributes
    ----------
    isOverturned : bool
        Was it overturned
    inProgress : bool
        Is it in progress
    reviewType : str
        What type of review
    challengeTeamId : int
        The team issuing the challenge review
    """
    isOverturned: bool
    inProgress: bool
    reviewType: str
    challengeTeamId: int