from typing import Union, Optional
from dataclasses import dataclass

from mlbstatsapi.models.game.gamedata import GameData
from mlbstatsapi.models.game.livedata import LiveData

from .attributes import MetaData
from pydantic import BaseModel


class Game(BaseModel):
    """Represents a game with detailed information.

    Attributes:
        gamePk (int): ID number of this game.
        link (str): Link to the API address for this game.
        copyright (str): MLB AM copyright information.
        metaData (MetaData): MetaData of this game.
        gameData (GameData): GameData of this game.
        liveData (LiveData): LiveData of this game.

    Methods:
        id: Returns this game's ID.
    """
    gamePk: int
    link: str
    metaData: MetaData
    gameData: GameData
    liveData: LiveData

    @property
    def id(self):
        return self.gamePk


