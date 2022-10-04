from dataclasses import dataclass, field


@dataclass
class Venue:
    """
    A class to represent a venue.

    Attributes
    ----------
    id : int
        id number of the venue
    name: str
        name of the venue
    link : str
        link of the venue
    """
    id: int = field(default=None)
    link: str = field(default=None)
    name: str = field(default=None)