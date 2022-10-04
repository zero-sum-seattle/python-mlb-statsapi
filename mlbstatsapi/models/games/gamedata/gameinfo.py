from dataclasses import dataclass

@dataclass
class GameInfo:
    attendance: int
    firstPitch: str
    gameDurationMinutes: int
    delayDurationMinutes: int
