from typing import Union, List, Dict, Any
from dataclasses import dataclass, field
from mlbstatsapi.models.game.gamedata import GameData # Import would be consistent through the project
from mlbstatsapi.models.game.livedata import LiveData

@dataclass
class MetaData:
    wait:           int
    timeStamp:      str
    gameEvents:     List[str]
    logicalEvents:  List[str]

@dataclass
class Game:
    copyright:  str
    gamePk:     int
    link:       str
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
