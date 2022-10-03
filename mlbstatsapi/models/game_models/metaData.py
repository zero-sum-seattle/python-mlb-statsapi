from typing import Union, List
from dataclasses import dataclass, field

@dataclass
class MetaData:
    wait:           int
    timeStamp:      str
    gameEvents:     List[str]
    logicalEvents:  List[str]
