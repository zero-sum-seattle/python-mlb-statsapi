from typing import Optional
from pydantic import Field
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
    is_pitch: bool = Field(alias="ispitch")
    type: str
    pfx_id: Optional[str] = Field(default=None, alias="pfxid")
    start_time: Optional[str] = Field(default=None, alias="starttime")
    end_time: Optional[str] = Field(default=None, alias="endtime")
    umpire: Optional[str] = None
    base: Optional[str] = None
    play_id: Optional[str] = Field(default=None, alias="playid")
    pitch_number: Optional[int] = Field(default=None, alias="pitchnumber")
    action_play_id: Optional[str] = Field(default=None, alias="actionplayid")
    is_base_running_play: Optional[bool] = Field(default=None, alias="isbaserunningplay")
    is_substitution: Optional[bool] = Field(default=None, alias="issubstitution")
    batting_order: Optional[str] = Field(default=None, alias="battingorder")
    count: Optional[Count] = None
    pitch_data: Optional[PitchData] = Field(default=None, alias="pitchdata")
    hit_data: Optional[HitData] = Field(default=None, alias="hitdata")
    player: Optional[Person] = None
    position: Optional[Position] = None
    replaced_player: Optional[Person] = Field(default=None, alias="replacedplayer")
    review_details: Optional[dict] = Field(default=None, alias="reviewdetails")
    injury_type: Optional[str] = Field(default=None, alias="injurytype")
