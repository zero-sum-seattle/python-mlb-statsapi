from dataclasses import dataclass


@dataclass
class Division:
    """
    A class to represent a division.

    Attributes
    ----------
    id : int
        id number of the divison
    name: str
        name of the division
    link : str
        link of the division
    """
    id: int = None
    name: str = None
    link: str = None