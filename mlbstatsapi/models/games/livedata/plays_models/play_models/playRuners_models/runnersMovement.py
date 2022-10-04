from dataclasses import dataclass

@dataclass
class PlaysPlayRunnersMovement:
    originBase: str = None
    start:      str = None
    end:        str = None
    outBase:    str = None
    isOut:      bool
    outNumber:  int
