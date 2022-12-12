from dataclasses import dataclass, field
from typing import List

from mlbstatsapi.models.people import DraftPick
from mlbstatsapi import mlb_module


@dataclass
class Round:
    round: str
    picks: List[DraftPick]

    def __post_init__(self):
        picks = []
        for pick in self.picks:
            picks.append(DraftPick(**(mlb_module.merge_keys(pick, ['person']))))
        self.picks = picks
