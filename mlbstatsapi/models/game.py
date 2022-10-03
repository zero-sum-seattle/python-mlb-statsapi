from typing import Union, List, Dict, Any
from dataclasses import dataclass, field
from mlbstatsapi.game_modules import MetaData, GameData, LiveData


@dataclass
class Game:
    gamePk:     int
    link:       str
    metaData:   Union[MetaData, Dict[str, Any]]
    gameData:   Union[GameData, Dict[str, Any]]
    liveData:   Union[LiveData, Dict[str, Any]]

    def __post_init__(self):
        self.metaData = MetaData(**metaData)
        self.gameData = GameData(**gameData)
        self.liveData = LiveData(**liveData)

    @property
    def id(self):
        return self.gamePk
