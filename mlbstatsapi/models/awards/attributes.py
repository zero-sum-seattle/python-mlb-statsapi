from typing import Optional
from pydantic import BaseModel

from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person

class Award(BaseModel):
    """Represents an award object.

    Attributes:
        id (str): Unique identifier for the award.
        name (str): Name of the award.
        date (str): Date when the award was given.
        season (str): Season the award is associated with.
        team (Team): Team associated with the award, or the team the player was part of when they received the award.
        player (Person): Person who received the award.
        votes (Optional[int]): Number of votes associated with the award, if applicable.
        notes (Optional[str]): Additional notes or comments about the award.
    """

    id: str
    name: str
    date: str
    season: str
    team: Team
    player: Person
    votes: Optional[int] = None
    notes: Optional[str] = None
