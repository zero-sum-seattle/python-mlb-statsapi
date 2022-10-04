from typing import Union, Dict, List, Any
from dataclasses import dataclass

@dataclass
class BoxScoreVL:
    """
    A class to represent a boxscore team's infos label and value

    Attributes
    ----------
    label : str
        The label for this peice of info
    value : str = None
        The info associated with this label
    """
    label: str
    value: str = None

@dataclass
class BoxScoreTeamInfo:
    """
    A class to represent a boxscore team's info

    Attributes
    ----------
    title : str
        Type of information
    fieldList : List[BoxScoreVL]
        List holding the info for this info type
    """
    title:      str
    fieldList:  Union[List[BoxScoreVL], List[Dict[str, Any]]]

    def __post_init__(self):
        self.fieldList = [BoxScoreVL(**fieldLists) for fieldLists in self.fieldList]
