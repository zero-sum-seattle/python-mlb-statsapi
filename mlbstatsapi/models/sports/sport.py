from typing import Optional
from pydantic import BaseModel


class Sport(BaseModel):
    """
    A class to represent a sport.

    Attributes
    ----------
    id : int
        id number of the sport
    link : str
        link of the sport
    name : str 
        name the sport
    code : str
        Sport code
    abbreviation : str
        Abbreviation for the sport
    sortorder : int
        Some sort of sorting order
    activestatus : bool
        Is the sport active
    """
    id: int
    link: str
    name: Optional[str]
    code: Optional[str]
    abbreviation: Optional[str]
    sortOrder: Optional[int]
    activeStatus: Optional[bool]
