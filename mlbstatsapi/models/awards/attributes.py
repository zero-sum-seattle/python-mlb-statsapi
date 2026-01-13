from typing import Optional
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person


class Award(MLBBaseModel):
    """
    A class representing an award.

    Attributes
    ----------
    id : str
        Award ID.
    name : str
        Name of the award.
    date : str
        Date of when award was given.
    season : str
        Season award is for/from.
    team : Team
        Team award was to / Player is from.
    player : Person
        Person award is for.
    votes : int
        Any votes associated with award.
    notes : str
        Any notes associated with award.
    """
    id: str
    name: str
    date: str
    season: str
    team: Team
    player: Person
    votes: Optional[int] = None
    notes: Optional[str] = None
