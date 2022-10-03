from dataclasses import dataclass

@dataclass
class GameStatus:
    abstractGameState: str
    codedGameState: str
    detailedState: str
    statusCode: str
    startTimeTBD: bool
    abstractGameCode: str
