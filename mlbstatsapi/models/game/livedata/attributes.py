from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person


class GameDecisions(MLBBaseModel):
    """
    A class to represent the winning and losing pitcher for this game.
    Only used when a game is over.

    Attributes
    ----------
    winner : Person
        The winning pitcher.
    loser : Person
        The losing pitcher.
    save : Person
        The save pitcher (if applicable).
    """
    winner: Person
    loser: Person
    save: Optional[Person] = None


class GameLeaders(MLBBaseModel):
    """
    A class to represent this game's live data leaders.

    Attributes
    ----------
    hit_distance : dict
        Hit distance leaders.
    hit_speed : dict
        Hit speed leaders.
    pitch_speed : dict
        Pitch speed leaders.
    """
    hit_distance: dict = Field(alias="hitDistance")
    hit_speed: dict = Field(alias="hitSpeed")
    pitch_speed: dict = Field(alias="pitchSpeed")
