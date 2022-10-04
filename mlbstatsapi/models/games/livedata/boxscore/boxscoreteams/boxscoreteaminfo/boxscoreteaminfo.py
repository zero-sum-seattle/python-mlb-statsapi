from typing import Union, Dict, List, Any
from dataclasses import dataclass

@dataclass
class BoxScoreVL:
    label: str
    value: str

@dataclass
class BoxScoreTeamInfo:
    title:      str
    fieldList:  Union[List[BoxScoreVL], List[Dict[str, Any]]]

    def __post_init__(self):
        self.fieldList = [BoxScoreVL(**fieldLists) for fieldLists in fieldList]
