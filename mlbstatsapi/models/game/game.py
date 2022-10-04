from typing import Union, List, Dict, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.game import MetaData
from mlbstatsapi.models.game.gamedata import GameData # Import would be consistent through the project
from mlbstatsapi.models.game.livedata import LiveData



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
    gamePk:     int
    link:       str
    copyright:  str
    metaData:   Union[MetaData, Dict[str, Any]]
    gameData:   Union[GameData, Dict[str, Any]]
    liveData:   Union[LiveData, Dict[str, Any]]

    def __post_init__(self):
        self.metaData = MetaData(**self.metaData)
        self.gameData = GameData(**self.gameData)
        self.liveData = LiveData(**self.liveData)

    @property
    def id(self):
        return self.gamePk
