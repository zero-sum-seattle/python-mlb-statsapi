from typing import Union, List, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel

from .attributes import RunnerMovement, RunnerDetails, RunnerCredits


class PlayRunner(BaseModel):
    """
    A class to represent a play runner.

    Attributes:
        movement (RunnerMovement): Runner movements.
        details (RunnerDetails): Runner details.
        credits (Optional[List[RunnerCredits]]): Runner credits, optional, defaults to an empty list.
    """

    movement: RunnerMovement
    details: RunnerDetails
    credits: Optional[List[RunnerCredits]] = []
