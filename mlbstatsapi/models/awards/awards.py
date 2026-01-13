from typing import List
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import Award


class Awards(MLBBaseModel):
    """
    A class representing an awards collection.

    Attributes
    ----------
    awards : List[Award]
        List of awards.
    """
    awards: List[Award] = []
