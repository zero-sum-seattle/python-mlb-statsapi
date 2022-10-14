from typing import Optional
from dataclasses import dataclass

@dataclass
class Sport:
    """
    A class to represent a sport.

    Attributes
    ----------
    id : int
        id number of the sport
    link : str
        link of the sport
    name : str = None
        name the sport
    code : str = None
        Sport code
    abbreviation : str = None
        Abbreviation for the sport
    sortOrder : int = None
        Some sort of sorting order
    activeStatus : bool = None
        Is the sport active
    """
    id: int
    link: str
    name: Optional[str] = None
    code: Optional[str] = None
    abbreviation: Optional[str] = None
    sortOrder: Optional[int] = None
    activeStatus: Optional[bool] = None
