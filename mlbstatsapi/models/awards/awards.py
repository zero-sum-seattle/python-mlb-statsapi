from typing import List
from pydantic import BaseModel

# Assuming the import for Award is correctly defined elsewhere in your project
from .attributes import Award

class Awards(BaseModel):
    """Represents an awards object.

    Attributes:
        awards (List[Award]): A list of awards.
    """

    awards: List[Award]
