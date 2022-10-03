from .splits import HittingSplits, PitchingSplits
from typing import List, Union

class Stats:
    """
    A class to represent a Stat.

    Attributes
    ----------
    """
    stat_group: str 
    stat_type: str  
    splits: List[Union[HittingSplits, PitchingSplits]]

    def __init__(self, group: str, type: str, splits: list, **kwargs) -> None:
        self.stat_group = group['displayName']
        self.stat_type = type['displayName']

        if splits:
            self.splits = self._build_splits(splits)

        self.__dict__.update(**kwargs) # assign kwargs

    def _build_splits(self, splits: list) -> None:
        splitList = []

        if self.stat_group == "hitting":
            for split in splits:
                splitList.append(HittingSplits(**split) if isinstance(split, dict) else None)
        elif self.stat_group == "pitching":
            for split in splits:
                splitList.append(PitchingSplits(**split) if isinstance(split, dict) else None)

        return splitList
 
    def __len__(self):
        return len(self.splits)