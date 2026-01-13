from typing import Optional, List
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import RunnerMovement, RunnerDetails, RunnerCredits


class PlayRunner(MLBBaseModel):
    """
    A class to represent a play runner.

    Attributes
    ----------
    movement : RunnerMovement
        Runner movements.
    details : RunnerDetails
        Runner details.
    credits : List[RunnerCredits]
        Runner credits.
    """
    movement: RunnerMovement
    details: RunnerDetails
    credits: List[RunnerCredits] = []
