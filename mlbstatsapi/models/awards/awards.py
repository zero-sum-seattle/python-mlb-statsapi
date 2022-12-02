from typing import List
from dataclasses import dataclass

from .attributes import Award

@dataclass
class Awards:
    """
    This class represents an awards object

    Attributes
    ----------
    awards : List[Award]
        Awards
    """

    awards: List[Award]
