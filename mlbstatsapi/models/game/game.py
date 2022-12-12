from typing import Union, Optional
from dataclasses import dataclass

from mlbstatsapi.models.game.gamedata import GameData
from mlbstatsapi.models.game.livedata import LiveData

from .attributes import MetaData


@dataclass
class Game:
    """
    A class to represent a Game.

    Attributes
    ----------
    gamepk : int
        id number of this game
    link : str
        link to the api address for this game
    copyright : str
        MLB AM copyright information
    metadata : MetaData
        metaData of this game
    gamedata : GameData
        gameData of this game
    livedata : LiveData
        liveData of this game

    Methods
    -------
    id():
        returns this games id
    """
    gamepk: int
    link: str
    metadata: Union[MetaData, dict]
    gamedata: Union[GameData, dict]
    livedata: Union[LiveData, dict]

    def __post_init__(self):
        self.metadata = MetaData(**self.metadata)
        self.gamedata = GameData(**self.gamedata)
        self.livedata = LiveData(**self.livedata)

    @property
    def id(self):
        return self.gamepk
