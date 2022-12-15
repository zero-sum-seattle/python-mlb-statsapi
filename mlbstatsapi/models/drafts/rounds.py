from dataclasses import dataclass, field
from typing import List

from mlbstatsapi.models.people import DraftPick
from mlbstatsapi import mlb_module


@dataclass
class Round:
    """
    Represents a round of the MLB draft.

    Attributes
    ----------
    round : str
        The round number of the draft, represented as a string.
    picks : List[DraftPick]
        A list of DraftPick objects representing the picks made in this round of the draft.
    """
    round: str
    picks: List[DraftPick]

    def __post_init__(self):
        picks = []
        for pick in self.picks:
            picks.append(DraftPick(**(mlb_module.merge_keys(pick, ['person']))))
        self.picks = picks
