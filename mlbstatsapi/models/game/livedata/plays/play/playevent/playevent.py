from typing import Optional, Union, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.data import Count, HitData, PitchData, PlayDetails


class PlayEvent(MLBBaseModel):
    """
    A class to represent a play event.

    Attributes
    ----------
    details : PlayDetails
        Event details.
    index : int
        Event index.
    start_time : str
        Event start time.
    end_time : str
        Event end time.
    is_pitch : bool
        Is this event a pitch.
    type : str
        Type.
    play_id : str
        Unique play ID.
    pitch_number : int
        Pitch number.
    action_play_id : str
        Unique action play ID.
    is_base_running_play : bool
        Is there base running this play.
    is_substitution : bool
        Is this a substitution.
    batting_order : str
        Batting order string.
    count : Count
        Count.
    pitch_data : PitchData
        Pitch data.
    hit_data : HitData
        Hit data.
    player : Person
        Player.
    position : Position
        Position.
    replaced_player : Person
        Replaced player.
    """
    details: PlayDetails
    index: int
    is_pitch: bool = Field(alias="isPitch")
    type: str
    pfx_id: Optional[str] = Field(default=None, alias="pfxId")
    start_time: Optional[str] = Field(default=None, alias="startTime")
    end_time: Optional[str] = Field(default=None, alias="endTime")
    # MLB API sometimes returns a person object (id/link) instead of a string.
    umpire: Optional[Union[str, Person]] = None
    base: Optional[str] = None
    play_id: Optional[str] = Field(default=None, alias="playId")
    pitch_number: Optional[int] = Field(default=None, alias="pitchNumber")
    action_play_id: Optional[str] = Field(default=None, alias="actionPlayId")
    is_base_running_play: Optional[bool] = Field(default=None, alias="isBaseRunningPlay")
    is_substitution: Optional[bool] = Field(default=None, alias="isSubstitution")
    batting_order: Optional[str] = Field(default=None, alias="battingOrder")
    count: Optional[Count] = None
    pitch_data: Optional[PitchData] = Field(default=None, alias="pitchData")
    hit_data: Optional[HitData] = Field(default=None, alias="hitData")
    player: Optional[Person] = None
    position: Optional[Position] = None
    replaced_player: Optional[Person] = Field(default=None, alias="replacedPlayer")
    review_details: Optional[dict] = Field(default=None, alias="reviewDetails")
    injury_type: Optional[str] = Field(default=None, alias="injuryType")

    @field_validator("umpire", mode="before")
    @classmethod
    def _empty_dict_to_none(cls, v: Any) -> Any:
        if isinstance(v, dict) and not v:
            return None
        return v
