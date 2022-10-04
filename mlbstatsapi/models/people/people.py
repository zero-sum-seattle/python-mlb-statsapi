from .person import Person
from .attributes import PrimaryPosition
from dataclasses import dataclass, field
from typing import Union, Optional

@dataclass
class Status:
    """
    A dataclass to hold player status

    Attributes
    ----------
    code : str
        code of the player
    description : str
        description of the status
    """
    code: str
    description: str

@dataclass 
class Player:
    """
    A class to represent a Person.

    Attributes
    ----------
    id : int
        id number of the person
    full_name : str
        full_name of the person
    status : 
        Status of the player
    parentTeamId : int
    """
    jerseyNumber: str
    parentTeamId: int
    position: Union[PrimaryPosition, dict] = field(default_factory=dict)
    person: Union[Person, dict] = field(default_factory=dict)
    status: Union[Status, dict] = field(default_factory=dict)
    def __post_init__(self):
        self.position = PrimaryPosition(**self.position) if self.position else self.position
        self.person = Person(**self.person) if self.person else self.person
        self.status = Status(**self.status) if self.status else self.status 