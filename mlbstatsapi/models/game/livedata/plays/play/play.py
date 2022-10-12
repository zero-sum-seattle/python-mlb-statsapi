from typing import Union, Dict, List, Any
from dataclasses import dataclass

from mlbstatsapi.models.game.livedata.plays.play.playevent import PlayCount
from mlbstatsapi.models.game.livedata.plays.play.playmatchup import PlayMatchup
from mlbstatsapi.models.game.livedata.plays.play.playrunner import PlayRunner
from mlbstatsapi.models.game.livedata.plays.play.playevent import PlayEvent

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
    atBatIndex:         int
    halfInning:         str
    isTopInning:        bool
    inning:             int
    startTime:          str
    endTime:            str
    isComplete:         bool
    isScoringPlay:      bool
    hasReview:          bool
    hasOut:             bool
    captivatingIndex:   int

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
    type:           str
    event:          str
    eventType:      str
    description:    str
    rbi:            int
    awayScore:      int
    homeScore:      int

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
    isOverturned:       bool
    inProgress:         bool
    reviewType:         str
    challengeTeamId:    int

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
    result:         Union[PlayResult, Dict[str, Any]]
    about:          Union[PlayAbout, Dict[str, Any]]
    count:          Union[PlayCount, Dict[str, Any]]
    matchup:        Union[PlayMatchup, Dict[str, Any]]
    pitchIndex:     List[int]
    actionIndex:    List[int]
    runnerIndex:    List[int]
    runners:        Union[List[PlayRunner], List[Dict[str, Any]]]
    playEvents:     Union[List[PlayEvent], List[Dict[str, Any]]]
    playEndTime:    str
    atBatIndex:     int
    reviewDetails:  Union[PlayReviewDetails, Dict[str, Any]] = None

    def __post_init__(self):
        self.result = PlayResult(**self.result)
        self.about = PlayAbout(**self.about)
        self.count = PlayCount(**self.count)
        self.matchup = PlayMatchup(**self.matchup)
        self.runners = [PlayRunner(**runner) for runner in self.runners]
        self.playEvents = [PlayEvent(**playEvent) for playEvent in self.playEvents]
        self.reviewDetails = PlayReviewDetails(**self.reviewDetails) if self.reviewDetails else self.reviewDetails