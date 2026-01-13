from typing import Optional
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.game.gamedata import GameData
from mlbstatsapi.models.game.livedata import LiveData
from .attributes import MetaData


class Game(MLBBaseModel):
    """
    A class to represent a Game.

    Attributes
    ----------
    game_pk : int
        ID number of this game.
    link : str
        Link to the API address for this game.
    metadata : MetaData
        Metadata of this game.
    game_data : GameData
        Game data of this game.
    live_data : LiveData
        Live data of this game.
    """
    game_pk: int = Field(alias="gamepk")
    link: str
    metadata: Optional[MetaData] = None
    game_data: Optional[GameData] = Field(default=None, alias="gamedata")
    live_data: Optional[LiveData] = Field(default=None, alias="livedata")

    @property
    def id(self) -> int:
        """Returns this game's ID."""
        return self.game_pk
