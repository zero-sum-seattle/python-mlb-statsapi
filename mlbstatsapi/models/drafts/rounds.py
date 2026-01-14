from typing import List, Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.data import CodeDesc
from .attributes import DraftSchool, DraftHome


class DraftPick(MLBBaseModel):
    """
    A class representing a pick made in the MLB draft.

    Attributes
    ----------
    team : Team
        The team that made this draft pick.
    draft_type : CodeDesc
        Information about the type of draft in which this pick was made.
    is_drafted : bool
        Whether or not the player associated with this pick has been drafted.
    is_pass : bool
        Whether or not the team passed on making a pick in this round.
    year : str
        The year in which the draft took place.
    school : DraftSchool
        Information about the player's school or college.
    home : DraftHome
        Information about the player's home location.
    pick_round : str
        The round of the draft in which this pick was made.
    pick_number : int
        The number of the pick in the round.
    display_pick_number : int
        The overall pick number displayed.
    round_pick_number : int
        The number of the pick overall in the draft.
    headshot_link : str
        A link to a headshot image of the player.
    person : Person
        The person drafted.
    bis_player_id : int
        The unique identifier of the player associated with this draft pick.
    rank : int
        The rank of the player among all players eligible for the draft.
    pick_value : str
        The value of the pick, if known.
    signing_bonus : str
        The signing bonus associated with this pick, if known.
    scouting_report : str
        A scouting report on the player's abilities.
    blurb : str
        A brief summary of the player's background and accomplishments.
    """
    team: Team
    draft_type: CodeDesc = Field(alias="draftType")
    is_drafted: bool = Field(alias="isDrafted")
    is_pass: bool = Field(alias="isPass")
    year: str
    school: DraftSchool
    home: DraftHome
    pick_round: str = Field(alias="pickRound")
    pick_number: int = Field(alias="pickNumber")
    display_pick_number: int = Field(alias="displayPickNumber")
    round_pick_number: int = Field(alias="roundPickNumber")
    headshot_link: Optional[str] = Field(default=None, alias="headshotLink")
    person: Optional[Person] = None
    bis_player_id: Optional[int] = Field(default=None, alias="bisPlayerId")
    rank: Optional[int] = None
    pick_value: Optional[str] = Field(default=None, alias="pickValue")
    signing_bonus: Optional[str] = Field(default=None, alias="signingBonus")
    scouting_report: Optional[str] = Field(default=None, alias="scoutingReport")
    blurb: Optional[str] = None


class Round(MLBBaseModel):
    """
    A class representing a round of the MLB draft.

    Attributes
    ----------
    round : str
        The round number of the draft, represented as a string.
    picks : List[DraftPick]
        A list of DraftPick objects representing the picks made in this round.
    """
    round: str
    picks: List[DraftPick] = []
