from typing import Optional
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person, Position


class RunnerCredits(MLBBaseModel):
    """
    A class to represent a runner's credit.

    Attributes
    ----------
    player : Person
        The player.
    position : Position
        The position.
    credit : str
        The credit.
    """
    player: Person
    position: Position
    credit: str


class RunnerMovement(MLBBaseModel):
    """
    A class to represent a play runner movement.

    Attributes
    ----------
    is_out : bool
        Was the running movement an out.
    out_number : int
        What is the out number (None if not an out).
    origin_base : str
        Original base.
    start : str
        What base the runner started from.
    end : str
        What base the runner ended at.
    out_base : str
        Base runner was made out.
    """
    is_out: bool = Field(default=False, alias="isOut")
    out_number: Optional[int] = Field(default=None, alias="outNumber")
    origin_base: Optional[str] = Field(default=None, alias="originBase")
    start: Optional[str] = None
    end: Optional[str] = None
    out_base: Optional[str] = Field(default=None, alias="outBase")

    @field_validator("is_out", mode="before")
    @classmethod
    def _coerce_is_out(cls, v):
        # MLB API occasionally returns null for isOut.
        if v is None:
            return False
        return v


class RunnerDetails(MLBBaseModel):
    """
    A class to represent a play runner details.

    Attributes
    ----------
    event : str
        Runner event.
    event_type : str
        Runner event type.
    runner : Person
        Who the runner is.
    is_scoring_event : bool
        Was this a scoring event.
    rbi : bool
        Was this an RBI.
    earned : bool
        Was it earned.
    team_unearned : bool
        Was it unearned.
    play_index : int
        Play index.
    movement_reason : str
        Reason for the movement.
    responsible_pitcher : Person
        Who was the responsible pitcher.
    """
    event: str
    event_type: str = Field(alias="eventType")
    runner: Person
    is_scoring_event: bool = Field(alias="isScoringEvent")
    rbi: bool
    earned: bool
    team_unearned: bool = Field(alias="teamUnearned")
    play_index: int = Field(alias="playIndex")
    movement_reason: Optional[str] = Field(default=None, alias="movementReason")
    responsible_pitcher: Optional[Person] = Field(default=None, alias="responsiblePitcher")
