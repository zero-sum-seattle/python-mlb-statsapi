from dataclasses import dataclass, field


@dataclass
class Home:
    """
    A home is a where a draft player is from

    Attributes
    ----------
    city : str
        The city where the player is from.
    state : str
        The state where the player is from.
    country : str
        The country where the player is from.
    """
    city: str
    state: str
    country: str

@dataclass
class School:
    """
    Represents the school the draft player is from.

    Attributes
    ----------
    name : str
        The name of the school.
    schoolclass : str
        The class the student is in.
    city : str
        The city where the school is located.
    country : str
        The country where the school is located.
    state : str
        The state where the school is located.
    """
    name: str
    schoolclass: str
    city: str
    country: str
    state: str