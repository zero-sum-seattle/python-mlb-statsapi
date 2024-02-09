from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel

from .attributes import School, Home
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.data import CodeDesc


class DraftPick(BaseModel):
    """
    Represents a pick made in the MLB draft, detailing the player picked, the round, number, and value of the pick, along with additional information about the player and the drafting team.

    Attributes:
        bisPlayerId (int): The unique identifier of the player associated with this draft pick.
        pickRound (str): The round of the draft in which this pick was made.
        pickNumber (int): The number of the pick in the round.
        roundPickNumber (int): The number of the pick overall in the draft.
        rank (int): The rank of the player among all players eligible for the draft.
        pickValue (str): The value of the pick, if known.
        signingBonus (str): The signing bonus associated with this pick, if known.
        home (Home): Information about the player's home location.
        scoutingReport (str): A scouting report on the player's abilities.
        school (School): Information about the player's school or college.
        blurb (str): A brief summary of the player's background and accomplishments.
        headshotLink (str): A link to a headshot image of the player.
        team (Team): The team that made this draft pick.
        draftType (CodeDesc): Information about the type of draft in which this pick was made.
        isDrafted (bool): Whether or not the player associated with this pick has been drafted.
        isPass (bool): Whether or not the team passed on making a pick in this round.
        year (str): The year in which the draft took place.
    """
    bisPlayerId: Optional[int] = None
    displayPickNumber: Optional[int] = None
    pickRound: str
    pickNumber: int
    roundPickNumber: int
    rank: Optional[int] = None
    pickValue: Optional[str] = None
    signingBonus: Optional[str] = None
    home: Home
    scoutingReport: Optional[str] = None
    school: School
    blurb: Optional[str] = None
    headshotLink: str
    team: Team
    draftType: CodeDesc
    isDrafted: bool
    isPass: bool
    year: str


class Round(BaseModel):
    """
    Represents a round in the MLB draft.

    Attributes:
        round (str): The round number of the draft, represented as a string.
        picks (List[DraftPick]): A list of DraftPick objects, each representing a pick made in this round.
    """
    round: str
    picks: List[DraftPick]

