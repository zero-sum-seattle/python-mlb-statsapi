from typing import Optional
from dataclasses import dataclass, InitVar


@dataclass(repr=False)
class Sport:
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
    name: Optional[str] = None
    code: Optional[str] = None
    abbreviation: Optional[str] = None
    sortorder: Optional[int] = None
    activestatus: Optional[bool] = None

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))