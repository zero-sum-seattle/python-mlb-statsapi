from typing import List, Any
from pydantic import field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person
from .attributes import Info, Status, Round


class HomeRunDerby(MLBBaseModel):
    """
    A class representing a homerun derby.

    Attributes
    ----------
    info : Info
        Information about the event.
    status : Status
        The status of the game.
    rounds : List[Round]
        The rounds in the game.
    players : List[Person]
        The players in the game.
    """
    info: Info
    status: Status
    rounds: List[Round] = []
    players: List[Person] = []

    @field_validator('players', mode='before')
    @classmethod
    def clean_players(cls, v: Any) -> Any:
        """Remove 'stats' key from player dicts before validation."""
        if isinstance(v, list):
            cleaned = []
            for player in v:
                if isinstance(player, dict) and 'stats' in player:
                    player = {k: val for k, val in player.items() if k != 'stats'}
                cleaned.append(player)
            return cleaned
        return v
