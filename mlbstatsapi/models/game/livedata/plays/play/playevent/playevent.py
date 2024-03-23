from typing import Optional
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.data import Count, HitData, PitchData, PlayDetails
from pydantic import BaseModel

class PlayEvent(BaseModel):
    """
    A class to represent information about a play.

    Attributes:
        details (Union[PlayDetails, dict]): Event details.
        index (int): Event index.
        isPitch (bool): Indicates if this event is a pitch.
        type (str): Type of event.
        pfxid (Optional[str]): Unique play ID, optional.
        startTime (Optional[str]): Event start time, optional.
        endTime (Optional[str]): Event end time, optional.
        umpire (Optional[str]): Umpire involved, optional.
        base (Optional[str]): Base involved in the event, optional.
        playId (Optional[str]): Unique play ID, optional.
        pitchNumber (Optional[int]): Pitch number, optional.
        actionPlayId (Optional[str]): Unique action play ID, optional.
        isBaseRunningPlay (Optional[bool]): Indicates if there is base running in this play, optional.
        isSubstitution (Optional[bool]): Indicates if this is a substitution, optional.
        battingOrder (Optional[str]): A weird batting order string, optional.
        count (Optional[Count]): Count during the play, optional.
        pitchData (Optional[PitchData]): Pitch data, optional.
        hitData (Optional[HitData]): Hit data, optional.
        player (Optional[Person]): Player involved, optional.
        position (Optional[Position]): Position involved, optional.
        replacedPlayer (Optional[Person]): Replaced player, optional.
        reviewDetails (Optional[dict]): Details about any review, defaults to an empty dict.
        injuryType (Optional[str]): Type of injury, if applicable, optional.
    """

    details: PlayDetails
    index: int
    isPitch: bool
    type: str
    pfxid: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    umpire: Optional[str] = None
    base: Optional[str] = None
    playId: Optional[str] = None
    pitchNumber: Optional[int] = None
    actionPlayId: Optional[str] = None
    isBaseRunningPlay: Optional[bool] = None
    isSubstitution: Optional[bool] = None
    battingOrder: Optional[str] = None
    count: Optional[Count] = None
    pitchData: Optional[PitchData] = None
    hitData: Optional[HitData] = None
    player: Optional[Person] = None
    position: Optional[Position] = None
    replacedPlayer: Optional[Person] = None
    reviewDetails: Optional[dict] = {}
    injuryType: Optional[str] = None
