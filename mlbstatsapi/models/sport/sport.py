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
    name : str
        name the sport
    """
    id: int
    link: str
    name: str
