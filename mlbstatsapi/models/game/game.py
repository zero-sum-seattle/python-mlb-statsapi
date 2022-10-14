from typing import Union
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
    gamePk : int
        id number of this game
    link : str
        link to the api address for this game
    copyright : str
        MLB AM copyright information
    metaData : MetaData
        metaData of this game
    gameData : GameData
        gameData of this game
    liveData : LiveData
        liveData of this game

    Methods
    -------
    id():
        returns this games id
    """
    gamePk: int
    link: str
    metaData: Union[MetaData, dict]
    gameData: Union[GameData, dict]
    liveData: Union[LiveData, dict]

    def __post_init__(self):
        self.metaData = MetaData(**self.metaData)
        self.gameData = GameData(**self.gameData)
        self.liveData = LiveData(**self.liveData)

    @property
    def id(self):
        return self.gamePk
