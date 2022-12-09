from typing import Union, List, Optional
from dataclasses import dataclass, field

from .attributes import RunnerMovement, RunnerDetails, RunnerCredits


@dataclass
class PlayRunner:
    """
    A class to represent a play runner.

    Attributes
    ----------
    movement: RunnerMovement
        Runner movements
    details: RunnerDetails
        Runner details
    credits: List[RunnerCredits]
        Runner credits
    """
    movement: Union[RunnerMovement, dict]
    details: Union[RunnerDetails, dict]
    credits: Optional[Union[List[RunnerCredits], List[dict]]] = field(default_factory=list)

    def __post_init__(self):
        self.movement = RunnerMovement(**self.movement)
        self.details = RunnerDetails(**self.details)
        self.credits = [RunnerCredits(**credit) for credit in self.credits]
